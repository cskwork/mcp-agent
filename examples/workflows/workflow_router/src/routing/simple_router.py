"""
간단한 에이전트 라우터 - 복잡하지 않은 실용적 접근
Simple Agent Router - Practical, not complex approach

이 라우터는 3가지 방법으로 작동합니다:
This router works in 3 ways:
1. 키워드 매칭 (빠름) / Keyword matching (fast)
2. LLM 분석 (정확함) / LLM analysis (accurate) 
3. 수동 선택 (확실함) / Manual selection (certain)
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from mcp_agent.workflows.router.router_llm_anthropic import AnthropicLLMRouter
from mcp_agent.workflows.router.router_llm_openai import OpenAILLMRouter

from ..agents.rag_agent import create_rag_agent, RAG_KEYWORDS
from ..agents.slack_agent import create_slack_agent, SLACK_KEYWORDS  
from ..agents.browser_agent import create_browser_agent, BROWSER_KEYWORDS
from ..agents.playwright_agent import create_playwright_agent, PLAYWRIGHT_KEYWORDS


class SimpleRouter:
    """
    간단한 라우터 클래스 - 3가지 라우팅 방법 제공
    Simple router class - provides 3 routing methods
    """
    
    def __init__(self, llm_provider: str = "anthropic"):
        """
        라우터 초기화 / Initialize router
        
        Args:
            llm_provider: 사용할 LLM ('anthropic' 또는 'openai')
        """
        # 에이전트들을 생성 / Create agents
        self.agents = {
            "rag": create_rag_agent(),
            "slack": create_slack_agent(), 
            "browser": create_browser_agent(),
            "playwright": create_playwright_agent()
        }
        
        # 키워드 매핑 / Keyword mappings
        self.keywords = {
            "rag": RAG_KEYWORDS,
            "slack": SLACK_KEYWORDS,
            "browser": BROWSER_KEYWORDS, 
            "playwright": PLAYWRIGHT_KEYWORDS
        }
        
        # LLM 라우터 초기화 / Initialize LLM router
        self._init_llm_router(llm_provider)
    
    def _init_llm_router(self, provider: str):
        """LLM 라우터 초기화 / Initialize LLM router"""
        all_agents = list(self.agents.values())
        
        try:
            if provider.lower() == "anthropic":
                self.llm_router = AnthropicLLMRouter(
                    server_names=["fetch", "filesystem"],
                    agents=all_agents,
                    functions=[]
                )
            else:
                self.llm_router = OpenAILLMRouter(
                    agents=all_agents,
                    functions=[]
                )
        except Exception:
            # LLM 라우터 실패해도 키워드 라우팅은 작동 / Keyword routing works even if LLM fails
            self.llm_router = None
    
    def route_by_keywords(self, request: str) -> Optional[str]:
        """
        키워드로 라우팅 - 가장 빠른 방법
        Route by keywords - fastest method
        
        Returns:
            에이전트 이름 또는 None / Agent name or None
        """
        request_lower = request.lower()
        scores = {}
        
        # 각 에이전트의 키워드 점수 계산 / Calculate keyword scores for each agent
        for agent_name, agent_keywords in self.keywords.items():
            score = 0
            for keyword in agent_keywords:
                # 단어 경계를 사용해서 정확한 매칭 / Use word boundaries for exact matching
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = len(re.findall(pattern, request_lower))
                score += matches
            scores[agent_name] = score
        
        # 가장 높은 점수의 에이전트 반환 / Return agent with highest score
        if max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    async def route_by_llm(self, request: str) -> Optional[str]:
        """
        LLM으로 라우팅 - 가장 정확한 방법
        Route by LLM - most accurate method
        """
        if not self.llm_router:
            return None
        
        try:
            results = await self.llm_router.route_to_agent(request, top_k=1)
            if results:
                agent = results[0].result
                # 에이전트 이름 찾기 / Find agent name
                for name, stored_agent in self.agents.items():
                    if stored_agent.name == agent.name:
                        return name
        except Exception:
            # LLM 에러가 나도 None 반환 / Return None even if LLM errors
            pass
        
        return None
    
    def route_manually(self, agent_name: str) -> Optional[str]:
        """
        수동으로 라우팅 - 가장 확실한 방법
        Route manually - most certain method
        """
        if agent_name in self.agents:
            return agent_name
        return None
    
    async def route(self, request: str, method: str = "smart") -> Tuple[Optional[str], str]:
        """
        메인 라우팅 함수 - 3가지 방법 중 선택
        Main routing function - choose from 3 methods
        
        Args:
            request: 사용자 요청 / User request
            method: 라우팅 방법 ("smart", "keyword", "llm") / Routing method
            
        Returns:
            (에이전트 이름, 사용된 방법) / (agent name, method used)
        """
        if method == "keyword":
            agent_name = self.route_by_keywords(request)
            return agent_name, "keyword"
        
        elif method == "llm":
            agent_name = await self.route_by_llm(request)
            return agent_name, "llm"
        
        else:  # method == "smart" (기본값 / default)
            # 먼저 키워드 시도 / Try keywords first
            agent_name = self.route_by_keywords(request)
            if agent_name:
                return agent_name, "keyword"
            
            # 키워드 실패시 LLM 시도 / Try LLM if keywords fail
            agent_name = await self.route_by_llm(request)
            return agent_name, "llm" if agent_name else "none"
    
    def get_agent(self, agent_name: str):
        """에이전트 객체 가져오기 / Get agent object"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """사용 가능한 에이전트 목록 / List available agents"""
        return list(self.agents.keys())
    
    def analyze(self, request: str) -> Dict[str, Any]:
        """
        요청 분석 - 디버깅용
        Analyze request - for debugging
        """
        scores = {}
        request_lower = request.lower()
        
        for agent_name, agent_keywords in self.keywords.items():
            score = 0
            matched_keywords = []
            
            for keyword in agent_keywords:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = len(re.findall(pattern, request_lower))
                if matches > 0:
                    matched_keywords.append(keyword)
                score += matches
            
            scores[agent_name] = {
                'score': score,
                'matched_keywords': matched_keywords
            }
        
        # 추천 에이전트 결정 / Determine recommended agent
        best_score = max(s['score'] for s in scores.values())
        recommended = None
        if best_score > 0:
            for name, data in scores.items():
                if data['score'] == best_score:
                    recommended = name
                    break
        
        return {
            'request': request,
            'scores': scores,
            'recommended': recommended,
            'method': 'keyword' if recommended else 'llm_needed'
        }