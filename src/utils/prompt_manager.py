"""YAML 프롬프트 관리 유틸리티"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_prompt(yaml_path: str, key: str = "template"):
    """YAML 파일에서 프롬프트 템플릿 로드"""
    yaml_path = Path(yaml_path)
    
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML 파일을 찾을 수 없습니다: {yaml_path}")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if key not in data:
        raise KeyError(f"'{key}' 키가 YAML에 없습니다: {yaml_path}")
    
    return data[key]


def load_yaml(yaml_path: str):
    """전체 YAML 파일 로드"""
    yaml_path = Path(yaml_path)
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
