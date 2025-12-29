import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os
import json
import sys
from pathlib import Path

# Add src to python path to import modules
current_dir = Path(__file__).parent
project_root = current_dir.parent
src_path = project_root / "src"

# 1. Add project root to sys.path so we can import 'src'
sys.path.append(str(project_root))

# 2. Add src to sys.path so we can import modules inside it directly if needed
sys.path.append(str(src_path))

# 3. Alias 'src' to 'app' to satisfy 'from app.core...' imports
try:
    import src
    sys.modules["app"] = src
except ImportError as e:
    st.error(f"Failed to setup module alias: {e}")

try:
    from src.llm.llm_factory import LLMFactory
    from langchain.schema import SystemMessage, HumanMessage
    from src.utils.callbacks import SUPPORTED_MODELS # Import from callbacks
except ImportError as e:
    st.error(f"Failed to import src modules: {e}")
    st.stop()

# ==========================================
# Global Configuration
# ==========================================
# Models are now imported from src.utils.callbacks

PROMPT_TEMPLATE_DIR = str(project_root / "src/prompts/templates")
COST_LOG_FILE = str(project_root / "logs/cost.jsonl")
API_LOG_FILE = str(project_root / "logs/api_requests.jsonl")

# Ensure prompt directory exists
os.makedirs(PROMPT_TEMPLATE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(COST_LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(API_LOG_FILE), exist_ok=True)

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="AI Service Admin Console",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛠️ AI Service Admin Console")

# ==========================================
# Data Loaders
# ==========================================
def load_cost_data():
    """Load cost data from JSONL logs."""
    if not os.path.exists(COST_LOG_FILE):
        return pd.DataFrame(columns=['timestamp', 'model', 'prompt_tokens', 'completion_tokens', 'total_tokens', 'cost'])
    
    data = []
    try:
        with open(COST_LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    except Exception as e:
        st.error(f"Error reading cost logs: {e}")
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def load_api_data():
    """Load API request logs."""
    if not os.path.exists(API_LOG_FILE):
        return pd.DataFrame(columns=['timestamp', 'method', 'path', 'status_code', 'latency_ms'])
    
    data = []
    try:
        with open(API_LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    except Exception as e:
        # Fail silently or log error
        pass
        
    df = pd.DataFrame(data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# ==========================================
# Sidebar Navigation
# ==========================================
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Playground"]
)

# ==========================================
# 1. Dashboard (Observability)
# ==========================================
if menu == "Dashboard":
    st.header("📊 System Observability")
    
    # Load Data
    df_cost = load_cost_data()
    df_api = load_api_data()
    
    # --- LLM Cost Metrics ---
    st.subheader("💰 LLM Cost & Usage")
    if df_cost.empty:
        st.info("No cost data available yet.")
        total_cost = 0.0
        total_tokens = 0
    else:
        total_cost = df_cost['cost'].sum()
        total_tokens = df_cost['total_tokens'].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Cost (Est.)", f"${total_cost:.4f}")
        c2.metric("Total Tokens", f"{total_tokens:,}")
        c3.metric("LLM Calls", f"{len(df_cost):,}")
        
        # Charts
        tab1, tab2 = st.tabs(["Daily Cost", "Model Distribution"])
        with tab1:
            df_cost['date'] = df_cost['timestamp'].dt.date
            daily_cost = df_cost.groupby(['date', 'model'])['cost'].sum().reset_index()
            fig = px.bar(daily_cost, x='date', y='cost', color='model', title="Daily Cost by Model")
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            model_usage = df_cost['model'].value_counts().reset_index()
            model_usage.columns = ['model', 'count']
            fig = px.pie(model_usage, values='count', names='model', title="Usage by Model")
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- API Performance Metrics ---
    st.subheader("⚡ API Performance (by Endpoint)")
    if df_api.empty:
        st.info("No API log data available yet.")
    else:
        # Calculate stats per endpoint
        stats = []
        for endpoint in df_api['path'].unique():
            df_ep = df_api[df_api['path'] == endpoint]
            total_requests = len(df_ep)
            avg_latency = df_ep['latency_ms'].mean()
            p95_latency = df_ep['latency_ms'].quantile(0.95)
            success_count = df_ep[df_ep['status_code'] == 200].shape[0]
            success_rate = (success_count / total_requests) * 100 if total_requests > 0 else 0
            
            stats.append({
                "Endpoint": endpoint,
                "Requests": total_requests,
                "Avg Latency (ms)": round(avg_latency, 2),
                "P95 Latency (ms)": round(p95_latency, 2),
                "Success Rate (%)": round(success_rate, 1)
            })
        
        summary_df = pd.DataFrame(stats)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ==========================================
# 2. Developer Tools (Playground)
# ==========================================
elif menu == "Playground":
    st.header("🎮 Sandboxed Playground")
    
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_sidebar:
        st.subheader("Settings")
        
        # Initialize session state for model
        if "last_model" not in st.session_state:
            st.session_state.last_model = None

        model_id = st.selectbox("Model", SUPPORTED_MODELS)
        
        # Clear history if model changes
        if st.session_state.last_model != model_id:
            st.session_state.messages = []
            st.session_state.last_model = model_id
            st.toast(f"Model changed to {model_id}. Chat history cleared.")
        
        # Determine provider based on model name
        if "gpt" in model_id:
            provider = "openai"
        elif "claude" in model_id:
            provider = "anthropic"
        elif "gemini" in model_id:
            provider = "gemini"
        else:
            provider = "openai" # Default fallback
            
        temp = st.slider("Temperature", 0.0, 1.0, 0.7)
        
        st.divider()
        st.subheader("Template Manager")
        
        # Load Templates
        templates = [f for f in os.listdir(PROMPT_TEMPLATE_DIR) if f.endswith(('.txt', '.yaml', '.md'))]
        selected_template = st.selectbox("Load Template", ["(None)"] + templates)
        
        if st.button("Load"):
            if selected_template != "(None)":
                try:
                    with open(os.path.join(PROMPT_TEMPLATE_DIR, selected_template), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if selected_template.endswith('.yaml'):
                            import yaml # Lazy import
                            try:
                                data = yaml.safe_load(content)
                                if isinstance(data, dict) and 'template' in data:
                                    st.session_state['system_prompt'] = data['template']
                                    st.toast(f"Loaded template from {selected_template}")
                                else:
                                    st.session_state['system_prompt'] = content
                                    st.warning("YAML loaded but 'template' field not found. Loaded full content.")
                            except Exception as e:
                                st.session_state['system_prompt'] = content
                                st.error(f"YAML Parse Error: {e}. Loaded raw content.")
                        else:
                            st.session_state['system_prompt'] = content
                            st.toast(f"Loaded {selected_template}")
                except Exception as e:
                    st.error(f"Failed to load file: {e}")

        # Download Chat History
        st.divider()
        if "messages" in st.session_state and st.session_state.messages:
            chat_json = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Download Chat History",
                data=chat_json,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    with col_main:
        # System Prompt Editor
        st.subheader("System Prompt")
        system_prompt = st.text_area(
            "Define agent persona & rules",
            value=st.session_state.get('system_prompt', "You are a helpful assistant."),
            height=150,
            key='system_prompt_input'
        )
        # Sync text area with session state
        st.session_state['system_prompt'] = system_prompt

        st.divider()
        st.subheader("Chat")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Test your prompt here..."):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                with st.spinner("Thinking..."):
                    try:
                        # 1. Create LLM Instance
                        llm = LLMFactory.create(
                            provider=provider,
                            model=model_id,
                            temperature=temp,
                            streaming=True 
                        )
                        
                        # 2. Prepare Messages
                        messages = [
                            SystemMessage(content=system_prompt),
                            HumanMessage(content=prompt)
                        ]
                        
                        # 3. Invoke LLM
                        try:
                            response = llm.invoke(messages)
                            # [DEBUG LOG]
                            print(f"[DEBUG] Raw Response Type: {type(response)}")
                            print(f"[DEBUG] Raw Response: {response}")
                                
                        except Exception as invoke_err:
                            st.error(f"LLM Invoke Error: {invoke_err}")
                            full_response = f"❌ Error: {str(invoke_err)}"
                            message_placeholder.error(full_response)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            st.stop()
                        
                        # Handle Structured Output with include_raw=True
                        # Response format: {"raw": AIMessage, "parsed": DefaultJSONResponse, "parsing_error": None}
                        if isinstance(response, dict) and "parsed" in response:
                            parsed = response.get("parsed")
                            raw = response.get("raw")
                            
                            # Extract text content
                            if parsed and hasattr(parsed, 'response'):
                                full_response = parsed.response
                            elif raw and hasattr(raw, 'content'):
                                full_response = raw.content
                            else:
                                full_response = str(parsed) if parsed else ""
                            
                            # Extract token usage and log cost
                            prompt_tokens = 0
                            completion_tokens = 0
                            total_tokens = 0
                            model_name = model_id
                            
                            if raw:
                                # Get model name from response_metadata
                                if hasattr(raw, 'response_metadata') and raw.response_metadata:
                                    model_name = raw.response_metadata.get('model_name', model_id)
                                    
                                    # Try token_usage first (OpenAI style)
                                    token_usage = raw.response_metadata.get('token_usage')
                                    if token_usage and isinstance(token_usage, dict):
                                        prompt_tokens = token_usage.get('prompt_tokens', 0)
                                        completion_tokens = token_usage.get('completion_tokens', 0)
                                        total_tokens = token_usage.get('total_tokens', 0)
                                
                                # Try usage_metadata (Anthropic/Gemini style)
                                if total_tokens == 0 and hasattr(raw, 'usage_metadata') and raw.usage_metadata:
                                    usage_meta = raw.usage_metadata
                                    prompt_tokens = usage_meta.get('input_tokens', 0)
                                    completion_tokens = usage_meta.get('output_tokens', 0)
                                    total_tokens = usage_meta.get('total_tokens', prompt_tokens + completion_tokens)
                                
                                # Calculate cost
                                from src.utils.callbacks import PRICING
                                price = PRICING.get(model_name, {})
                                if not price:
                                    # Fallback partial match
                                    for key in PRICING:
                                        if key in model_name:
                                            price = PRICING[key]
                                            break
                                            
                                if price:
                                    input_cost = (prompt_tokens / 1_000_000) * price.get("input", 0)
                                    output_cost = (completion_tokens / 1_000_000) * price.get("output", 0)
                                    cost = input_cost + output_cost
                                else:
                                    cost = 0.0
                                
                                # Log to file
                                log_entry = {
                                    "timestamp": datetime.now().isoformat(),
                                    "model": model_name,
                                    "prompt_tokens": prompt_tokens,
                                    "completion_tokens": completion_tokens,
                                    "total_tokens": total_tokens,
                                    "cost": round(cost, 6)
                                }
                                with open(COST_LOG_FILE, "a", encoding="utf-8") as f:
                                    f.write(json.dumps(log_entry) + "\n")
                                print(f"[CostLog] {log_entry}")
                        
                        elif hasattr(response, 'response'):
                            full_response = response.response
                        elif hasattr(response, 'content'):
                            full_response = response.content
                        else:
                            full_response = str(response)

                        if not full_response:
                            st.warning(f"Response is empty/None. Debug info: {response}")

                        message_placeholder.markdown(full_response)
                        
                    except Exception as e:
                        full_response = f"❌ Error: {str(e)}"
                        message_placeholder.error(full_response)
                
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
