# CLI Command Reference (`visa-gen`)

Comprehensive reference and parameter matrix for the `visa-gen` command-line interface.

---

## 📋 1. Commands Overview Matrix Table

| Command | Inbound Port Invoked | Input Parameters | Output Artifacts | Compiles C++? | Description |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`pipeline`** | `RunPipelinePort` | Name, `num-insts`, `vlen`, `seed`, `out-dir`, flags | `.sail`, `.hpp`, `.cpp`, `CMakeLists.txt`, binary | Yes (configurable via `--no-compile`) | Executes end-to-end synthesis, Sail export, C++ emission, Clang++ compilation, and test execution |
| **`synthesize`** | `GenerateSpecPort`, `SailSpecWriterPort` | Name, `num-insts`, `vlen`, `seed`, `out-file` | `.sail` formal specification file | No | Synthesizes a formal Sail V-ISA specification and saves to disk |
| **`parse`** | `SailParserPort` | Path to `.sail` file, `name` | In-memory AST, terminal table summary | No | Parses any `.sail` file using ANTLR4 and prints instruction layout |
| **`compile-sail`** | `SailParserPort`, `CppCodeEmitterPort`, `CompilerRunnerPort` | Path to `.sail` file, `out-dir`, flags | C++ project files, verification binary | Yes (configurable via `--no-compile`) | Parses an existing `.sail` file directly and compiles it into a runnable C++ emulator |

---

## ⚙️ 2. Detailed Options & Flags Matrix Table

| Option Name | Short Flag | Applicable Commands | Type | Default Value | Valid Range / Constraints | Detailed Description |
| :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| `--name` | — | `pipeline`, `synthesize`, `parse`, `compile-sail` | `str` | `RVV_Random_ISA` | Valid identifier `[A-Za-z0-9_]+` | Unique name of the synthesized or parsed Vector ISA architecture |
| `--num-insts` | `-n` | `pipeline`, `synthesize` | `int` | `12` | $1 \le n \le 512$ | Number of randomized vector instructions to synthesize |
| `--vlen` | — | `pipeline`, `synthesize` | `int` | `128` | Power of 2 $\ge 64$ ($64, 128, 256, 512, 1024, 2048, 4096, 8192$) | Vector register bitwidth ($VLEN$) for vector state allocation |
| `--seed` | — | `pipeline`, `synthesize` | `int` | `42` | Any 32-bit/64-bit integer | Randomization seed for 100% deterministic and reproducible spec synthesis |
| `--out-dir` | `-o` | `pipeline`, `compile-sail` | `path` | `generated_emulator` | Writable directory path | Directory where C++ emulator headers, sources, and CMake files are written |
| `--out-file` | `-o` | `synthesize` | `path` | `<name>.sail` | Writable file path ending in `.sail` | Destination file path for generated Sail formal specification |
| `--no-compile`| — | `pipeline`, `compile-sail` | `bool` | `False` | Flag (presence activates) | Skips `clang++` compilation and test runner execution |
| `--help` | `-h` | All commands | `bool` | — | Flag | Displays command-line syntax, argument help, and exit |

---

## 🚥 3. CLI Exit Codes & Error Scenarios Matrix

| Exit Code | Status | Meaning | Typical Trigger | Recovery Action |
| :---: | :---: | :--- | :--- | :--- |
| **`0`** | `SUCCESS` | Pipeline / command completed successfully | All instructions synthesized, compiled, and all verification tests passed | Process generated artifacts in target directory |
| **`1`** | `FAILURE` | Compilation or verification failure | Clang++ compilation error, missing C++20 compiler, or test vector mismatch | Inspect compiler stderr or test logs |
| **`1`** | `FILE_NOT_FOUND` | Specified `.sail` file does not exist | Invalid path passed to `parse` or `compile-sail` | Provide a valid path to an existing `.sail` file |
| **`2`** | `CLI_SYNTAX_ERROR` | Unknown command line argument or missing required parameter | Typos in CLI flags (e.g. `--num-inst` instead of `--num-insts`) | Check `--help` for syntax specifications |

---

## 💡 4. Common Execution Recipes

| Use Case Scenario | Command Line Invocation |
| :--- | :--- |
| **Standard V-ISA Demo** | `python3 -m random_visa.adapters.inbound.cli.main pipeline --name RVV_Standard -n 16 --vlen 128 --seed 100` |
| **Wide Vector Supercomputer (VLEN=512)** | `python3 -m random_visa.adapters.inbound.cli.main pipeline --name RVV_Wide_512 -n 24 --vlen 512 --out-dir supercomputer_emu` |
| **HPC Massive Vector (VLEN=2048)** | `python3 -m random_visa.adapters.inbound.cli.main pipeline --name RVV_HPC_2048 -n 32 --vlen 2048 --out-dir hpc_emu` |
| **Formal Sail Export Only** | `python3 -m random_visa.adapters.inbound.cli.main synthesize --name Custom_DSP -n 12 --vlen 256 -o dsp_spec.sail` |
| **Inspect Sail File with ANTLR4** | `python3 -m random_visa.adapters.inbound.cli.main parse dsp_spec.sail` |
| **Direct Sail to C++ Emulator Build** | `python3 -m random_visa.adapters.inbound.cli.main compile-sail dsp_spec.sail --out-dir dsp_emulator` |
