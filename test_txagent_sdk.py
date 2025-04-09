
import unittest
from TxAgentSDK import TxAgentSDK

class TestTxAgentSDK(unittest.TestCase):
    def setUp(self):
        # Set up the SDK instance
        self.sdk = TxAgentSDK(model_name="TxAgent-T1", rag_model_name="mims-harvard/ToolRAG-T1-GTE-Qwen2-1.5B")

    def test_run_query(self):
        # Test that running a valid query returns a result
        query = "What is the dosage for a 70kg adult with moderate renal impairment taking drug X?"
        result = self.sdk.run_query(query)
        self.assertIn("answer", result)
        self.assertIn("reasoning", result)

    def test_invalid_query(self):
        # Test that an invalid query returns a default response
        invalid_query = ""
        result = self.sdk.run_query(invalid_query)
        self.assertEqual(result["answer"], "(No answer returned)")

if __name__ == '__main__':
    unittest.main()
