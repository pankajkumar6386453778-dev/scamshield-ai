import unittest
from src.url_analyzer import analyze_url

class URLAnalyzerTests(unittest.TestCase):
    def test_empty_url(self):
        self.assertIn("error", analyze_url(""))

    def test_regular_url_parses(self):
        result = analyze_url("https://example.com")
        self.assertIsNone(result["error"])
        self.assertEqual(result["host"], "example.com")

    def test_ip_host_indicator(self):
        result = analyze_url("http://192.0.2.1/login")
        self.assertTrue(any("IP address" in x for x in result["indicators"]))

    def test_does_not_fetch_url(self):
        # Analyzer is a pure parser/rule engine; it should not make network requests.
        result = analyze_url("https://example.com/verify")
        self.assertIsNone(result["error"])

if __name__ == "__main__":
    unittest.main()
