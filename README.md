# Secret Files
![Python](https://github.com/jslay88/secret_files/actions/workflows/python.yml/badge.svg)

As file based secrets have become a more common place with technologies
like Kubernetes, a better approach to more common patterns for Python is
needed. This project aims to serve that purpose

* [Theory](#Theory)
* [Installation](#Installation)
* [Contributing](#Contributing)

## Theory
Kubernetes and other applications place file based secrets under
`/var/run/secrets`. As most apps are designed in 12 factor app manner,
they are usually targeting environment variables. This Python module
attempts to bridge the gap between file based secrets and environment
variables by traversing a specified directory, using the filename as
the environment variable name, and the contents of the file as the
environment variable value. This happens only within the Python runtime,
and not within the executing shell/environment. Python applications can
explicitly load secrets at a desired time or from multiple specified
directories. These can then be accessed via `os.getenv`. A secrets directory
can also be specified via `SECRETS_DIR` environment variable.

```bash
$ export SECRETS_DIR="$(mktemp -d)"
$ echo -n "test-secret" > "$SECRETS_DIR/TEST_SECRET"
$ python - <<EOF
import os
from secret_files import load_secret_files
load_secret_files()
print(os.getenv('TEST_SECRET'))
EOF
test-secret
```

## Installation

### Pip Install from PyPi
Recommended method is installation via `pip` from PyPi.

```bash
pip install secret-files
```

### Pip install from GitHub
You can also install via `pip` from GitHub

```bash
pip install git+https://github.com/jslay88/secret_files
```

### Cloning/Installing from source
Obtain a copy of the source via `git clone` or downloading from GitHub.
Then you can pip install from the directory.

```bash
pip install .
```

## Usage
Have some secrets in a directory, import the method and point it to the
directory when you call it. Then access the values from `os.getenv` or
`os.environ`.

Example has a file `MY_SECRET` in `/my/secret/dir`, with the
value `my-secret`.

```Python
import os

from secret_files import load_secret_files


load_secret_files('/my/secret/dir')
print(os.getenv('MY_SECRET'))
"my-secret"
```

## Contributing
All PRs welcome, especially those that increase security, address
additional use cases, or add features. Some initial ideas that come
to mind:
* Other options outside of environment variables
* Secret store object that could handle encrypted secret files
and decrypt from disk instead of store in memory.
* Integrations into secret providers.
* Kubernetes API support
