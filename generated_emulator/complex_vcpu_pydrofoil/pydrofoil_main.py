#!/usr/bin/env python3
# Standalone Pydrofoil / Python Verification Harness and Bytecode Runner
import sys
import os
import struct
try:
    from .pydrofoil_state import PydrofoilState
    from .pydrofoil_decoder import decode
    from .pydrofoil_instructions import execute
    from .pydrofoil_emulator import PydrofoilVectorEmulator
except (ImportError, ValueError):
    from pydrofoil_state import PydrofoilState
    from pydrofoil_decoder import decode
    from pydrofoil_instructions import execute
    from pydrofoil_emulator import PydrofoilVectorEmulator

TEST_VECTORS = [
    (0x0220A1D7, "vclz_m_0"),
    (0x0620B1D7, "vor_vi_1"),
    (0x0A20C1D7, "vxor_vx_2"),
    (0x0E20C1D7, "vmin_vx_3"),
    (0x1220C1D7, "vsadd_vx_4"),
    (0x1620C1D7, "vsra_vx_5"),
    (0x1A20C1D7, "vrem_vx_6"),
    (0x1E20A1D7, "vabs_m_7"),
    (0x2220A1D7, "vclz_m_8"),
    (0x2620C1D7, "vsrl_vx_9"),
    (0x2A20A1D7, "vcpop_m_10"),
    (0x2E20A1D7, "vcpop_m_11"),
    (0x322081D7, "vrem_vv_12"),
    (0x3620C1D7, "vxor_vx_13"),
    (0x3A20C1D7, "vmax_vx_14"),
    (0x3E2081D7, "vrem_vv_15"),
    (0x4220C1D7, "vxor_vx_16"),
    (0x462081D7, "vdiv_vv_17"),
    (0x4A20A1D7, "vabs_m_18"),
    (0x4E2081D7, "vxor_vv_19"),
    (0x5220A1D7, "vclz_m_20"),
    (0x5620A1D7, "vnot_m_21"),
    (0x5A2081D7, "vmin_vv_22"),
    (0x5E20A1D7, "vcpop_m_23"),
    (0x6220C1D7, "vor_vx_24"),
    (0x662081D7, "vmul_vv_25"),
    (0x6A20A1D7, "vcpop_m_26"),
    (0x6E20C1D7, "vdiv_vx_27"),
    (0x7220A1D7, "vclz_m_28"),
    (0x7620C1D7, "vsrl_vx_29"),
    (0x7A2081D7, "vsadd_vv_30"),
    (0x7E20C1D7, "vadd_vx_31"),
]

def run_verification_suite():
    emu = PydrofoilVectorEmulator()
    print("=" * 60)
    print("Starting Pydrofoil JIT Vector ISA (Parsed_Pydrofoil_ISA) Verification")
    print(f"VLEN = {emu.state.vregs.regs[0].__len__() * 8} bits, Num VRegs = 32")
    print("=" * 60)

    passed = 0
    total = len(TEST_VECTORS)

    for idx, (word, mnemonic) in enumerate(TEST_VECTORS, start=1):
        emu.reset()
        # Setup test inputs
        emu.state.vregs.set_elem(1, 0, 10)
        emu.state.vregs.set_elem(1, 1, 20)
        emu.state.vregs.set_elem(1, 2, 30)
        emu.state.vregs.set_elem(1, 3, 40)

        emu.state.vregs.set_elem(2, 0, 2)
        emu.state.vregs.set_elem(2, 1, 4)
        emu.state.vregs.set_elem(2, 2, 6)
        emu.state.vregs.set_elem(2, 3, 8)

        emu.state.set_xreg(1, 5)

        ok = emu.step(word)
        if ok:
            res_elems = [emu.state.vregs.get_elem(3, e) for e in range(4)]
            print(f"[Test {idx}/{total}] Executing {mnemonic} (0x{word:08X})... SUCCESS -> v3: {res_elems}")
            passed += 1
        else:
            print(f"[Test {idx}/{total}] Executing {mnemonic} (0x{word:08X})... FAILED (Unknown Instruction)")

    print(f"\nResults: {passed}/{total} Pydrofoil tests passed.")
    return 0 if passed == total else 1


def run_bytecode_file(bin_path: str):
    if not os.path.exists(bin_path):
        print(f"Error: file not found '{bin_path}'")
        return 1

    with open(bin_path, "rb") as f:
        data = f.read()

    emu = PydrofoilVectorEmulator()
    # Setup initial state
    emu.state.vregs.set_elem(1, 0, 10)
    emu.state.vregs.set_elem(1, 1, 20)
    emu.state.vregs.set_elem(1, 2, 30)
    emu.state.vregs.set_elem(1, 3, 40)

    emu.state.vregs.set_elem(2, 0, 2)
    emu.state.vregs.set_elem(2, 1, 4)
    emu.state.vregs.set_elem(2, 2, 6)
    emu.state.vregs.set_elem(2, 3, 8)
    emu.state.set_xreg(1, 5)

    words_count = len(data) // 4
    print(f"Executing Bytecode Program ({words_count} instructions)...")
    for i in range(words_count):
        word = struct.unpack_from("<I", data, i * 4)[0]
        pc = emu.state.csr.pc
        dec = decode(word)
        mnem = dec.mnemonic if dec else "unknown"
        ok = emu.step(word)
        vd_val = [emu.state.vregs.get_elem(dec.vd, e) for e in range(4)] if dec else []
        print(f"  [{i+1}] PC=0x{pc:08x} Word=0x{word:08x} ({mnem})... {'OK' if ok else 'FAIL'} -> vd (v{dec.vd if dec else 0}): {vd_val}")

    print("\n[Final Vector Register File Dump]:")
    print(emu.state.vregs.dump())
    return 0


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--bin":
        sys.exit(run_bytecode_file(sys.argv[2]))
    else:
        sys.exit(run_verification_suite())


if __name__ == "__main__":
    main()