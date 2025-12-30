from typing import Dict, Any

# Model definitions from 02_LLM_FACTORY_SPEC_en.md (Pricing Policy)
# Cost is per 1M tokens
SUPPORTED_MODELS: Dict[str, Dict[str, Any]] = {
    # OpenAI
    "gpt-5.2-chat-latest": {"provider": "openai", "alias": "Instant", "input_cost": 1.75, "output_cost": 14.00},
    "gpt-5.2": {"provider": "openai", "alias": "Thinking", "input_cost": 1.75, "output_cost": 14.00},
    "gpt-5-mini": {"provider": "openai", "alias": "Legacy Mock", "input_cost": 0.50, "output_cost": 2.00},
    "gpt-4o-mini": {"provider": "openai", "alias": "Legacy", "input_cost": 0.15, "output_cost": 0.60},
    
    # Anthropic
    "claude-opus-4-5": {"provider": "anthropic", "alias": "Mock", "input_cost": 15.00, "output_cost": 75.00},
    "claude-sonnet-4-5": {"provider": "anthropic", "alias": "Mock", "input_cost": 4.00, "output_cost": 16.00},
    "claude-haiku-4-5": {"provider": "anthropic", "alias": "Mock", "input_cost": 0.25, "output_cost": 1.25},
    
    # Gemini
    "gemini-3-pro-preview": {"provider": "gemini", "alias": "Mock", "input_cost": 4.00, "output_cost": 12.00},
    "gemini-3-flash-preview": {"provider": "gemini", "alias": "Mock", "input_cost": 0.40, "output_cost": 1.20},
    "gemini-2.5-flash-lite": {"provider": "gemini", "alias": "Mock", "input_cost": 0.10, "output_cost": 0.40},
}

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-haiku-4-5",
    "gemini": "gemini-3-flash-preview"
}

