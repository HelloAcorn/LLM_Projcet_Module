import os
import yaml
from typing import List, Dict, Any
from src.core.config import settings

class PromptManager:
    @staticmethod
    def get_template_names() -> List[str]:
        """Returns a list of available template filenames"""
        if not os.path.exists(settings.PROMPT_TEMPLATE_DIR):
            return []
        return [f for f in os.listdir(settings.PROMPT_TEMPLATE_DIR) if f.endswith(".yaml")]

    @staticmethod
    def load_template(file_name: str) -> Dict[str, Any]:
        """Loads and parses a YAML file"""
        path = os.path.join(settings.PROMPT_TEMPLATE_DIR, file_name)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompt template not found: {path}")
            
        with open(path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
            
        # Validation
        if "template" not in content:
            raise KeyError(f"Missing required field 'template' in {file_name}")
            
        return content

