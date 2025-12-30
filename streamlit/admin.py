import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from src.core.config import settings
from src.llm.factory import LLMFactory
from src.llm.models import SUPPORTED_MODELS
from src.prompts.prompt_manager import PromptManager
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="LLM Admin Console", layout="wide")


def load_jsonl(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)


st.title("🚀 LLM Admin Console")

tab1, tab2 = st.tabs(["📊 Dashboard", "🎮 Playground"])

# --- Dashboard ---
with tab1:
    st.header("System Observability")

    col1, col2 = st.columns(2)

    # 2.1 LLM Cost & Usage
    with col1:
        st.subheader("LLM Cost & Usage")
        df_cost = load_jsonl(settings.COST_LOG_PATH)
        if not df_cost.empty:
            df_cost["timestamp"] = pd.to_datetime(df_cost["timestamp"])

            # Key Metrics
            total_cost = df_cost["cost"].sum()
            total_tokens = df_cost["total_tokens"].sum()
            total_calls = len(df_cost)

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Cost", f"${total_cost:.4f}")
            m2.metric("Total Tokens", f"{total_tokens:,}")
            m3.metric("LLM Calls", f"{total_calls:,}")

            # Daily Cost Trend
            df_cost["date"] = df_cost["timestamp"].dt.date
            daily_cost = df_cost.groupby("date")["cost"].sum().reset_index()
            fig_cost = px.bar(
                daily_cost, x="date", y="cost", title="Daily Cost Trend (USD)"
            )
            st.plotly_chart(fig_cost, use_container_width=True)

            # Usage by Model
            model_usage = df_cost.groupby("model")["cost"].sum().reset_index()
            fig_model = px.pie(
                model_usage,
                values="cost",
                names="model",
                title="Cost Distribution by Model",
            )
            st.plotly_chart(fig_model, use_container_width=True)
        else:
            st.info("No cost logs found yet.")

    # 2.2 API Performance
    with col2:
        st.subheader("API Performance")
        df_api = load_jsonl(settings.API_REQUEST_LOG_PATH)
        if not df_api.empty:
            df_api["timestamp"] = pd.to_datetime(df_api["timestamp"])

            # Endpoint Summary Table
            # Need to aggregate by path
            summary = (
                df_api.groupby("path")
                .agg(
                    {
                        "method": "count",
                        "latency_ms": ["mean", lambda x: x.quantile(0.95)],
                        "status_code": lambda x: (x == 200).mean() * 100,
                    }
                )
                .reset_index()
            )

            # Flatten columns
            summary.columns = [
                "Endpoint",
                "Requests",
                "Avg Latency (ms)",
                "P95 Latency (ms)",
                "Success Rate (%)",
            ]
            st.dataframe(summary, hide_index=True)

            # Latency over time
            fig_lat = px.line(
                df_api,
                x="timestamp",
                y="latency_ms",
                color="path",
                title="Latency Over Time (ms)",
            )
            st.plotly_chart(fig_lat, use_container_width=True)
        else:
            st.info("No API logs found yet.")

# --- Playground ---
with tab2:
    st.header("Developer Playground")

    with st.sidebar:
        st.subheader("Settings")

        # Model Selection (Synced with SUPPORTED_MODELS)
        model_options = list(SUPPORTED_MODELS.keys())
        selected_model = st.selectbox("Select Model", model_options)

        # Auto Provider Detection
        provider = SUPPORTED_MODELS[selected_model]["provider"]
        st.caption(f"Detected Provider: **{provider.upper()}**")

        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)

        st.divider()
        st.subheader("Template Manager")

        # Load Templates
        templates = PromptManager.get_template_names()
        selected_template = st.selectbox("Load Template", ["None"] + templates)

        default_system = "You are a helpful assistant."
        if selected_template != "None":
            try:
                t_data = PromptManager.load_template(selected_template)
                default_system = t_data.get("template", default_system)
                st.success(f"Loaded {selected_template}")
            except Exception as e:
                st.error(f"Error loading template: {e}")

        system_prompt = st.text_area("System Prompt", value=default_system, height=200)

        if st.button("Download Chat History"):
            chat_json = json.dumps(
                st.session_state.get("messages", []), ensure_ascii=False, indent=2
            )
            st.download_button(
                "Click to Download", chat_json, "chat_history.json", "application/json"
            )

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Enter your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Construct LangChain messages
                    lc_messages = [SystemMessage(content=system_prompt)]
                    for m in st.session_state.messages:
                        if m["role"] == "user":
                            lc_messages.append(HumanMessage(content=m["content"]))
                        else:
                            lc_messages.append(AIMessage(content=m["content"]))

                    # Create LLM
                    llm = LLMFactory.create(
                        provider=provider, model=selected_model, temperature=temperature
                    )

                    # Invoke
                    # Note: LLMFactory uses structured output by default.
                    # The response object will be a Pydantic model (DefaultJSONResponse)
                    result = llm.invoke(lc_messages)

                    # Extract text responses
                    # DefaultJSONResponse has 'responses' list
                    response_text = result.responses[0]

                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )

                except Exception as e:
                    st.error(f"Error: {str(e)}")
