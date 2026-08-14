"""Application Data Transfer Objects (DTOs)."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class GenerateSpecRequest:
    name: str = "RVV_Random_ISA"
    num_instructions: int = 16
    vlen: int = 128
    elen: int = 64
    seed: Optional[int] = None


@dataclass
class EmitEmulatorRequest:
    spec_name: str
    output_dir: str


@dataclass
class PipelineRequest:
    spec_name: str = "RVV_Random_ISA"
    num_instructions: int = 16
    output_dir: str = "generated_emulator"
    vlen: int = 128
    elen: int = 64
    seed: Optional[int] = 42
    compile_and_run_tests: bool = True


@dataclass
class PipelineResult:
    spec_name: str
    instruction_count: int
    sail_file_path: str
    emitted_files: List[str]
    compilation_success: bool
    compiler_output: str
    execution_output: str
    metadata: Dict[str, Any] = field(default_factory=dict)
