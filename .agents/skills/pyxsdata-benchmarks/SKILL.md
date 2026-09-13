---
name: pyxsdata-benchmarks
description: >-
  Use this skill when running performance benchmarks, profiling XML parsers and
  serializers, comparing PolyXML (Rust), pugixml, lxml, and native handlers, or
  investigating throughput regressions.
---

# Pyxsdata Performance Benchmarking & Profiling

This skill describes how to run and analyze performance benchmarks in `pyxsdata`.

## 1. Handlers Under Benchmark

`pyxsdata` supports four distinct XML parsing backends:

| Backend     | Handler               | Implementation   | Throughput (est.) | Primary Advantage                |
| :---------- | :-------------------- | :--------------- | :---------------- | :------------------------------- |
| **PolyXML** | `CoreXmlParser`       | Pure Rust 2021   | ~310,000 obj/s    | Zero-allocation token streaming  |
| **pugixml** | `PugixmlEventHandler` | Cython + C++     | ~140,000 obj/s    | Minimal memory footprint         |
| **lxml**    | `LxmlEventHandler`    | Cython + libxml2 | ~85,000 obj/s     | Full XPath & DTD entity features |
| **native**  | `XmlEventHandler`     | Pure Python      | ~40,000 obj/s     | No compiled C/Rust dependencies  |

## 2. Running Benchmarks

Always run benchmarks in an isolated environment with consistent CPU frequency:

```bash
# Ensure virtualenv binaries are in PATH
PATH="$PWD/.venv/bin:$PATH"

# Run all parser & serializer benchmarks
.venv/bin/pytest tests/integration/benchmarks/ --benchmark-only

# Run a specific benchmark suite (e.g. handlers comparison)
.venv/bin/pytest tests/integration/benchmarks/test_handlers.py --benchmark-only --benchmark-sort=mean

# Save benchmark results to JSON for regression tracking
.venv/bin/pytest tests/integration/benchmarks/ --benchmark-only --benchmark-json=benchmark_results.json
```

## 3. Standalone Benchmark Script

For quick ad-hoc benchmark runs against the book catalog fixture:

```bash
.venv/bin/python benchmark.py
```

## 4. Profiling Memory and CPU

To profile hot paths and allocations:

```bash
# Using cProfile for CPU bottlenecks
.venv/bin/python -m cProfile -s cumtime benchmark.py | head -n 35

# Using memray for heap allocations (if installed)
uv run memray run benchmark.py
uv run memray summary memray-*.bin
```
