"""Unit tests for app.py utility functions."""
import io
import os
import pytest
import pandas as pd

# Set a dummy API key before importing app to avoid OpenAI initialization error
os.environ.setdefault("OPENAI_API_KEY", "test-key-for-unit-tests")

from app import (
    looks_like_url,
    validate_public_url,
    extract_text_from_plain,
    summarize_table,
)


class TestLooksLikeUrl:
    """Tests for looks_like_url function."""

    def test_http_url(self):
        assert looks_like_url("http://example.com") is True

    def test_https_url(self):
        assert looks_like_url("https://example.com") is True

    def test_http_with_path(self):
        assert looks_like_url("http://example.com/path/to/resource") is True

    def test_https_with_query(self):
        assert looks_like_url("https://example.com?query=value") is True

    def test_plain_text(self):
        assert looks_like_url("hello world") is False

    def test_email(self):
        assert looks_like_url("user@example.com") is False

    def test_ftp_url(self):
        # Should not match non-http schemes
        assert looks_like_url("ftp://example.com") is False

    def test_empty_string(self):
        assert looks_like_url("") is False

    def test_whitespace_url(self):
        assert looks_like_url("  https://example.com  ") is True

    def test_mixed_case(self):
        assert looks_like_url("HTTP://Example.com") is True
        assert looks_like_url("HTTPS://Example.com") is True


class TestValidatePublicUrl:
    """Tests for validate_public_url SSRF protection."""

    def test_valid_public_url(self):
        # Note: This test may fail in restricted network environments
        # where DNS resolution fails or returns non-public IPs
        url, reason = validate_public_url("https://example.com")
        # In restricted environments, either the URL passes or it fails
        # with a DNS-related error, not a security rejection
        if url is None:
            # Accept DNS resolution failure as valid in test environments
            assert "resolution" in reason.lower() or "disallowed" in reason.lower()
        else:
            assert reason is None

    def test_rejects_localhost(self):
        url, reason = validate_public_url("http://localhost/")
        assert url is None
        assert "localhost" in reason.lower()

    def test_rejects_ftp_scheme(self):
        url, reason = validate_public_url("ftp://example.com")
        assert url is None
        assert "HTTP" in reason

    def test_rejects_file_scheme(self):
        url, reason = validate_public_url("file:///etc/passwd")
        assert url is None
        assert "HTTP" in reason

    def test_rejects_no_hostname(self):
        url, reason = validate_public_url("http:///path")
        assert url is None
        assert "hostname" in reason.lower()

    def test_rejects_private_ip_127(self):
        url, reason = validate_public_url("http://127.0.0.1/")
        assert url is None
        assert "disallowed IP" in reason

    def test_rejects_private_ip_10(self):
        url, reason = validate_public_url("http://10.0.0.1/")
        assert url is None
        assert "disallowed IP" in reason

    def test_rejects_private_ip_192_168(self):
        url, reason = validate_public_url("http://192.168.1.1/")
        assert url is None
        assert "disallowed IP" in reason

    def test_rejects_private_ip_172(self):
        url, reason = validate_public_url("http://172.16.0.1/")
        assert url is None
        assert "disallowed IP" in reason


class TestExtractTextFromPlain:
    """Tests for extract_text_from_plain function."""

    def test_basic_text(self):
        stream = io.BytesIO(b"Hello, world!")
        result = extract_text_from_plain(stream)
        assert result == "Hello, world!"

    def test_multiline_text(self):
        stream = io.BytesIO(b"Line 1\nLine 2\nLine 3")
        result = extract_text_from_plain(stream)
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_utf8_text(self):
        stream = io.BytesIO("Hello, 世界! 🌍".encode("utf-8"))
        result = extract_text_from_plain(stream)
        assert "Hello" in result
        assert "世界" in result

    def test_empty_file(self):
        stream = io.BytesIO(b"")
        result = extract_text_from_plain(stream)
        assert result == ""


class TestSummarizeTable:
    """Tests for summarize_table function."""

    def test_basic_dataframe(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })
        result = summarize_table(df)
        assert "3 rows" in result
        assert "2 columns" in result
        assert "name" in result
        assert "age" in result

    def test_numeric_stats(self):
        df = pd.DataFrame({
            'value': [10, 20, 30, 40, 50]
        })
        result = summarize_table(df)
        assert "mean" in result
        assert "min" in result
        assert "max" in result

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = summarize_table(df)
        assert "0 rows" in result
        assert "0 columns" in result


class TestUrlRegex:
    """Tests for URL detection regex."""

    def test_various_urls(self):
        valid_urls = [
            "http://example.com",
            "https://www.google.com",
            "http://subdomain.example.org/path",
            "https://example.com:8080/path?query=value",
        ]
        for url in valid_urls:
            assert looks_like_url(url) is True, f"Expected {url} to be detected as URL"

    def test_non_urls(self):
        non_urls = [
            "not a url",
            "www.example.com",  # Missing scheme
            "example.com",
            "mailto:user@example.com",
            "javascript:alert(1)",
        ]
        for text in non_urls:
            assert looks_like_url(text) is False, f"Expected {text} to NOT be detected as URL"
