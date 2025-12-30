from typing import Literal, Optional, Type, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from src.core.config import settings
from src.llm.models import SUPPORTED_MODELS, DEFAULT_MODELS
from src.utils.callbacks import CostCallbackHandler

class DefaultJSONResponse(BaseModel):
    """Fallback JSON schema when none is provided."""
    responses: list[str] = Field(..., description="The list of response strings from the LLM.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata if applicable.")

class LLMFactory:
    @staticmethod
    def create(
        provider: Literal["openai", "anthropic", "gemini"],
        model: Optional[str] = None,
        json_schema: Optional[Type[BaseModel]] = None,
        **kwargs
    ) -> BaseChatModel:
        # Determine model
        if model is None:
            model = DEFAULT_MODELS.get(provider)
        
        # Verify model belongs to provider (Optional validation)
        # if model in SUPPORTED_MODELS and SUPPORTED_MODELS[model]["provider"] != provider:
        #     model = DEFAULT_MODELS.get(provider)

        # Initialize base model
        if provider == "openai":
            base_llm = ChatOpenAI(
                model=model,
                api_key=settings.OPENAI_API_KEY,
                callbacks=[CostCallbackHandler()],
                **kwargs
            )
        elif provider == "anthropic":
            base_llm = ChatAnthropic(
                model=model,
                anthropic_api_key=settings.ANTHROPIC_API_KEY,
                callbacks=[CostCallbackHandler()],
                **kwargs
            )
        elif provider == "gemini":
            base_llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=settings.GEMINI_API_KEY,
                callbacks=[CostCallbackHandler()],
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Apply structured output
        # Strict Mode logic depends on the specific provider's implementation of with_structured_output
        schema = json_schema or DefaultJSONResponse
        
        # Note: 'strict' parameter might be needed depending on langchain version and provider
        return base_llm.with_structured_output(schema)

