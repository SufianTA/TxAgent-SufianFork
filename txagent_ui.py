import os
import streamlit as st
from src.txagent import TxAgent  # assuming txagent is installed as a package
# If tool-specific classes are needed:
# from tooluniverse import ToolUniverse, MCPTool, RESTfulTool, GraphQLTool, OpenFDATool

# --- Page configuration ---
# Set the page title and page icon with the Harvard logo
logo_path = "harvard_logo.jpg"  # Path to the Harvard logo image
if os.path.exists(logo_path):
    st.set_page_config(page_title="TxAgent UI", page_icon=logo_path, layout="centered")
else:
    st.set_page_config(page_title="TxAgent UI", page_icon="🧬", layout="centered")  # Default to DNA if logo is not found


# --- Load logo (if available) and display header ---
logo_path = "logo.png"
header_cols = st.columns([0.15, 0.85])  # allocate space for logo vs title
if os.path.exists(logo_path):
    header_cols[0].image(logo_path, width=80)  # display TxAgent logo
else:
    # If logo.png is not present, display a placeholder or text
    header_cols[0].markdown("🧬")  # using an emoji as placeholder
header_cols[1].markdown("# **TxAgent**")
st.write("*An AI agent for therapeutic reasoning that uses a universe of tools to provide evidence-backed answers in precision medicine.*")  # brief description

# --- Configuration Expander ---
with st.expander("Configuration", expanded=True):
    st.subheader("Model Settings")
    # Select or input Model name
    model_options = ["TxAgent-T1", "GPT-4", "GPT-3.5", "Custom"]  # example options
    model_name = st.selectbox("Select Model", options=model_options, index=0)
    custom_model = None
    if model_name == "Custom":
        custom_model = st.text_input("Enter custom model name or path")
    # Use custom_model if provided
    final_model_name = custom_model if model_name == "Custom" and custom_model else model_name

    rag_model = st.text_input("Enter RAG Model Name", value="mims-harvard/ToolRAG-T1-GTE-Qwen2-1.5B")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3)
    max_new_tokens = st.number_input("Max New Tokens", min_value=1, max_value=2048, value=1024)
    max_rounds = st.number_input("Maximum Rounds", min_value=1, max_value=50, value=20)
    enable_summary = st.checkbox("Enable Summary Mode", value=False)

    st.subheader("Tool Configurations")
    # MCP Tool configuration
    use_mcp = st.checkbox("Enable MCP Tool", value=False)
    mcp_url = st.text_input("MCP Server URL (if using MCP Tool)", value="")  # left blank if not used
    # RESTful Tool configuration
    use_rest = st.checkbox("Enable RESTful API Tool", value=False)
    rest_base_url = st.text_input("RESTful API Base URL", value="")
    # GraphQL Tool configuration
    use_graphql = st.checkbox("Enable GraphQL Tool", value=False)
    graphql_endpoint = st.text_input("GraphQL Endpoint URL", value="")
    # OpenFDA Tool configuration
    use_fda = st.checkbox("Enable OpenFDA Tool", value=False)
    fda_api_key = st.text_input("OpenFDA API Key", value="", type="password")

# Prepare example queries (could also be in sidebar)
example_queries = {
    "Drug Interaction": "What are the risks of combining rivaroxaban with NSAIDs in an elderly patient with hypertension?",
    "Personalized Dosing": "Given a 50-year-old patient with moderate hepatic impairment starting on Drug X (a newly approved medication), how should the dosage be adjusted?",
    "Contraindications": "Is Drug Y contraindicated for a pregnant patient with diabetes and hypertension?",
}
# Sidebar (or top) for examples
st.sidebar.header("Example Queries")
selected_example = st.sidebar.selectbox("Select an example question", [""] + list(example_queries.keys()))
if selected_example and selected_example in example_queries:
    st.session_state["user_query"] = example_queries[selected_example]

st.subheader("Agent Interaction")
# Query text area
default_query = st.session_state.get("user_query", "")
user_query = st.text_area("Enter your query", value=default_query, height=100,
                          placeholder="Type a medical question or select an example from the sidebar")
# Run button
run_button = st.button("🔍 Run TxAgent")

# --- Handling the query execution ---
if run_button and user_query:
    # Instantiate TxAgent with chosen models and parameters
    agent = TxAgent(model_name=final_model_name, rag_model_name=rag_model)

    # If specific tool configurations are enabled, pass them to the agent or initialize tools
    tool_kwargs = {}
    if use_mcp and mcp_url:
        tool_kwargs["mcp_url"] = mcp_url
    if use_rest and rest_base_url:
        tool_kwargs["rest_base_url"] = rest_base_url
    if use_graphql and graphql_endpoint:
        tool_kwargs["graphql_endpoint"] = graphql_endpoint
    if use_fda and fda_api_key:
        os.environ["FDA_API_KEY"] = fda_api_key  # set environment variable for OpenFDA Tool
        tool_kwargs["openfda_api_key"] = fda_api_key

    # (If the TxAgent API allows enabling/disabling tools, we would pass these tool_kwargs accordingly.
    # For example, agent.configure_tools(**tool_kwargs) or when running the query, agent.run(query, tools=...))
    # Here, we'll assume TxAgent automatically picks up env vars and internal configs for tools.

    # Run the agent to get answer (and reasoning). We use a spinner to indicate processing.
    with st.spinner("TxAgent is thinking..."):
        # Suppose TxAgent has a method to return reasoning and answer:
        result = agent.run(user_query, temperature=temperature, max_new_tokens=max_new_tokens, max_rounds=max_rounds, enable_summary=enable_summary, **tool_kwargs)
        # (In practice, the actual call might differ. It could be agent.chat or agent.run_query etc.)
        # We will assume `result` contains a dict with 'answer' and 'reasoning'.
        # For demonstration, if `result` is just the answer string, we set reasoning to None.
        if isinstance(result, dict):
            final_answer = result.get("answer", "*(No answer returned)*")
            reasoning_trace = result.get("reasoning", "")
        else:
            final_answer = str(result)
            reasoning_trace = getattr(agent, "last_reasoning", "")  # assume the agent stores its last reasoning trace

    # Display the results
    st.write("**Answer:**")
    st.success(final_answer)  # highlight answer in success box

    if reasoning_trace:
        with st.expander("Show reasoning trace"):
            st.markdown(reasoning_trace)
