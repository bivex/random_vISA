# ArchC Architecture Description Language (ADL) & SystemC Integration in random_vISA

## 1. Overview

[**ArchC**](http://www.archc.org) is an open-source Architecture Description Language (ADL) based on SystemC, developed at the University of Campinas (IC-UNICAMP).

`random_vISA` provides direct support for translating any synthesized or parsed Sail V-ISA specification into **ArchC 2.4.1 ADL models (`.ac` + `.isa` + `_isa.cpp`)** and compiling them into executable **SystemC cycle-level / behavioral simulators (`.x`)**.

---

## 2. Emitted ArchC Project Structure

When `compile-archc` is invoked, `ArchCEmitterAdapter` produces:

| File | Description |
| :--- | :--- |
| [`<model>.ac`](file:///Volumes/External/Code/random_vISA/generated_emulator/archc_emulator/parsed_archc_isa.ac) | Architectural resource description: memory (`ac_mem DM:512M`), register banks (`VRB:32`, `XRB:32`), endianness, and word size. |
| [`<model>.isa`](file:///Volumes/External/Code/random_vISA/generated_emulator/archc_emulator/parsed_archc_isa.isa) | Instruction set formats (`Type_VV`, `Type_VX`, `Type_VI`, `Type_MVV`), instruction definitions, and bitfield decode rules. |
| [`<model>_isa.cpp`](file:///Volumes/External/Code/random_vISA/generated_emulator/archc_emulator/parsed_archc_isa_isa.cpp) | Behavioral implementation in C++ for all synthesized vector instructions using SystemC/ArchC register accessors. |
| [`main.cpp`](file:///Volumes/External/Code/random_vISA/generated_emulator/archc_emulator/main.cpp) | SystemC `sc_main` runner initializing the processor model and running simulations. |
| [`build.sh`](file:///Volumes/External/Code/random_vISA/generated_emulator/archc_emulator/build.sh) | Automated build script that invokes `acsim` and compiles with `clang++` and SystemC. |

---

## 3. CLI Usage

### 3.1. Compile Sail to ArchC SystemC Simulator
```bash
python3 -m random_visa.adapters.inbound.cli.main compile-archc \
  generated_emulator/hypervector_isa.sail \
  -o generated_emulator/archc_emulator
```

### 3.2. Run SystemC Simulator
```bash
./generated_emulator/archc_emulator/parsed_archc_isa.x --help
```
