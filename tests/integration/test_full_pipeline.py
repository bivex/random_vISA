"""Integration tests for end-to-end V-ISA to C++ emulator generation and execution."""

import os
import shutil
import tempfile
from random_visa.application.use_cases.pipeline import (
    GenerateRandomVisaUseCase, RunFullPipelineUseCase
)
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.sail.sail_file_adapter import SailFileAdapter
from random_visa.adapters.outbound.cpp_codegen.cpp_emitter_adapter import CppEmulatorEmitterAdapter
from random_visa.adapters.outbound.compiler.clang_runner_adapter import ClangCompilerRunnerAdapter


def test_full_pipeline_compiles_and_passes_verification():
    temp_dir = tempfile.mkdtemp(prefix="visa_test_")
    try:
        gen_service = RandomVisaGeneratorService(seed=777)
        gen_use_case = GenerateRandomVisaUseCase(gen_service)
        sail_writer = SailFileAdapter()
        cpp_emitter = CppEmulatorEmitterAdapter()
        compiler_runner = ClangCompilerRunnerAdapter()

        pipeline = RunFullPipelineUseCase(
            generate_use_case=gen_use_case,
            sail_writer=sail_writer,
            cpp_emitter=cpp_emitter,
            compiler_runner=compiler_runner,
        )

        result = pipeline.execute(
            name="RVV_Integration_ISA",
            num_instructions=6,
            output_dir=temp_dir,
            vlen=128,
            seed=777,
            compile_and_test=True,
        )

        assert result.spec_name == "RVV_Integration_ISA"
        assert result.instruction_count == 6
        assert os.path.exists(result.sail_file_path)
        assert result.compilation_success is True
        assert "Results: 6/6 instructions executed successfully" in result.execution_output

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
