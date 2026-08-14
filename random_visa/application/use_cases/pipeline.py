"""Use Cases for V-ISA Synthesizer and Emulator Generation."""

import os
from typing import Optional, Dict, Any, List
from random_visa.domain.model.types import SEW, LMUL
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.domain.ports.inbound.ports import GenerateSpecPort, EmitEmulatorPort, RunPipelinePort
from random_visa.domain.ports.outbound.ports import SailSpecWriterPort, CppCodeEmitterPort, CompilerRunnerPort
from random_visa.application.dtos import PipelineRequest, PipelineResult


class GenerateRandomVisaUseCase(GenerateSpecPort):
    """Use Case: Generate randomized V-ISA specification."""

    def __init__(self, generator_service: Optional[RandomVisaGeneratorService] = None) -> None:
        self.generator_service = generator_service or RandomVisaGeneratorService()

    def generate(
        self,
        name: str = "RVV_Random_ISA",
        num_instructions: int = 16,
        vlen: int = 128,
        elen: int = 64,
        seed: Optional[int] = None,
    ) -> VectorIsaSpec:
        if seed is not None:
            self.generator_service = RandomVisaGeneratorService(seed=seed)
        
        config = VectorConfig(vlen=vlen, elen=elen, default_sew=SEW.E32, default_lmul=LMUL.M1)
        spec, _events = self.generator_service.generate_spec(
            name=name,
            num_instructions=num_instructions,
            config=config,
        )
        return spec


class EmitCppEmulatorUseCase(EmitEmulatorPort):
    """Use Case: Emit C++ emulator files for a given ISA specification."""

    def __init__(self, cpp_emitter: CppCodeEmitterPort) -> None:
        self.cpp_emitter = cpp_emitter

    def emit(
        self,
        spec: VectorIsaSpec,
        output_directory: str,
    ) -> Dict[str, str]:
        return self.cpp_emitter.emit_emulator_project(spec, output_directory)


class RunFullPipelineUseCase(RunPipelinePort):
    """Use Case: End-to-End pipeline (Synthesize V-ISA -> Write Sail -> Emit C++ -> Compile & Test)."""

    def __init__(
        self,
        generate_use_case: GenerateRandomVisaUseCase,
        sail_writer: SailSpecWriterPort,
        cpp_emitter: CppCodeEmitterPort,
        compiler_runner: Optional[CompilerRunnerPort] = None,
    ) -> None:
        self.generate_use_case = generate_use_case
        self.sail_writer = sail_writer
        self.cpp_emitter = cpp_emitter
        self.compiler_runner = compiler_runner

    def execute(
        self,
        name: str,
        num_instructions: int,
        output_dir: str,
        vlen: int = 128,
        seed: Optional[int] = None,
        compile_and_test: bool = True,
    ) -> PipelineResult:
        # Step 1: Synthesize random ISA Spec
        spec = self.generate_use_case.generate(
            name=name,
            num_instructions=num_instructions,
            vlen=vlen,
            seed=seed,
        )

        os.makedirs(output_dir, exist_ok=True)

        # Step 2: Write formal Sail spec
        sail_path = os.path.join(output_dir, f"{name.lower()}.sail")
        self.sail_writer.write_spec(spec, sail_path)

        # Step 3: Emit C++20 Emulator
        emitted_files_map = self.cpp_emitter.emit_emulator_project(spec, output_dir)
        emitted_file_list = list(emitted_files_map.keys())

        compilation_success = False
        compiler_output = ""
        execution_output = ""

        # Step 4: Compile and Run tests (if compiler runner available and requested)
        if compile_and_test and self.compiler_runner:
            comp_result = self.compiler_runner.compile_and_run(output_dir)
            compilation_success = comp_result.get("success", False)
            compiler_output = comp_result.get("compiler_output", "")
            execution_output = comp_result.get("execution_output", "")

        return PipelineResult(
            spec_name=spec.name,
            instruction_count=len(spec.instructions),
            sail_file_path=sail_path,
            emitted_files=emitted_file_list,
            compilation_success=compilation_success,
            compiler_output=compiler_output,
            execution_output=execution_output,
            metadata={
                "vlen": spec.config.vlen,
                "elen": spec.config.elen,
                "num_instructions": len(spec.instructions),
                "seed": seed,
            },
        )
