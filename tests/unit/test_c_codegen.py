"""Unit and integration tests for C11 Code Generator Adapter."""

import tempfile
import os
import subprocess
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.c_codegen.c_code_emitter_adapter import CCodeEmitterAdapter


def test_c11_emulator_emission_and_compilation():
    gen = RandomVisaGeneratorService(seed=99)
    spec, _ = gen.generate_spec(name="C11_Test_ISA", num_instructions=6)

    with tempfile.TemporaryDirectory() as tmp_dir:
        emitter = CCodeEmitterAdapter()
        emitted_files = emitter.emit_c_project(spec, tmp_dir)

        assert len(emitted_files) == 5
        assert os.path.exists(os.path.join(tmp_dir, "visa_emulator.h"))
        assert os.path.exists(os.path.join(tmp_dir, "visa_instructions.c"))
        assert os.path.exists(os.path.join(tmp_dir, "visa_emulator.c"))
        assert os.path.exists(os.path.join(tmp_dir, "visa_main.c"))
        assert os.path.exists(os.path.join(tmp_dir, "Makefile"))

        # Compile with clang -std=c11
        compile_cmd = [
            "clang", "-std=c11", "-O3", "-Wall", "-Wextra", "-I.",
            "visa_emulator.c", "visa_instructions.c", "visa_main.c",
            "-o", "visa_c_runner"
        ]
        comp_proc = subprocess.run(compile_cmd, cwd=tmp_dir, capture_output=True, text=True)
        assert comp_proc.returncode == 0, f"Compilation failed: {comp_proc.stderr}"

        # Run verification binary
        run_proc = subprocess.run([os.path.join(tmp_dir, "visa_c_runner")], cwd=tmp_dir, capture_output=True, text=True)
        assert run_proc.returncode == 0, f"Execution failed: {run_proc.stdout} {run_proc.stderr}"
        assert "6/6 C11 tests passed" in run_proc.stdout
