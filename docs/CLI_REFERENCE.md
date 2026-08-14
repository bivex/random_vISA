# CLI Command Reference (`visa-gen`)

Comprehensive guide for the `visa-gen` command-line interface.

---

## 📋 Commands Overview

| Command | Description |
| :--- | :--- |
| `pipeline` | Run full synthesis -> Sail export -> C++ generation -> compile & test verification |
| `synthesize` | Synthesize random Vector ISA and write `.sail` file only |
| `parse` | Parse an existing `.sail` file with ANTLR4 and display instruction table |
| `compile-sail` | Parse a `.sail` file with ANTLR4 and generate/run C++ emulator directly |

---

## 🔧 Command Details & Examples

### 1. `pipeline`
Runs the complete end-to-end workflow:
```bash
python3 -m random_visa.adapters.inbound.cli.main pipeline [OPTIONS]
```
**Options**:
- `--name TEXT`: Name of the ISA specification (default: `RVV_Random_ISA`).
- `-n, --num-insts INT`: Number of random instructions to generate (default: `12`).
- `--vlen INT`: Vector register length in bits (default: `128`).
- `--seed INT`: Randomization seed for reproducible generation (default: `42`).
- `-o, --out-dir PATH`: Directory for emitted files (default: `generated_emulator`).
- `--no-compile`: Skip C++ compilation and test execution.

---

### 2. `synthesize`
Generates a formal `.sail` specification file only:
```bash
python3 -m random_visa.adapters.inbound.cli.main synthesize \
  --name Custom_DSP_ISA \
  -n 16 \
  --vlen 256 \
  --seed 12345 \
  -o my_spec.sail
```

---

### 3. `parse`
Parses any Sail specification file with ANTLR4 and inspects instructions:
```bash
python3 -m random_visa.adapters.inbound.cli.main parse my_spec.sail
```

---

### 4. `compile-sail`
Parses an existing `.sail` specification file and compiles it into a C++ emulator:
```bash
python3 -m random_visa.adapters.inbound.cli.main compile-sail \
  my_spec.sail \
  --out-dir my_emulator
```
