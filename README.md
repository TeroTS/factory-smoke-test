# factory-smoke-test

Dependency-free calculator fixture for the software factory PoC. It provides
`calculator.py:add(a, b)` and `multiply(a, b)`, with standard-library tests for
positive, negative, and zero operands.

## Verify

Requires Docker Engine and modern Docker Compose supporting `up --wait`.
No Python package installation is needed. From this repository's root:

```sh
sh scripts/setup
sh scripts/verify
```

`scripts/verify` builds and starts the calculator HTTP API, waits for health,
then runs unit and integration tests once in a non-root test container. The
integration tests cover service-name DNS, HTTP arithmetic and invalid inputs,
SQLite writes on a named volume, and a writable checkout bind mount. The HTTP
fixture exposes addition; unit tests cover both addition and multiplication.

A cleanup trap removes the stack's containers, network, and SQLite volume on
success or failure. The first run needs internet access to pull the Python image;
build images/cache are retained. Run one verification at a time per Compose
project. No host ports are published.

For Docker-free unit tests, including verification-script failure checks:

```sh
python3 -m unittest discover -s tests -v
```

Run `scripts/verify` as `factory` inside the VM/Codex execution path to test nested
Docker. Local success alone does not establish MicroVM or sandbox support.
This smoke test does not check host-port access, persistence after recreation,
a separate database server, or production security.
