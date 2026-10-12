# blankly: portable verification records

These records retain exact commands, outcomes, original-log hashes and available source snapshots. Failed, interrupted and earlier exploratory commands remain visible. A later focused pass proves only its own scope.

[Machine-readable records](verification.json) · [Validation](../validation.md) · [Engineering guide](../ayu-develop.md)

Original logs remain in the workspace maintenance evidence. Tracked source hashes exclude untracked additions and later edits, as stated in each captured snapshot.

| Check | Exit | Duration | Command |
| --- | ---: | ---: | --- |
| blankly-build-final.log | 0 | 0.94s | `uv build --python 3.14` |
| blankly-build-selected-python.log | 0 | 2.44s | `uv build --python 3.15` |
| blankly-build.log | 0 | 1.03s | `uv build --python 3.14` |
| blankly-compile-final.log | 0 | 0.13s | `uv run --no-sync python -m compileall -q src` |
| blankly-compile-selected-python.log | 0 | 0.14s | `uv run --no-sync python -m compileall -q src` |
| blankly-compile.log | 0 | 0.13s | `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` |
| blankly-lock-3.14.log | 0 | 0.29s | `uv lock --upgrade --python 3.14` |
| blankly-lock-3.15.log | 0 | 0.56s | `uv lock --upgrade --python 3.15` |
| blankly-lock-python315-source-supported.log | 0 | 0.61s | `uv lock --upgrade --python 3.15` |
| build | 0 | 0.5s | `uv build --python 3.15.0` |
| compile | 0 | 0.04s | `.venv/bin/python -Werror -m compileall -q src` |
| full-tests | 1 | 1.04s | `.venv/bin/python -m pytest --continue-on-collection-errors --tb=short` |
| lock-check | 0 | 0.02s | `uv lock --check` |
| pure-tests | 0 | 0.97s | `.venv/bin/python -m pytest tests/indicators tests/metrics --tb=short` |
| sync | 0 | 0.39s | `uv sync --all-extras --all-groups --frozen --python 3.15.0` |
| blankly-python315-source-probe.log | 0 | 3.88s | `uv sync --directory /tmp/trading-python315-probes/blankly --all-extras --all-groups --python 3.15` |
| blankly-sync-3.14.log | 0 | 0.62s | `uv sync --all-extras --all-groups --python 3.14` |
| blankly-sync-python315-source-supported.log | 0 | 1.83s | `uv sync --all-extras --all-groups --python 3.15` |
| blankly-tests-python315-source-supported.log | 2 | unknowns | `uv run --no-sync python -m pytest` |
| blankly-tests.log | 2 | 4.68s | `uv run --no-sync python -m pytest` |
| blankly-versions-final.log | 0 | 0.13s | `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]:d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` |
| blankly-wheel-probe-3.14.log | 2 | 0.05s | `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` |
| blankly-wheel-probe-3.15.log | 2 | 0.61s | `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` |
