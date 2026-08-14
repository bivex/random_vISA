"""Outbound Adapter: Clang/GCC Compiler and Test Runner."""

import subprocess
import os
import shutil
from typing import Dict, List, Any, Optional
from random_visa.domain.ports.outbound.ports import CompilerRunnerPort


class ClangCompilerRunnerAdapter(CompilerRunnerPort):
    """Adapter for compiling and executing generated C++ emulator test harness."""

    def __init__(self, default_compiler: str = "clang++") -> None:
        self.compiler = default_compiler

    def compile_and_run(
        self,
        source_dir: str,
        compiler: Optional[str] = None,
        extra_flags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        cxx = compiler or self.compiler
        if not shutil.which(cxx):
            # Fallback to g++ or clang++
            cxx = "g++" if shutil.which("g++") else "c++"

        binary_path = os.path.abspath(os.path.join(source_dir, "visa_test_runner"))
        source_files = [
            os.path.abspath(os.path.join(source_dir, "main.cpp")),
            os.path.abspath(os.path.join(source_dir, "instructions.cpp")),
        ]

        flags = ["-std=c++20", "-O2", "-Wall", "-Wextra", f"-I{os.path.abspath(source_dir)}"]
        if extra_flags:
            flags.extend(extra_flags)

        compile_cmd = [cxx] + flags + source_files + ["-o", binary_path]

        try:
            compile_proc = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if compile_proc.returncode != 0:
                return {
                    "success": False,
                    "compiler_output": compile_proc.stderr or compile_proc.stdout,
                    "execution_output": "",
                    "returncode": compile_proc.returncode,
                }

            # Run test runner binary
            exec_proc = subprocess.run(
                [binary_path],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=os.path.abspath(source_dir),
            )

            return {
                "success": (exec_proc.returncode == 0),
                "compiler_output": compile_proc.stdout + compile_proc.stderr,
                "execution_output": exec_proc.stdout + exec_proc.stderr,
                "returncode": exec_proc.returncode,
            }

        except Exception as e:
            return {
                "success": False,
                "compiler_output": f"Exception during build/run: {str(e)}",
                "execution_output": "",
                "returncode": -1,
            }
