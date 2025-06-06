"""Test configuration and fixtures."""

import os

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def pytest_configure(config):
    """Configure test environment."""
    # Register custom marks
    config.addinivalue_line(
        "markers", "integration: mark a test as an integration test"
    )
    config.addinivalue_line("markers", "slow: mark a test as a slow-running test")
    config.addinivalue_line(
        "markers", "requires_api_key: mark a test as requiring an API key"
    )


def pytest_collection_modifyitems(config, items):
    """Modify collected test items based on environment conditions."""
    # Check for API key presence - don't skip tests as we have the API key
    api_key_missing = not os.getenv("OPENROUTER_API_KEY")

    # Print a message about the API key status for debugging
    if api_key_missing:
        print("WARNING: OPENROUTER_API_KEY not found in environment.")
    else:
        print(
            f"INFO: OPENROUTER_API_KEY found in environment (length: {len(os.getenv('OPENROUTER_API_KEY'))})"
        )

    # Only skip tests if API key is actually missing
    if api_key_missing:
        skip_marker = pytest.mark.skip(
            reason="OPENROUTER_API_KEY environment variable not set. "
            "Please set it to run integration tests."
        )
        for item in items:
            # Skip tests marked with 'integration' or 'requires_api_key'
            if any(
                mark in item.keywords for mark in ["integration", "requires_api_key"]
            ):
                item.add_marker(skip_marker)
