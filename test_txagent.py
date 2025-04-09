
import unittest
from txagent import TxAgent
from tooluniverse.mcp_tool import MCPTool

class TestTxAgent(unittest.TestCase):
    def setUp(self):
        # Initialize TxAgent with default configurations
        self.tx_agent = TxAgent(model_name="GPT-3", rag_model_name="Default RAG Model")
        self.mcp_tool = MCPTool(tool_config={"call_url": "https://mcp-server.com/call"})

    def test_run_txagent(self):
        # Test running TxAgent with an example query
        input_text = "What is the weather like today?"
        result = self.tx_agent.run(input_text)
        self.assertIsNotNone(result)
        self.assertIn("weather", result.lower())  # Assuming the result will contain 'weather'

    def test_mcp_tool_run(self):
        # Test MCP Tool with an example configuration
        mcp_result = self.mcp_tool.run({"tool_name": "restful", "tool_input": {"url": "https://jsonplaceholder.typicode.com/users", "method": "GET"}})
        self.assertTrue(mcp_result[0])  # Check that MCP tool returns True as success
        self.assertIn("data", mcp_result[1])  # Assuming the response contains 'data' field

if __name__ == "__main__":
    unittest.main()
