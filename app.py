"""
Foundry Local + Fabric Semantic Model Integration
Multi-page Streamlit application combining:
1. Chat interface with intelligent model routing
2. Fabric semantic model integration with DAX generation
3. Configuration and workspace management
"""

import re
import os
import requests
import streamlit as st
from pathlib import Path

# Add current directory to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from modules import (
    FabricDaxGenerator,
    PowerBIExecutor,
    TokenManager,
    WorkspaceManager
)

# Configure Streamlit page
st.set_page_config(
    page_title="Foundry Local + Fabric",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get Foundry API base URL from environment or default to localhost
FOUNDRY_BASE = os.getenv("FOUNDRY_BASE", "http://127.0.0.1:51970/v1")


@st.cache_data(ttl=300)
def fetch_models():
    """Fetch available models from Foundry API (5-min cache)."""
    try:
        r = requests.get(f"{FOUNDRY_BASE}/models", timeout=30)
        r.raise_for_status()
        data = r.json()
        models = sorted([m["id"] for m in data.get("data", [])])
        if models:
            return models
    except Exception:
        pass
    
    # Fallback: Return common Foundry models if service not responding
    return [
        "qwen2.5-14b-instruct",
        "qwen2.5-7b-instruct", 
        "phi-3.5-mini-instruct",
        "phi-3-small-instruct"
    ]


def pick_default_models(models: list[str]) -> tuple[str | None, str | None]:
    """
    Returns (phi_model_id, qwen_model_id) if found, otherwise (None, None)
    """
    phi = next((m for m in models if m.lower().startswith("phi-")), None)
    qwen = next((m for m in models if m.lower().startswith("qwen")), None)
    return phi, qwen


def auto_route_model(prompt: str, phi_id: str | None, qwen_id: str | None) -> str | None:
    """
    Simple routing heuristics:
    - Longer prompts -> Qwen
    - Code/debugging/steps/architecture words -> Qwen
    - Otherwise -> Phi (faster)
    """
    if not prompt.strip():
        return qwen_id or phi_id

    p = prompt.strip()
    words = re.findall(r"\w+", p.lower())
    word_count = len(words)

    heavy_keywords = [
        "explain", "compare", "why", "how", "steps", "architecture", "design",
        "optimize", "performance", "refactor", "debug", "error", "traceback",
        "sql", "pipeline", "fabric", "synapse", "databricks", "rag", "agent"
    ]
    looks_heavy = any(k in p.lower() for k in heavy_keywords)

    if qwen_id and (word_count >= 25 or len(p) >= 160 or looks_heavy):
        return qwen_id

    return phi_id or qwen_id


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Answer clearly and concisely."}]
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "workspace_id" not in st.session_state:
    st.session_state.workspace_id = None
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None
if "last_dax_query" not in st.session_state:
    st.session_state.last_dax_query = None
if "last_results" not in st.session_state:
    st.session_state.last_results = None


def home_page():
    """Render the home/chat page."""
    st.title("🧠 Foundry Local Chat (Auto Model Select)")

    # ---- Load models ----
    with st.sidebar:
        st.header("⚙️ Chat Settings")

        foundry_available = False
        try:
            r = requests.get(f"{FOUNDRY_BASE}/models", timeout=5)
            r.raise_for_status()
            data = r.json()
            models = sorted([m["id"] for m in data.get("data", [])])
            if models:
                foundry_available = True
            else:
                foundry_available = False
                models = [
                    "qwen2.5-14b-instruct",
                    "phi-3.5-mini-instruct"
                ]
                st.warning("⚠️ Foundry Local not responding - Demo Mode Active")
        except Exception as e:
            foundry_available = False
            models = [
                "qwen2.5-14b-instruct",
                "phi-3.5-mini-instruct"
            ]
            st.warning("⚠️ Using Demo Mode (Foundry not available)")

        phi_id, qwen_id = pick_default_models(models)
        
        # Set defaults if found
        if not phi_id and models:
            phi_id = models[0]
        if not qwen_id and models:
            qwen_id = models[0]

        st.caption("Model routing")
        mode = st.radio(
            "Choose mode",
            ["Auto (recommended)", "Manual"],
            index=0,
            key="chat_mode"
        )

        if mode == "Manual":
            # Find index of first qwen or phi, otherwise 0
            default_idx = 0
            for i, m in enumerate(models):
                if "qwen" in m.lower():
                    default_idx = i
                    break
            selected_model = st.selectbox("Select a model", models, index=default_idx, key="manual_model")
            st.caption(f"✓ Selected: {selected_model}")
        else:
            # Auto mode: show the defaults we'll route between
            st.success("✅ Auto Mode Active")
            st.write("Auto route between:")
            st.write(f"- 🚀 **Fast**: {phi_id or '(not found)'}")
            st.write(f"- 💪 **Powerful**: {qwen_id or '(not found)'}")
            selected_model = None  # chosen per prompt

        # Demo mode toggle
        st.divider()
        st.caption("Testing & Demo")
        
        # Auto-enable demo mode if Foundry not available
        default_demo_mode = not foundry_available
        demo_mode = st.toggle("🎮 Demo Mode (Mock Responses)", value=default_demo_mode, help="When enabled, shows demo responses without needing Foundry Local")
        
        if demo_mode:
            st.success("✅ Demo Mode ON - Mock responses enabled")
        elif foundry_available:
            st.success("✅ Live Mode ON - Connected to Foundry Local")
            st.info("ℹ️ Demo Mode auto-enabled (Foundry Local not responding). Disable to use real Foundry once it's running.")

        system_prompt = st.text_area(
            "System prompt",
            value=st.session_state.messages[0].get("content", "Answer clearly and concisely."),
            height=90,
            key="system_prompt_chat"
        )

        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    # Update system prompt
    if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
        st.session_state.messages[0]["content"] = system_prompt

    # Render history (skip system)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                if "model_used" in msg and msg["role"] == "assistant":
                    st.caption(f"Model: {msg['model_used']}")
                st.markdown(msg["content"])

    prompt = st.chat_input("Ask something...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Decide model
        if mode == "Manual":
            model_to_use = selected_model
        else:
            model_to_use = auto_route_model(prompt, phi_id, qwen_id)

        if not model_to_use:
            with st.chat_message("assistant"):
                st.error("Could not auto-pick a model (Phi/Qwen not found). Switch to Manual mode.")
            st.stop()

        payload = {
            "model": model_to_use,
            "messages": st.session_state.messages,
        }

        try:
            with st.chat_message("assistant"):
                st.caption(f"Model: {model_to_use}" + (" [DEMO]" if demo_mode else ""))
                with st.spinner(f"Thinking with {model_to_use}..."):
                    # Demo mode: return mock response
                    if demo_mode:
                        import time
                        time.sleep(2)  # Simulate thinking time
                        answer = f"""**[DEMO MODE - Mock Response]**

This is a demonstration response showing how the app works. In production with Foundry Local running, you would receive an actual AI-generated response here.

Query: "{prompt}"
Model: {model_to_use}
Status: Demo Mode Active ✓

To use real responses:
1. Start Foundry Local service
2. Turn off Demo Mode
3. Refresh and try again"""
                    else:
                        r = requests.post(
                            f"{FOUNDRY_BASE}/chat/completions",
                            json=payload,
                            timeout=180,
                        )
                        r.raise_for_status()
                        data = r.json()
                        answer = data["choices"][0]["message"]["content"]
                    
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "model_used": model_to_use}
                    )
                    st.markdown(answer)

        except Exception as e:
            error_str = str(e)
            with st.chat_message("assistant"):
                if "connection" in error_str.lower() or "refused" in error_str.lower():
                    st.error("""
❌ **Connection Failed**

Foundry Local service is not responding at `http://127.0.0.1:51970`

**To fix:**
1. Install Foundry Local
2. Start the service:
   ```
   foundry service start
   foundry model run qwen2.5-14b-instruct
   ```
3. Refresh this page

**Alternative:** Use Demo Mode below
                    """)
                    
                    # Offer demo mode
                    if st.button("🎮 Try Demo Mode (Mock Response)"):
                        demo_answer = f"[DEMO MODE] This is a simulated response from {model_to_use}. In production, you would see a real response from the model."
                        st.session_state.messages.append(
                            {"role": "assistant", "content": demo_answer, "model_used": f"{model_to_use} (demo)"}
                        )
                        st.markdown(demo_answer)
                        st.rerun()
                else:
                    st.error(f"❌ Error: {error_str}")
                    st.info("Try again or check your Foundry Local installation.")


def main():
    """Main entry point - handles multi-page navigation."""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🚀 Foundry + Fabric")
        st.divider()
        
        page = st.radio(
            "Navigate:",
            ["💬 Chat", "⚙️ Settings", "📊 Semantic Query"],
            index=0
        )
        
        # Display authentication status
        st.divider()
        if st.session_state.authenticated:
            st.success("✅ Authenticated")
            if st.session_state.workspace_id:
                st.write(f"📍 Workspace: `{st.session_state.get('workspace_name', 'N/A')}`")
            if st.session_state.dataset_id:
                st.write(f"📊 Dataset: `{st.session_state.get('dataset_name', 'N/A')}`")
        else:
            st.info("ℹ️ Go to Settings to authenticate")
    
    # Route to pages
    if page == "💬 Chat":
        home_page()
    elif page == "⚙️ Settings":
        from pages.workspace_config import workspace_config_page
        workspace_config_page()
    elif page == "📊 Semantic Query":
        from pages.semantic_query import semantic_query_page
        semantic_query_page()


if __name__ == "__main__":
    main()
