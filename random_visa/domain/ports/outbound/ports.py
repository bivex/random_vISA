"""Outbound (Driven) Ports for Infrastructure and Code Generation."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from random_visa.domain.model.isa_spec import VectorIsaSpec


class SailSpecWriterPort(ABC):
    """Port for persisting/formatting Sail specifications to disk or stream."""
    @abstractmethod
    def write_spec(self, spec: VectorIsaSpec, target_file_path: str) -> str:
        pass


class CppCodeEmitterPort(ABC):
    """Port for generating C++ emulator source code artifacts from an ISA Spec."""
    @abstractmethod
    def emit_emulator_project(
        self,
        spec: VectorIsaSpec,
        destination_dir: str,
    ) -> Dict[str, str]:
        """Emits all C++ emulator files (headers, sources, test suite, CMakeLists).

        Returns a dictionary mapping relative filepath to generated code content.
        """
        pass


class CCodeEmitterPort(ABC):
    """Port for generating Pure C11 emulator source code artifacts from an ISA Spec."""
    @abstractmethod
    def emit_c_project(
        self,
        spec: VectorIsaSpec,
        destination_dir: str,
    ) -> List[str]:
        """Emits all C11 emulator files (headers, sources, test suite, Makefile)."""
        pass


class PydrofoilCodeEmitterPort(ABC):
    """Port for generating Pydrofoil JIT emulator modules from an ISA Spec."""
    @abstractmethod
    def emit_pydrofoil_project(
        self,
        spec: VectorIsaSpec,
        destination_dir: str,
    ) -> List[str]:
        """Emits Pydrofoil Python/RPython emulator files (state, decoder, instructions, runner)."""
        pass


class CompilerRunnerPort(ABC):
    """Port for compiling and executing generated C++ emulator test harness."""
    @abstractmethod
    def compile_and_run(
        self,
        source_dir: str,
        compiler: str = "clang++",
        extra_flags: List[str] = None,
    ) -> Dict[str, Any]:
        """Compiles C++ files and runs the emulator test harness.

        Returns {success: bool, output: str, returncode: int}
        """
        pass
