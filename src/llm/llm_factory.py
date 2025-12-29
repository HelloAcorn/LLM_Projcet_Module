"""
LLM 팩토리 모듈

이 모듈은 다양한 LLM(Large Language Model) 제공자의 인스턴스를 생성하는 팩토리 패턴을 구현합니다.

각 제공자별로 모델, 온도 등의 파라미터를 설정할 수 있으며,
적절한 API 키가 .api_key 파일을 통해 제공되어야 합니다.

모든 LLM 인스턴스는 기본적으로 JSON 스키마를 사용한 structured output이 적용됩니다.
"""
from typing import Literal, Optional, Any, Union, Dict

from langchain.chat_models.base import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from pydantic import BaseModel, Field, create_model

from app.core.settings import settings
from app.utils.decorators import measure_cost

ProviderType = Literal["openai", "anthropic", "gemini"]

# 기본 JSON 스키마를 위한 Pydantic 모델 (Gemini 호환성)
class DefaultJSONResponse(BaseModel):
    """기본 JSON 응답 모델"""
    response: str = Field(description="The main response content")

DEFAULT_JSON_SCHEMA = DefaultJSONResponse


class LLMFactory:
    """LLM 인스턴스를 생성하는 팩토리 클래스"""
    
    # 각 제공자별 기본 모델
    DEFAULT_MODELS = {
        "openai": "gpt-5-mini",
        "anthropic": "claude-sonnet-4-5",
        "gemini": "gemini-2.5-flash"
    }
    
    @staticmethod
    @measure_cost
    def create_openai(
        model: str = "gpt-5-mini",
        reasoning_effort: str = "medium",
        temperature: float = 1.0,
        streaming: bool = False,
        json_schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        **kwargs
    ) -> BaseChatModel:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .api_key 파일을 확인하세요.")
        
        # [Fix] Extract callbacks FIRST to avoid Pydantic "supplied twice" error
        callbacks = kwargs.pop("callbacks", [])
        
        # GPT-5 계열만 reasoning_effort 파라미터 사용
        if model.startswith("gpt-5"):
            model_kwargs = {
                "reasoning_effort": reasoning_effort,
            }
            # [Fix] gpt-5 계열은 temperature 1.0 고정 (API 제약)
            temperature = 1.0
            # Add remaining kwargs (callbacks already popped)
            model_kwargs.update(kwargs)
        else:
            # GPT-4 계열은 reasoning_effort 없이
            model_kwargs = kwargs.copy()
        
        llm = ChatOpenAI(
            model=model,
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature,
            streaming=streaming,
            model_kwargs=model_kwargs,
            callbacks=callbacks
        )
        
        # Structured output 적용 (기본 JSON 스키마 또는 커스텀 스키마)
        # include_raw=True: 원본 AIMessage도 반환하여 token_usage 추출 가능
        schema = json_schema if json_schema is not None else DEFAULT_JSON_SCHEMA
        runnable = llm.with_structured_output(schema, include_raw=True)
        
        # 재시도 로직 추가 (Gemini 빈 응답 이슈 대응)
        return runnable.with_retry(stop_after_attempt=2)
    
    @staticmethod
    @measure_cost
    def create_anthropic(
        model: str = "claude-sonnet-4-5",
        temperature: float = 0.7,
        streaming: bool = False,
        json_schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        **kwargs
    ) -> BaseChatModel:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다. .api_key 파일을 확인하세요.")
        
        # [Fix] Extract callbacks FIRST to avoid Pydantic "supplied twice" error
        callbacks = kwargs.pop("callbacks", [])
        
        llm = ChatAnthropic(
            model=model,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            **kwargs
        )
        
        # Structured output 적용 (기본 JSON 스키마 또는 커스텀 스키마)
        # include_raw=True: 원본 AIMessage도 반환하여 token_usage 추출 가능
        schema = json_schema if json_schema is not None else DEFAULT_JSON_SCHEMA
        runnable = llm.with_structured_output(schema, include_raw=True)
        
        # 재시도 로직 추가 (Gemini 빈 응답 이슈 대응)
        return runnable.with_retry(stop_after_attempt=2)
    
    @staticmethod
    @measure_cost
    def create_gemini(
        model: str = "gemini-2.5-flash",
        temperature: float = 1.0,
        top_p: float = 0.95,
        top_k: int = 40,
        streaming: bool = False,
        json_schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        **kwargs
    ) -> BaseChatModel:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. .api_key 파일을 확인하세요.")
        
        # [Fix] Extract callbacks FIRST to avoid Pydantic "supplied twice" error
        callbacks = kwargs.pop("callbacks", [])
        
        # 안전 설정: 모든 차단 해제 (테스트용)
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }

        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            streaming=streaming,
            safety_settings=safety_settings,
            callbacks=callbacks,
            **kwargs
        )
        
        # Structured output 적용 (기본 JSON 스키마 또는 커스텀 스키마)
        # include_raw=True: 원본 AIMessage도 반환하여 token_usage 추출 가능
        schema = json_schema if json_schema is not None else DEFAULT_JSON_SCHEMA
        runnable = llm.with_structured_output(schema, include_raw=True)
        
        # 재시도 로직 추가 (Gemini 빈 응답 이슈 대응)
        return runnable.with_retry(stop_after_attempt=2)
    
    @staticmethod
    def create(
        provider: ProviderType,
        model: Optional[str] = None,
        temperature: float = 1.0,
        streaming: bool = False,
        json_schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        **kwargs
    ) -> BaseChatModel:
        # 기본 모델 설정
        if model is None:
            model = LLMFactory.DEFAULT_MODELS.get(provider)
        
        # 제공자별 인스턴스 생성
        if provider == "openai":
            # GPT-5 추론형 모델: reasoning_effort 사용
            reasoning_effort = kwargs.pop('reasoning_effort', 'medium')
            return LLMFactory.create_openai(
                model=model, 
                reasoning_effort=reasoning_effort,
                temperature=temperature, 
                streaming=streaming,
                json_schema=json_schema,
                **kwargs
            )
        elif provider == "anthropic":
            return LLMFactory.create_anthropic(
                model=model, 
                temperature=temperature, 
                streaming=streaming,
                json_schema=json_schema,
                **kwargs
            )
        elif provider == "gemini":
            # Gemini 2.5 추론형 모델: top_p, top_k 사용
            top_p = kwargs.pop('top_p', 0.95)
            top_k = kwargs.pop('top_k', 10)
            return LLMFactory.create_gemini(
                model=model,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                streaming=streaming,
                json_schema=json_schema,
                **kwargs
            )
        else:
            raise ValueError(f"지원하지 않는 provider: {provider}. 지원 목록: openai, anthropic, gemini")
