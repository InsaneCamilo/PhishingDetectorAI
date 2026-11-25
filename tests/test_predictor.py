import unittest
from app.predictor import normalize_url

class URLValidationTests(unittest.TestCase):
    def test_adds_https_when_scheme_missing(self):
        self.assertEqual(normalize_url("example.com"), "https://example.com")

    def test_keeps_https(self):
        self.assertEqual(normalize_url("https://example.com/login"), "https://example.com/login")

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            normalize_url("")

    def test_rejects_spaces(self):
        with self.assertRaises(ValueError):
            normalize_url("https://example.com/a b")

    def test_rejects_invalid_domain(self):
        with self.assertRaises(ValueError):
            normalize_url("https:///")

if __name__ == "__main__":
    unittest.main()
