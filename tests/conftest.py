import os

import pytest


@pytest.fixture(scope="session")
def _secrets_dir(tmpdir_factory):
    # Internal fixture to separate scope from session and function
    # as os.environ needs to be reset after each test, but we
    # don't need to keep recreating secrets
    secrets = [
        ("test-app-1/lowercase_name", "lowercase_name_secret"),
        ("test-app-1/UPPERCASE_NAME", "uppercase_name_secret"),
    ]
    links = [
        ("lowercase_link", "test-app-1/lowercase_name"),
        ("UPPERCASE_LINK", "test-app-1/UPPERCASE_NAME"),
    ]
    # Use a tmp directory
    tmp_dir = tmpdir_factory.mktemp("secrets")
    # Create secrets in the tmp directory
    for path, secret in secrets:
        if os.path.dirname(path) and not os.path.isdir(
            tmp_dir.join(os.path.dirname(path))
        ):
            os.makedirs(tmp_dir.join(os.path.dirname(path)))
        with open(tmp_dir.join(path), "w") as f:
            f.write(secret)
    # Create some link secrets
    for link, secret_path in links:
        os.symlink(tmp_dir.join(secret_path), tmp_dir.join(link))
    return tmp_dir, secrets, links


@pytest.fixture
def secrets_dir(_secrets_dir, monkeypatch):
    tmp_dir, secrets, links = _secrets_dir
    # Set SECRETS_DIR to tmp_dir path to set path for module globally
    monkeypatch.setenv("SECRETS_DIR", tmp_dir.strpath)
    yield tmp_dir, secrets, links
    # Clean out any secrets that got loaded for next function test
    for path, _ in secrets + links:
        os.environ.pop(os.path.basename(path), None)
