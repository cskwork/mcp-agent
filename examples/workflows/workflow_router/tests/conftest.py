"""
테스트 설정 파일 - pytest 공통 설정
Test configuration file - pytest common settings

이 파일은 모든 테스트에서 공통으로 사용하는 설정을 정의합니다.
This file defines common settings used across all tests.
"""

import pytest
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_requests():
    """
    테스트용 샘플 요청들 / Sample requests for testing
    
    Returns:
        다양한 에이전트를 위한 샘플 요청 딕셔너리
        Dictionary of sample requests for different agents
    """
    return {
        'rag': [
            "search for documentation about APIs",
            "find information about machine learning",
            "lookup research papers on neural networks"
        ],
        'slack': [
            "send a message to the development team",
            "notify the channel about deployment",
            "post update to team chat"
        ],
        'browser': [
            "scrape product data from website",
            "take screenshot of homepage", 
            "extract content from web page"
        ],
        'playwright': [
            "test login workflow across browsers",
            "automate the checkout process",
            "validate form submission in different browsers"
        ],
        'no_match': [
            "hello how are you",
            "what's the weather like",
            "tell me a joke"
        ]
    }


@pytest.fixture
def mock_anthropic_key(monkeypatch):
    """
    테스트용 Anthropic API 키 모킹 / Mock Anthropic API key for testing
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-12345")


@pytest.fixture 
def mock_openai_key(monkeypatch):
    """
    테스트용 OpenAI API 키 모킹 / Mock OpenAI API key for testing
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-67890")