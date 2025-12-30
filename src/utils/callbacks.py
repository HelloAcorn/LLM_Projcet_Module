import datetime
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from src.utils.logger import logger_manager
from src.llm.models import SUPPORTED_MODELS

class CostCallbackHandler(BaseCallbackHandler):
    """Callback Handler that logs the cost of LLM calls."""
    
    def __init__(self):
        super().__init__()
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        try:
            for generation in response.generations:
                for chunk in generation:
                    # Universal Token Extraction Logic
                    # This attempts to find usage info in standard LangChain locations
                    usage_metadata = {}
                    
                    # 1. Check message metadata (common in newer LangChain versions)
                    if hasattr(chunk, 'message') and hasattr(chunk.message, 'usage_metadata'):
                         usage_metadata = chunk.message.usage_metadata
                    
                    # 2. Check generation_info (older or specific providers)
                    if not usage_metadata and hasattr(chunk, 'generation_info') and chunk.generation_info:
                         usage_metadata = chunk.generation_info.get("token_usage", {})
                         if not usage_metadata:
                             # Some providers might put it directly in generation_info keys
                             pass # Logic can be expanded here
                    
                    # 3. Fallback to LLMResult.llm_output (often aggregated)
                    if not usage_metadata and response.llm_output:
                        usage_metadata = response.llm_output.get("token_usage", {})

                    if not usage_metadata:
                        # If no usage info found, we can't calculate cost.
                        # Logging a warning might be appropriate, or just skipping.
                        continue

                    model_name = response.llm_output.get("model_name", "unknown") if response.llm_output else "unknown"
                    
                    # Ensure numeric values
                    prompt_tokens = int(usage_metadata.get("prompt_tokens", usage_metadata.get("input_tokens", 0)))
                    completion_tokens = int(usage_metadata.get("completion_tokens", usage_metadata.get("output_tokens", 0)))
                    total_tokens = int(usage_metadata.get("total_tokens", prompt_tokens + completion_tokens))
                    
                    # Calculate cost based on SUPPORTED_MODELS pricing
                    # Cost in models.py is per 1M tokens
                    model_spec = SUPPORTED_MODELS.get(model_name, {})
                    
                    # If model name from API doesn't match exactly (e.g. version suffix), 
                    # one might implement fuzzy matching here. For now, strict match.
                    input_price_per_1m = model_spec.get("input_cost", 0.0)
                    output_price_per_1m = model_spec.get("output_cost", 0.0)
                    
                    cost = (prompt_tokens / 1_000_000 * input_price_per_1m) + (completion_tokens / 1_000_000 * output_price_per_1m)
                    
                    log_entry = {
                        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                        "model": model_name,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                        "cost": cost,
                        "trace_id": "N/A" # Trace ID injection could be handled via context vars if needed
                    }
                    
                    logger_manager.log_cost(log_entry)
                    
        except Exception as e:
            # Prevent callback errors from crashing the main application
            logger_manager.get_logger().error(f"Error in CostCallbackHandler: {e}")

