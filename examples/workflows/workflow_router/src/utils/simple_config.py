"""
간단한 설정 관리자 - 복잡하지 않고 실용적인 접근 방식
Simple Configuration Manager - Practical, not over-engineered approach

이 모듈은 설정 파일을 간단하게 로드하고 검증합니다.
This module simply loads and validates configuration files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class SimpleConfig:
    """
    간단한 설정 관리 클래스 - 복잡한 기능 없이 핵심만 구현
    Simple configuration management - only essential features
    """
    
    def __init__(self):
        """설정 관리자 초기화 / Initialize configuration manager"""
        self.project_root = Path(__file__).parent.parent.parent
        self.secrets_file = self._find_secrets_file()
        self._secrets = None
    
    def _find_secrets_file(self) -> Optional[Path]:
        """
        시크릿 파일을 찾는 간단한 방법
        Simple way to find secrets file
        """
        # 가능한 위치들을 순서대로 확인 / Check possible locations in order
        possible_paths = [
            self.project_root / "mcp_agent.secrets.yaml",
            Path.cwd() / "mcp_agent.secrets.yaml",
            self.project_root / "config" / "secrets.yaml"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        API 키를 가져오는 간단한 방법
        Simple way to get API key
        
        Args:
            provider: 'anthropic' 또는 'openai' / 'anthropic' or 'openai'
        """
        if not self._secrets:
            self._load_secrets()
        
        if not self._secrets:
            return None
        
        # 환경 변수 먼저 확인 / Check environment variables first
        env_key = f"{provider.upper()}_API_KEY"
        if os.getenv(env_key):
            return os.getenv(env_key)
        
        # 설정 파일에서 확인 / Check config file
        provider_config = self._secrets.get(provider, {})
        api_key = provider_config.get('api_key')
        
        # 템플릿 값이 아닌 실제 키인지 확인 / Check if it's a real key, not template
        if api_key and api_key != f"{provider}_api_key":
            return api_key
        
        return None
    
    def _load_secrets(self):
        """시크릿 파일 로드 / Load secrets file"""
        if not self.secrets_file:
            return
        
        try:
            with open(self.secrets_file, 'r', encoding='utf-8') as f:
                self._secrets = yaml.safe_load(f) or {}
        except Exception:
            # 에러가 나도 계속 실행 / Continue even if error occurs
            self._secrets = {}
    
    def has_required_keys(self) -> bool:
        """
        필수 키가 있는지 확인 (Anthropic만 필수)
        Check if required keys exist (only Anthropic required)
        """
        return bool(self.get_api_key('anthropic'))
    
    def get_status(self) -> Dict[str, Any]:
        """
        현재 설정 상태 반환 / Return current configuration status
        """
        return {
            'secrets_file_found': self.secrets_file is not None,
            'secrets_file_path': str(self.secrets_file) if self.secrets_file else None,
            'anthropic_key_available': bool(self.get_api_key('anthropic')),
            'openai_key_available': bool(self.get_api_key('openai')),
            'ready_to_use': self.has_required_keys()
        }