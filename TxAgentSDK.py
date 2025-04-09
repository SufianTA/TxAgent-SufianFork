import os
from src.txagent import TxAgent

class TxAgentSDK:
    def __init__(self, model_name='TxAgent-T1', rag_model_name='mims-harvard/ToolRAG-T1-GTE-Qwen2-1.5B', **kwargs):
        self.model_name = model_name
        self.rag_model_name = rag_model_name
        self.kwargs = kwargs
        self.agent = TxAgent(model_name=self.model_name, rag_model_name=self.rag_model_name, **self.kwargs)

    def run_query(self, query, temperature=0.3, max_new_tokens=1024, max_rounds=20, enable_summary=False):
        """
        Runs a query using the configured TxAgent.
        Args:
        - query: The query string to send to the agent
        - temperature: Controls the randomness of the response
        - max_new_tokens: Limits the length of the response
        - max_rounds: Limits the number of reasoning rounds
        - enable_summary: Whether to enable summary mode for the response
        
        Returns:
        - A dictionary with the final answer and reasoning trace
        """
        result = self.agent.run(query, temperature=temperature, max_new_tokens=max_new_tokens, 
                                max_rounds=max_rounds, enable_summary=enable_summary, **self.kwargs)
        return result

    def get_agent(self):
        """Returns the agent instance."""
        return self.agent
