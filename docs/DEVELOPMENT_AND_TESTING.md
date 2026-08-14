# Development, Testing & Contribution Guide

This document provides instructions for developers contributing to or extending **random_vISA**.

---

## 🛠 Prerequisites & Setup

```bash
# Clone and enter directory
cd /Volumes/External/Code/random_vISA

# Install dependencies in editable mode
python3 -m pip install -e .
```

Required tools:
- Python $\ge$ 3.10
- `clang++` (or `g++` with C++20 support)
- `antlr4` ($\ge$ 4.13)
- Python packages: `jinja2`, `rich`, `antlr4-python3-runtime`, `pytest`

---

## 🧪 Running Tests

Run the complete test suite with `pytest`:

```bash
python3 -m pytest -v
```

### Test Suite Structure:
- `tests/unit/test_domain_models.py`: Validates `VectorConfig` invariants, power-of-2 checks, encoding/decoding bitwise packing, and aggregate collision detection.
- `tests/unit/test_random_generator.py`: Verifies deterministic generation via seeds, instruction count compliance, and unique encoding guarantees.
- `tests/unit/test_sail_antlr_parser.py`: Verifies ANTLR4 lexing, parsing, and AST reconstruction.
- `tests/integration/test_full_pipeline.py`: Tests the complete loop (Synthesis $\to$ Sail $\to$ C++ $\to$ Clang++ build $\to$ execution verification).

---

## ➕ Adding New Vector Instructions or Operations

### 1. Register in Domain Model
Add the operator to [`random_visa/domain/model/types.py`](file:///Volumes/External/Code/random_vISA/random_visa/domain/model/types.py):
```python
class BinaryOp(Enum):
    # ...
    DOT_PRODUCT = "dot"
```

### 2. Add to Generator Pool
Update [`random_visa/domain/services/random_generator.py`](file:///Volumes/External/Code/random_vISA/random_visa/domain/services/random_generator.py):
```python
AVAILABLE_BINARY_OPS = [
    # ...
    (BinaryOp.DOT_PRODUCT, "dot", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
]
```

### 3. Update C++ Generator Template
Add the execution case in [`random_visa/adapters/outbound/cpp_codegen/cpp_emitter_adapter.py`](file:///Volumes/External/Code/random_vISA/random_visa/adapters/outbound/cpp_codegen/cpp_emitter_adapter.py):
```jinja2
{% elif inst.binary_op.name == "DOT_PRODUCT" %}
    result = op2 * op1; // custom SIMD dot-product logic
```

### 4. Regenerate ANTLR4 Grammar (if grammar modified)
```bash
antlr4 -Dlanguage=Python3 -visitor -o random_visa/adapters/inbound/parser/antlr random_visa/adapters/inbound/parser/antlr/Sail.g4
```
