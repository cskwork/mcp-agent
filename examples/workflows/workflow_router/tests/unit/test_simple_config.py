"""
간단한 설정 모듈 테스트 - AAA 패턴
Simple config module tests - AAA pattern

설정 관리의 핵심 기능만 테스트합니다.
Test only core functionality of configuration management.
"""

import pytest
import os
from unittest.mock import patch, mock_open
from src.utils.simple_config import SimpleConfig


class TestSimpleConfig:
    """간단한 설정 테스트 클래스 / Simple config test class"""
    
    def test_config_initialization(self):
        """
        설정 초기화 테스트
        Test config initialization
        """
        # Arrange (준비)
        # Nothing to arrange
        
        # Act (실행)
        config = SimpleConfig()
        
        # Assert (검증)
        assert config is not None
        assert config.project_root is not None
        assert config._secrets is None  # 아직 로드되지 않았음 / Not loaded yet
    
    def test_get_api_key_from_env(self, mock_anthropic_key):
        """
        환경변수에서 API 키 가져오기 테스트
        Test getting API key from environment variable
        """
        # Arrange (준비)
        config = SimpleConfig()
        
        # Act (실행)
        api_key = config.get_api_key('anthropic')
        
        # Assert (검증)
        assert api_key == "test-key-12345"
    
    @patch('builtins.open', mock_open(read_data="""
anthropic:
  api_key: sk-ant-test-key-from-file

openai:
  api_key: sk-openai-test-key
"""))
    @patch('pathlib.Path.exists')
    def test_get_api_key_from_file(self, mock_exists):
        """
        파일에서 API 키 가져오기 테스트
        Test getting API key from file
        """
        # Arrange (준비)
        mock_exists.return_value = True
        config = SimpleConfig()
        
        # Act (실행)
        api_key = config.get_api_key('anthropic')
        
        # Assert (검증)
        assert api_key == "sk-ant-test-key-from-file"
    
    def test_get_api_key_none_when_missing(self):
        """
        API 키가 없을 때 None 반환 테스트
        Test returning None when API key is missing
        """
        # Arrange (준비)
        config = SimpleConfig()
        config.secrets_file = None  # 파일 없음 / No file
        
        # Act (실행)
        api_key = config.get_api_key('nonexistent')
        
        # Assert (검증)
        assert api_key is None
    
    @patch('builtins.open', mock_open(read_data="""
anthropic:
  api_key: anthropic_api_key  # 템플릿 값 / Template value
"""))
    @patch('pathlib.Path.exists')
    def test_get_api_key_ignores_template_values(self, mock_exists):
        """
        템플릿 값을 무시하는 테스트
        Test ignoring template values
        """
        # Arrange (준비)
        mock_exists.return_value = True
        config = SimpleConfig()
        
        # Act (실행)
        api_key = config.get_api_key('anthropic')
        
        # Assert (검증)
        assert api_key is None  # 템플릿 값이므로 None / None because it's template value
    
    def test_has_required_keys_false_when_no_anthropic(self):
        """
        Anthropic 키가 없을 때 required_keys가 False인지 테스트
        Test has_required_keys returns False when no Anthropic key
        """
        # Arrange (준비)
        config = SimpleConfig()
        config.secrets_file = None
        
        # Act (실행)
        has_keys = config.has_required_keys()
        
        # Assert (검증)
        assert has_keys is False
    
    @patch('builtins.open', mock_open(read_data="""
anthropic:
  api_key: sk-ant-real-key-here
"""))
    @patch('pathlib.Path.exists')
    def test_has_required_keys_true_when_anthropic_exists(self, mock_exists):
        """
        Anthropic 키가 있을 때 required_keys가 True인지 테스트
        Test has_required_keys returns True when Anthropic key exists
        """
        # Arrange (준비)
        mock_exists.return_value = True
        config = SimpleConfig()
        
        # Act (실행)
        has_keys = config.has_required_keys()
        
        # Assert (검증)
        assert has_keys is True
    
    def test_get_status_returns_dict(self):
        """
        get_status가 딕셔너리를 반환하는지 테스트
        Test that get_status returns a dictionary
        """
        # Arrange (준비)
        config = SimpleConfig()
        
        # Act (실행)
        status = config.get_status()
        
        # Assert (검증)
        assert isinstance(status, dict)
        assert 'secrets_file_found' in status
        assert 'anthropic_key_available' in status
        assert 'ready_to_use' in status