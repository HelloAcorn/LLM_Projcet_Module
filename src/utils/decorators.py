from functools import wraps
from typing import List, Any
from app.utils.callbacks import CostCallbackHandler

def measure_cost(func):
    """
    함수 호출 시 CostCallbackHandler를 callbacks 인자에 자동으로 주입하는 데코레이터.
    LangChain 모델 생성 함수에 적용하여 비용 추적 기능을 활성화합니다.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # kwargs에서 callbacks 리스트 가져오기 (없으면 생성)
        callbacks = kwargs.get("callbacks", [])
        
        # 이미 CostCallbackHandler가 있는지 확인
        if not any(isinstance(c, CostCallbackHandler) for c in callbacks):
            callbacks.append(CostCallbackHandler())
            
        # kwargs 업데이트
        kwargs["callbacks"] = callbacks
        
        return func(*args, **kwargs)
    return wrapper

