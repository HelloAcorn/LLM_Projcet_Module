import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

# Pricing Table (USD per 1M tokens)
# Note: This is an estimation. Prices may vary by provider updates.
PRICING = {
    # OpenAI (GPT-5.2 Series)
    "gpt-5.2-chat-latest": {"input": 1.75, "output": 14.00}, # Instant
    "gpt-5.2": {"input": 1.75, "output": 14.00},             # Thinking
    "gpt-5-mini": {"input": 0.50, "output": 2.00},           # Legacy Mock
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},          # Legacy
    
    # Anthropic
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},     # Mock Price
    "claude-sonnet-4-5": {"input": 4.00, "output": 16.00},    # Mock Price
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},      # Mock Price

    # Gemini
    "gemini-3-pro-preview": {"input": 4.00, "output": 12.00},   # Mock Price
    "gemini-3-flash-preview": {"input": 0.40, "output": 1.20}, # Mock Price
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40}   # Mock Price
}

# Export supported models list for UI consistency
SUPPORTED_MODELS = list(PRICING.keys())

class CostCallbackHandler(BaseCallbackHandler):
    """Callback Handler that logs the cost of LLM calls to a JSONL file."""
    
    def __init__(self, log_path: str = "logs/cost.jsonl"):
        self.log_path = log_path
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        try:
            # Debug log
            print(f"[CostCallback] on_llm_end called. llm_output: {response.llm_output}")
            
            model_name = "unknown"
            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0
            
            # Try to extract from llm_output first
            if response.llm_output:
                model_name = response.llm_output.get("model_name", "unknown")
                token_usage = response.llm_output.get("token_usage", {})
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                total_tokens = token_usage.get("total_tokens", 0)
            
            # If token_usage is still 0, try to extract from generations
            if total_tokens == 0 and response.generations:
                for gen_list in response.generations:
                    for gen in gen_list:
                        # Check generation_info
                        if hasattr(gen, 'generation_info') and gen.generation_info:
                            info = gen.generation_info
                            if 'usage_metadata' in info and info['usage_metadata']:
                                usage = info['usage_metadata']
                                prompt_tokens = usage.get('input_tokens', 0)
                                completion_tokens = usage.get('output_tokens', 0)
                                total_tokens = usage.get('total_tokens', prompt_tokens + completion_tokens)
                            if 'model_name' in info:
                                model_name = info['model_name']
                        
                        # Check message response_metadata
                        if hasattr(gen, 'message') and hasattr(gen.message, 'response_metadata'):
                            meta = gen.message.response_metadata
                            if meta:
                                # Try token_usage (OpenAI style)
                                if 'token_usage' in meta and meta['token_usage']:
                                    usage = meta['token_usage']
                                    prompt_tokens = usage.get('prompt_tokens', 0)
                                    completion_tokens = usage.get('completion_tokens', 0)
                                    total_tokens = usage.get('total_tokens', prompt_tokens + completion_tokens)
                                if 'model_name' in meta:
                                    model_name = meta['model_name']
                        
                        # Check usage_metadata directly on message
                        if hasattr(gen, 'message') and hasattr(gen.message, 'usage_metadata'):
                            usage_meta = gen.message.usage_metadata
                            if usage_meta and total_tokens == 0:
                                prompt_tokens = usage_meta.get('input_tokens', 0)
                                completion_tokens = usage_meta.get('output_tokens', 0)
                                total_tokens = usage_meta.get('total_tokens', prompt_tokens + completion_tokens)
            
            # Calculate cost
            cost = self._calculate_cost(model_name, prompt_tokens, completion_tokens)
            
            # Trace ID (Run ID)
            run_id = kwargs.get("run_id")
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost": round(cost, 6),
                "trace_id": str(run_id) if run_id else None
            }
            
            # Append to log file
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            print(f"[CostCallback] Logged: {log_entry}")
                
        except Exception as e:
            # Log error but don't interrupt main flow
            print(f"[CostCallback] Error logging cost: {e}")

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        # Normalize model name (handle specific version tags if needed)
        price = PRICING.get(model)
        
        if not price:
            # Fallback for unknown models - try partial matching
            for key in PRICING:
                if key in model:
                    price = PRICING[key]
                    break
        
        if not price:
            return 0.0

        # Price is per 1M tokens
        input_cost = (prompt_tokens / 1_000_000) * price["input"]
        output_cost = (completion_tokens / 1_000_000) * price["output"]
        
        return input_cost + output_cost
