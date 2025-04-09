
import streamlit as st
from txagent import TxAgent
import json
from datetime import datetime

st.set_page_config(page_title="TxAgent", layout="wide")
st.title("🧬 TxAgent – Biomedical Reasoning Assistant")
query = st.text_input("Enter your biomedical question", "")
agent = TxAgent()

if 'history' not in st.session_state:
    st.session_state['history'] = []

if query:
    with st.spinner("Thinking..."):
        reasoning, tool_output = agent.run_with_reasoning(query)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.append({
            "timestamp": timestamp,
            "query": query,
            "reasoning": reasoning,
            "output": tool_output
        })

st.subheader("📜 Query History")
for entry in reversed(st.session_state.history):
    st.markdown(f"**🕒 {entry['timestamp']}**")
    st.markdown(f"**🔍 Query:** {entry['query']}")
    st.markdown(f"**🧠 Reasoning:** `{entry['reasoning']}`")
    st.markdown("**📤 Output:**")
    st.code(json.dumps(entry['output'], indent=2), language='json')
    st.markdown("---")
