import functools
from typing import Any, List
from src.utils.callbacks import CostCallbackHandler

def measure_cost(func):
    """
    Decorator that automatically injects CostCallbackHandler into the 'callbacks' argument 
    of the decorated function if it's missing.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if 'callbacks' is in kwargs
        callbacks = kwargs.get("callbacks", [])
        
        # Ensure it's a list
        if callbacks is None:
            callbacks = []
        
        # Check if CostCallbackHandler is already present
        has_cost_handler = any(isinstance(cb, CostCallbackHandler) for cb in callbacks)
        
        if not has_cost_handler:
            callbacks.append(CostCallbackHandler())
            kwargs["callbacks"] = callbacks
            
        return func(*args, **kwargs)
    return wrapper

