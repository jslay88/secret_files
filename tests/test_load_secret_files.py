import logging
import os
from pathlib import Path

from secret_files.methods import load_secret_files


# Set log level to DEBUG as tests are dependent on checking debug output
logging.getLogger("secret_files.methods").setLevel(logging.DEBUG)


def test_secrets_dir_env_var(caplog, monkeypatch):
    monkeypatch.setenv("SECRETS_DIR", "/this/is/a/test")
    load_secret_files()
    assert "secrets_dir: /this/is/a/test" in caplog.text


def test_path_arg(caplog):
    path = Path("/this/is/a/test")
    load_secret_files(path)
    assert "secrets_dir: /this/is/a/test" in caplog.text


def test_string_arg(caplog):
    path = "/this/is/a/test"
    load_secret_files(path)
    assert "secrets_dir: /this/is/a/test" in caplog.text


def test_not_a_directory(caplog, secrets_dir):
    secrets_dir, _, _ = secrets_dir
    load_secret_files(secrets_dir.join("definitely-not-a-dir"))
    assert "not a directory" in caplog.text


def test_follow_symlink(monkeypatch, secrets_dir):
    monkeypatch.setenv("SECRETS_FOLLOW_SYMLINKS", "True")
    secrets_dir, _, links = secrets_dir
    load_secret_files()
    for link, secret_path in links:
        assert os.path.basename(link) in os.environ.keys()
        with open(secrets_dir.join(secret_path)) as f:
            assert os.getenv(os.path.basename(link)) == f.read().strip()


def test_ignore_symlink(caplog, monkeypatch, secrets_dir):
    _, _, links = secrets_dir
    load_secret_files()
    assert all(link not in os.environ.keys() for link, _ in links)
    assert all(f"{link} is symlink" in caplog.text for link, _ in links)


def test_load_secret_files(secrets_dir):
    secrets_dir, secrets, _ = secrets_dir
    load_secret_files()
    for path, secret in secrets:
        assert os.path.basename(path) in os.environ.keys()
        with open(secrets_dir.join(path)) as f:
            assert (
                os.getenv(os.path.basename(path)) == f.read().strip() == secret
            )
