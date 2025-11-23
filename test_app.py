"""
Basic tests for the Speech-to-Text Light application.
These tests verify core functionality without requiring API keys.
"""

import pytest
from app import (
    looks_like_url,
    extract_text_from_plain,
    summarize_table,
)
import io
import pandas as pd


class TestURLDetection:
    """Test URL detection utility"""

    def test_valid_http_url(self):
        """Test that valid HTTP URLs are detected"""
        assert looks_like_url("http://example.com")

    def test_valid_https_url(self):
        """Test that valid HTTPS URLs are detected"""
        assert looks_like_url("https://example.com")

    def test_invalid_url(self):
        """Test that non-URLs are not detected"""
        assert not looks_like_url("not a url")
        assert not looks_like_url("ftp://example.com")

    def test_url_with_whitespace(self):
        """Test that URLs with surrounding whitespace are detected"""
        assert looks_like_url("  https://example.com  ")


class TestTextExtraction:
    """Test text extraction utilities"""

    def test_extract_plain_text(self):
        """Test plain text extraction"""
        test_text = "Hello, world!"
        stream = io.BytesIO(test_text.encode("utf-8"))
        result = extract_text_from_plain(stream)
        assert result == test_text

    def test_extract_plain_text_with_unicode(self):
        """Test plain text extraction with unicode characters"""
        test_text = "Hello, 世界! 🌍"
        stream = io.BytesIO(test_text.encode("utf-8"))
        result = extract_text_from_plain(stream)
        assert result == test_text


class TestTableSummarization:
    """Test table summarization"""

    def test_summarize_simple_table(self):
        """Test summarizing a simple pandas dataframe"""
        df = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6]
        })
        result = summarize_table(df)
        assert "3 rows x 2 columns" in result
        assert "col1" in result
        assert "col2" in result

    def test_summarize_table_with_numeric_stats(self):
        """Test that numeric statistics are included"""
        df = pd.DataFrame({
            "numbers": [10, 20, 30, 40, 50]
        })
        result = summarize_table(df)
        assert "mean" in result
        assert "min" in result
        assert "max" in result


class TestAppConfiguration:
    """Test application configuration"""

    def test_app_imports(self):
        """Test that the Flask app can be imported"""
        from app import app
        assert app is not None

    def test_routes_defined(self):
        """Test that expected routes are defined"""
        from app import app
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        assert "/" in routes
        assert "/api/process" in routes
        assert "/api/voice" in routes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
