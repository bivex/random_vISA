"""Unit tests for Pydrofoil JIT / Python Vector Emulator Generation and Execution."""

import os
import sys
import subprocess
import pytest
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.pydrofoil.pydrofoil_emitter_adapter import PydrofoilEmitterAdapter


@pytest.mark.parametrize("vlen", [64, 128, 256, 512])
def test_pydrofoil_codegen_multi_vlen(vlen, tmp_path):
    gen_service = RandomVisaGeneratorService(seed=5000 + vlen)
    spec, _ = gen_service.generate_spec(
        name=f"VLEN_{vlen}_Pydrofoil_ISA",
        num_instructions=6,
        config=VectorConfig(vlen=vlen),
    )

    out_dir = str(tmp_path / f"pydrofoil_vlen_{vlen}")
    emitter = PydrofoilEmitterAdapter()
    emitted = emitter.emit_pydrofoil_project(spec, out_dir)

    basenames = [os.path.basename(p) for p in emitted]
    assert "pydrofoil_state.py" in basenames
    assert "pydrofoil_decoder.py" in basenames
    assert "pydrofoil_instructions.py" in basenames
    assert "pydrofoil_emulator.py" in basenames
    assert "pydrofoil_main.py" in basenames

    # Run verification harness
    main_py = os.path.join(out_dir, "pydrofoil_main.py")
    res = subprocess.run([sys.executable, main_py], capture_output=True, text=True, cwd=out_dir)
    assert res.returncode == 0, f"Pydrofoil verification failed: {res.stderr}\n{res.stdout}"
    assert "Results: 6/6 Pydrofoil tests passed." in res.stdout


def test_pydrofoil_bytecode_execution(tmp_path):
    from random_visa.domain.services.assembler import VectorAssemblerService

    gen_service = RandomVisaGeneratorService(seed=9876)
    spec, _ = gen_service.generate_spec(
        name="BytecodePydrofoil_ISA",
        num_instructions=8,
        config=VectorConfig(vlen=128),
    )

    out_dir = str(tmp_path / "pydrofoil_emu")
    emitter = PydrofoilEmitterAdapter()
    emitter.emit_pydrofoil_project(spec, out_dir)

    # Assemble simple instructions
    inst1 = spec.instructions[0]
    inst2 = spec.instructions[1]
    asm_text = f"{inst1.mnemonic} v4, v2, v1\n{inst2.mnemonic} v5, v2, x1\n"

    assembler = VectorAssemblerService()
    words = assembler.assemble_program(spec, asm_text)
    vbc_path = os.path.join(out_dir, "test.vbc")
    assembler.write_binary_bytecode(words, vbc_path)

    # Execute bytecode via pydrofoil_main.py --bin test.vbc
    main_py = os.path.join(out_dir, "pydrofoil_main.py")
    res = subprocess.run([sys.executable, main_py, "--bin", vbc_path], capture_output=True, text=True, cwd=out_dir)
    assert res.returncode == 0, f"Pydrofoil bytecode run failed: {res.stderr}\n{res.stdout}"
    assert "Executing Bytecode Program (2 instructions)..." in res.stdout
    assert "Final Vector Register File Dump" in res.stdout
