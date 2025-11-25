"""
Basic tests for Speech-to-Text Light application
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import io


class TestURLValidation:
    """Tests for URL detection and validation"""

    def test_looks_like_url_valid_https(self):
        """Test URL detection for valid HTTPS URLs"""
        from app import looks_like_url
        assert looks_like_url("https://example.com")
        assert looks_like_url("https://www.example.com/path")

    def test_looks_like_url_valid_http(self):
        """Test URL detection for valid HTTP URLs"""
        from app import looks_like_url
        assert looks_like_url("http://example.com")
        assert looks_like_url("http://test.org/page")

    def test_looks_like_url_invalid(self):
        """Test URL detection for non-URLs"""
        from app import looks_like_url
        assert not looks_like_url("plain text")
        assert not looks_like_url("example.com")
        assert not looks_like_url("just some words")

    def test_validate_public_url_localhost_blocked(self):
        """Test that localhost URLs are blocked"""
        from app import validate_public_url
        url, reason = validate_public_url("http://localhost:8080")
        assert url is None
        assert reason is not None
        assert "localhost" in reason.lower()

    def test_validate_public_url_invalid_scheme(self):
        """Test that non-HTTP(S) schemes are blocked"""
        from app import validate_public_url
        url, reason = validate_public_url("ftp://example.com")
        assert url is None
        assert "HTTP" in reason or "HTTPS" in reason


class TestFileProcessing:
    """Tests for file processing utilities"""

    def test_extract_text_from_plain(self):
        """Test plain text extraction"""
        from app import extract_text_from_plain
        test_text = "Hello, world!"
        file_stream = io.BytesIO(test_text.encode('utf-8'))
        result = extract_text_from_plain(file_stream)
        assert result == test_text

    def test_extract_text_from_plain_utf8_errors(self):
        """Test plain text extraction with encoding errors"""
        from app import extract_text_from_plain
        # Invalid UTF-8 byte sequence
        file_stream = io.BytesIO(b'\xff\xfe invalid')
        result = extract_text_from_plain(file_stream)
        # Should not raise exception, handles errors gracefully
        assert isinstance(result, str)


class TestApplicationStructure:
    """Tests for Flask application structure"""

    def test_flask_app_exists(self):
        """Test that Flask app is created"""
        from app import app
        assert app is not None
        assert app.name == 'app'

    def test_routes_exist(self):
        """Test that required routes are defined"""
        from app import app
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        assert '/' in routes
        assert '/api/process' in routes
        assert '/api/voice' in routes


class TestConstants:
    """Tests for application constants"""

    def test_model_names_defined(self):
        """Test that AI model names are defined"""
        from app import TTS_MODEL, STT_MODEL, LLM_MODEL
        assert TTS_MODEL is not None
        assert STT_MODEL is not None
        assert LLM_MODEL is not None
        assert isinstance(TTS_MODEL, str)
        assert isinstance(STT_MODEL, str)
        assert isinstance(LLM_MODEL, str)

    def test_url_fetch_timeout_defined(self):
        """Test that URL fetch timeout is defined"""
        from app import URL_FETCH_TIMEOUT
        assert URL_FETCH_TIMEOUT > 0
        assert isinstance(URL_FETCH_TIMEOUT, int)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
