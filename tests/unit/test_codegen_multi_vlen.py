"""Unit tests for C11 and C++ codegen with various VLEN configurations."""

import os
import tempfile
import pytest
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.c_codegen.c_code_emitter_adapter import CCodeEmitterAdapter
from random_visa.adapters.outbound.cpp_codegen.cpp_emitter_adapter import CppEmulatorEmitterAdapter
from random_visa.adapters.outbound.compiler.clang_runner_adapter import ClangCompilerRunnerAdapter


@pytest.mark.parametrize("vlen", [64, 128, 256, 512])
def test_cpp_codegen_various_vlens(vlen, tmp_path):
    from random_visa.domain.model.vector_config import VectorConfig
    gen_service = RandomVisaGeneratorService(seed=1000 + vlen)
    spec, _ = gen_service.generate_spec(name=f"VLEN_{vlen}_CPP_ISA", num_instructions=4, config=VectorConfig(vlen=vlen))

    out_dir = str(tmp_path / f"cpp_vlen_{vlen}")
    emitter = CppEmulatorEmitterAdapter()
    emitted_files = emitter.emit_emulator_project(spec, out_dir)

    assert "isa_state.hpp" in emitted_files
    assert "instructions.cpp" in emitted_files

    compiler = ClangCompilerRunnerAdapter()
    res = compiler.compile_and_run(out_dir)
    assert res["success"] is True, f"C++ compilation failed for VLEN={vlen}: {res['compiler_output']}"
    assert "Results: 4/4 instructions executed successfully." in res["execution_output"]


@pytest.mark.parametrize("vlen", [64, 128, 256, 512])
def test_c11_codegen_various_vlens(vlen, tmp_path):
    from random_visa.domain.model.vector_config import VectorConfig
    gen_service = RandomVisaGeneratorService(seed=2000 + vlen)
    spec, _ = gen_service.generate_spec(name=f"VLEN_{vlen}_C_ISA", num_instructions=4, config=VectorConfig(vlen=vlen))

    out_dir = str(tmp_path / f"c_vlen_{vlen}")
    emitter = CCodeEmitterAdapter()
    emitted_files = emitter.emit_c_project(spec, out_dir)

    basenames = [os.path.basename(f) for f in emitted_files]
    assert "visa_emulator.h" in basenames
    assert "visa_instructions.c" in basenames

    # Compile with clang C11
    import subprocess
    comp_proc = subprocess.run(
        ["clang", "-std=c11", "-O3", "-Wall", "visa_instructions.c", "visa_emulator.c", "visa_main.c", "-o", "visa_c_runner"],
        cwd=out_dir,
        capture_output=True,
        text=True
    )
    assert comp_proc.returncode == 0, f"C11 compilation failed for VLEN={vlen}: {comp_proc.stderr}"

    run_proc = subprocess.run(["./visa_c_runner"], cwd=out_dir, capture_output=True, text=True)
    assert run_proc.returncode == 0
    assert "Results: 4/4 C11 tests passed." in run_proc.stdout
