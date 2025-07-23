"""
간단한 라우터 테스트 - AAA 패턴 사용
Simple router tests - using AAA pattern

테스트는 최소한으로 유지하고 핵심 기능만 검증
Keep tests minimal and verify only core functionality
"""

import pytest
from src.routing.simple_router import SimpleRouter


class TestSimpleRouter:
    """간단한 라우터 테스트 클래스 / Simple router test class"""
    
    def test_router_initialization(self):
        """
        라우터 초기화 테스트
        Test router initialization
        """
        # Arrange (준비) - 테스트 데이터 준비
        # Nothing to arrange
        
        # Act (실행) - 테스트할 동작 실행
        router = SimpleRouter()
        
        # Assert (검증) - 결과 검증
        assert router is not None
        assert len(router.agents) == 4
        assert "rag" in router.agents
        assert "slack" in router.agents
        assert "browser" in router.agents
        assert "playwright" in router.agents
    
    def test_keyword_routing_rag(self):
        """
        RAG 에이전트 키워드 라우팅 테스트
        Test keyword routing for RAG agent
        """
        # Arrange (준비)
        router = SimpleRouter()
        test_request = "search for documents about machine learning"
        
        # Act (실행)
        result = router.route_by_keywords(test_request)
        
        # Assert (검증)
        assert result == "rag"
    
    def test_keyword_routing_slack(self):
        """
        Slack 에이전트 키워드 라우팅 테스트
        Test keyword routing for Slack agent
        """
        # Arrange (준비)
        router = SimpleRouter()
        test_request = "send a message to the team"
        
        # Act (실행)
        result = router.route_by_keywords(test_request)
        
        # Assert (검증)
        assert result == "slack"
    
    def test_keyword_routing_browser(self):
        """
        Browser 에이전트 키워드 라우팅 테스트
        Test keyword routing for Browser agent
        """
        # Arrange (준비)
        router = SimpleRouter()
        test_request = "scrape the website for product data"
        
        # Act (실행)
        result = router.route_by_keywords(test_request)
        
        # Assert (검증)
        assert result == "browser"
    
    def test_keyword_routing_no_match(self):
        """
        키워드 매칭 실패 테스트
        Test keyword routing failure
        """
        # Arrange (준비)
        router = SimpleRouter()
        test_request = "hello world how are you"
        
        # Act (실행)
        result = router.route_by_keywords(test_request)
        
        # Assert (검증)
        assert result is None
    
    def test_manual_routing_success(self):
        """
        수동 라우팅 성공 테스트
        Test manual routing success
        """
        # Arrange (준비)
        router = SimpleRouter()
        agent_name = "rag"
        
        # Act (실행)
        result = router.route_manually(agent_name)
        
        # Assert (검증)
        assert result == "rag"
    
    def test_manual_routing_failure(self):
        """
        수동 라우팅 실패 테스트
        Test manual routing failure
        """
        # Arrange (준비)
        router = SimpleRouter()
        invalid_agent_name = "nonexistent_agent"
        
        # Act (실행)
        result = router.route_manually(invalid_agent_name)
        
        # Assert (검증)
        assert result is None
    
    def test_list_agents(self):
        """
        에이전트 목록 조회 테스트
        Test listing agents
        """
        # Arrange (준비)
        router = SimpleRouter()
        
        # Act (실행)
        agents = router.list_agents()
        
        # Assert (검증)
        assert len(agents) == 4
        assert "rag" in agents
        assert "slack" in agents
        assert "browser" in agents
        assert "playwright" in agents
    
    def test_get_agent_success(self):
        """
        에이전트 객체 가져오기 성공 테스트
        Test get agent success
        """
        # Arrange (준비)
        router = SimpleRouter()
        
        # Act (실행)
        agent = router.get_agent("rag")
        
        # Assert (검증)
        assert agent is not None
        assert agent.name == "rag_agent"
    
    def test_get_agent_failure(self):
        """
        에이전트 객체 가져오기 실패 테스트
        Test get agent failure
        """
        # Arrange (준비)
        router = SimpleRouter()
        
        # Act (실행)
        agent = router.get_agent("nonexistent")
        
        # Assert (검증)
        assert agent is None
    
    def test_analyze_request(self):
        """
        요청 분석 테스트
        Test request analysis
        """
        # Arrange (준비)
        router = SimpleRouter()
        test_request = "search for API documentation"
        
        # Act (실행)
        analysis = router.analyze(test_request)
        
        # Assert (검증)
        assert analysis['request'] == test_request
        assert 'scores' in analysis
        assert 'recommended' in analysis
        assert analysis['recommended'] == "rag"  # search 키워드로 인해
        assert analysis['method'] == 'keyword'