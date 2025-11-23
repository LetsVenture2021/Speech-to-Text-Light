"""Basic tests for the Speech-to-Text application."""
import os
import pytest


@pytest.fixture(autouse=True)
def set_openai_key():
    """Set a dummy OpenAI key for testing."""
    original_key = os.environ.get('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = 'sk-test-dummy-key-for-testing'
    yield
    if original_key:
        os.environ['OPENAI_API_KEY'] = original_key
    else:
        os.environ.pop('OPENAI_API_KEY', None)


def test_import_app():
    """Test that app module can be imported."""
    import app
    assert app is not None


def test_flask_app_exists():
    """Test that Flask app is created."""
    from app import app as flask_app
    assert flask_app is not None
    assert flask_app.name == 'app'


def test_routes_exist():
    """Test that expected routes are registered."""
    from app import app as flask_app

    # Get all registered routes
    routes = [str(rule) for rule in flask_app.url_map.iter_rules()]

    # Check that key routes exist
    assert '/' in routes
    assert '/api/process' in routes
    assert '/api/voice' in routes
