# Validation evidence: blankly

Run date: 2026-10-12. Branch: `feature/ayu_develop`. Interpreter: `3.15.0 (main, Oct  9 2026, 15:11:47) [Clang 22.1.3 ]`.

| Check | Result |
|---|---|
| lock | passed |
| sync | passed |
| compile | passed |
| build | passed |
| tests | failed |

## Current result and compatibility decisions

- The full pytest suite is attempted without changing discovery. Live exchange test collection reads missing Keys.json and cannot proceed without the original credential setup.
- The retained Alpaca SDK requires msgpack==1.0.3; that exact compatible pin is preserved instead of forcing a contradictory latest major.
- Python 3.15 actual installation succeeds including source builds.

Current unresolved checks:

- tests: exit 2; see [docs/maintenance-2026-10-12/blankly-tests-python315-source-supported.log](../../docs/maintenance-2026-10-12/blankly-tests-python315-source-supported.log)

## Latest full-suite output

```text
$ uv run --no-sync python -m pytest
INFO: Live futures trading is untested due to US regulations - this prevents blankly developers from integrating with these exchanges. We are looking for someone who is interested in helping us create & test our integrations.
INFO: "auto_truncate" not specified in preferences, defaulting to: "False"
INFO: "global_shorting" not specified in preferences, defaulting to: "False"
INFO: "simulate_margin" not specified in preferences, defaulting to: "True"
INFO: "margin_type" not specified in preferences, defaulting to: "USDT-M"
INFO: "enable_shorting" not specified in preferences, defaulting to: "True"
INFO: "use_yfinance" not specified in preferences, defaulting to: "False"
INFO: "okx" not specified in preferences, defaulting to: "{'cash': 'USDT'}"
INFO: "keyless" not specified in preferences, defaulting to: "{'cash': 'USD'}"
INFO: "cash" not specified in preferences, defaulting to: "USD"
INFO: "paper" not specified in preferences, defaulting to: "{'price_source': 'api'}"
============================= test session starts ==============================
platform darwin -- Python 3.15.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/alex/workspaces/trading/blankly
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
testpaths: tests
plugins: mock-3.16.0
collected 63 items / 1 error

==================================== ERRORS ====================================
__________________ ERROR collecting tests/new_interface_tests __________________
src/blankly/exchanges/auth/utils.py:117: in load_json
    f = open(keys_file)
        ^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: './tests/config/keys.json'

During handling of the above exception, another exception occurred:
../../../.local/share/uv/python/cpython-3.15.0-macos-aarch64-none/lib/python3.15/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1390: in _gcd_import
    ???
<frozen importlib._bootstrap>:1350: in _find_and_load
    ???
<frozen importlib._bootstrap>:1309: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:915: in _load_unlocked
    ???
.venv/lib/python3.15/site-packages/_pytest/assertion/rewrite.py:188: in exec_module
    exec(co, module.__dict__)
tests/new_interface_tests/conftest.py:8: in <module>
    from tests.new_interface_tests.test_utils import FUTURES_EXCHANGES, get_symbols, SPOT_EXCHANGES
<frozen importlib._bootstrap>:1350: in _find_and_load
    ???
<frozen importlib._bootstrap>:1309: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:915: in _load_unlocked
    ???
.venv/lib/python3.15/site-packages/_pytest/assertion/rewrite.py:188: in exec_module
    exec(co, module.__dict__)
tests/new_interface_tests/test_utils.py:37: in <module>
    binance_futures = BinanceFutures(keys_path="./tests/config/keys.json",
src/blankly/exchanges/interfaces/binance_futures/binance_futures.py:35: in __init__
    auth = AuthConstructor(keys_path, portfolio_name, 'binance',
src/blankly/exchanges/auth/auth_constructor.py:40: in __init__
    self.portfolio_name, self.keys = load_auth(exchange, keys_file, portfolio_name)
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src/blankly/exchanges/auth/utils.py:57: in load_auth
    auth_object = load_json(keys_file)
                  ^^^^^^^^^^^^^^^^^^^^
src/blankly/exchanges/auth/utils.py:122: in load_json
    raise FileNotFoundError("Make sure a Keys.json file is placed in the same folder as the project working "
E   FileNotFoundError: Make sure a Keys.json file is placed in the same folder as the project working directory!
=========================== short test summary info ============================
ERROR tests/new_interface_tests - FileNotFoundError: Make sure a Keys.json fi...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 8.01s ===============================

```

## Exact commands and exit codes

Unsuccessful rows are retained as historical compatibility attempts; they are not claims that a current passing check remains blocked. Source-build probes use isolated temporary copies to preserve the selected repository environment.

| Command | Exit | Seconds | Evidence |
|---|---:|---:|---|
| `uv lock --upgrade --python 3.15` | 0 | 0.56 | [log](../../docs/maintenance-2026-10-12/blankly-lock-3.15.log) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 0.61 | [log](../../docs/maintenance-2026-10-12/blankly-wheel-probe-3.15.log) |
| `uv lock --upgrade --python 3.14` | 0 | 0.29 | [log](../../docs/maintenance-2026-10-12/blankly-lock-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 2 | 0.05 | [log](../../docs/maintenance-2026-10-12/blankly-wheel-probe-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 0.62 | [log](../../docs/maintenance-2026-10-12/blankly-sync-3.14.log) |
| `uv build --python 3.14` | 0 | 1.03 | [log](../../docs/maintenance-2026-10-12/blankly-build.log) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/blankly-compile.log) |
| `uv run --no-sync python -m pytest` | 2 | 4.68 | [log](../../docs/maintenance-2026-10-12/blankly-tests.log) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/blankly-compile-final.log) |
| `uv build --python 3.14` | 0 | 0.94 | [log](../../docs/maintenance-2026-10-12/blankly-build-final.log) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/blankly-versions-final.log) |
| `uv sync --directory /tmp/trading-python315-probes/blankly --all-extras --all-groups --python 3.15` | 0 | 3.88 | [log](../../docs/maintenance-2026-10-12/blankly-python315-source-probe.log) |
| `uv lock --upgrade --python 3.15` | 0 | 0.61 | [log](../../docs/maintenance-2026-10-12/blankly-lock-python315-source-supported.log) |
| `uv sync --all-extras --all-groups --python 3.15` | 0 | 1.83 | [log](../../docs/maintenance-2026-10-12/blankly-sync-python315-source-supported.log) |
| `uv run --no-sync python -m pytest` | 2 | 10.3 | [log](../../docs/maintenance-2026-10-12/blankly-tests-python315-source-supported.log) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.14 | [log](../../docs/maintenance-2026-10-12/blankly-compile-selected-python.log) |
| `uv build --python 3.15` | 0 | 2.44 | [log](../../docs/maintenance-2026-10-12/blankly-build-selected-python.log) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]:d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/blankly-versions-final.log) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [result](../../docs/maintenance-2026-10-12/blankly-result.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|
| `pytest-mock>=3.15.1` | `pytest-mock>=3.16.0` |

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.
