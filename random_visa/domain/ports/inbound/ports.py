"""Inbound (Driving) Ports for V-ISA Use Cases."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from random_visa.domain.model.isa_spec import VectorIsaSpec


class GenerateSpecPort(ABC):
    """Port for generating randomized or custom Vector ISA specifications."""
    @abstractmethod
    def generate(
        self,
        name: str,
        num_instructions: int,
        vlen: int = 128,
        elen: int = 64,
        seed: Optional[int] = None,
    ) -> VectorIsaSpec:
        pass


class EmitEmulatorPort(ABC):
    """Port for translating an ISA spec into a C++ emulator codebase."""
    @abstractmethod
    def emit(
        self,
        spec: VectorIsaSpec,
        output_directory: str,
    ) -> Dict[str, str]:
        pass


class RunPipelinePort(ABC):
    """Port for orchestrating synthesis -> Sail export -> C++ emission -> compilation & validation."""
    @abstractmethod
    def execute(
        self,
        name: str,
        num_instructions: int,
        output_dir: str,
        vlen: int = 128,
        seed: Optional[int] = None,
        compile_and_test: bool = True,
    ) -> Dict[str, Any]:
        pass


class SailParserPort(ABC):
    """Port for parsing Sail specification source code into domain VectorIsaSpec AST."""
    @abstractmethod
    def parse_sail_source(self, source_text: str, spec_name: str = "Parsed_Sail_ISA") -> VectorIsaSpec:
        pass

