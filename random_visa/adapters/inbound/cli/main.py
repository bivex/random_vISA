"""Inbound Driving Adapter: CLI Interface using Rich and Argparse."""

import argparse
import sys
import os
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.application.use_cases.pipeline import (
    GenerateRandomVisaUseCase, EmitCppEmulatorUseCase, RunFullPipelineUseCase
)
from random_visa.adapters.outbound.sail.sail_file_adapter import SailFileAdapter
from random_visa.adapters.outbound.cpp_codegen.cpp_emitter_adapter import CppEmulatorEmitterAdapter
from random_visa.adapters.outbound.compiler.clang_runner_adapter import ClangCompilerRunnerAdapter


def build_pipeline_use_case() -> RunFullPipelineUseCase:
    """Dependency Injection / Composition Root."""
    gen_service = RandomVisaGeneratorService()
    gen_use_case = GenerateRandomVisaUseCase(gen_service)
    sail_writer = SailFileAdapter()
    cpp_emitter = CppEmulatorEmitterAdapter()
    compiler_runner = ClangCompilerRunnerAdapter()

    return RunFullPipelineUseCase(
        generate_use_case=gen_use_case,
        sail_writer=sail_writer,
        cpp_emitter=cpp_emitter,
        compiler_runner=compiler_runner,
    )


def run_pipeline_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    
    if HAS_RICH:
        console.print(Panel.fit(
            f"[bold cyan]Hexagonal DDD V-ISA Synthesizer -> C++ Emulator Generator[/bold cyan]\n"
            f"[yellow]Spec:[/yellow] {args.name} | [yellow]Instructions:[/yellow] {args.num_insts} | "
            f"[yellow]VLEN:[/yellow] {args.vlen}b | [yellow]Seed:[/yellow] {args.seed}",
            border_style="cyan"
        ))
    else:
        print(f"=== Synthesizing {args.name} ({args.num_insts} insts, VLEN={args.vlen}) ===")

    use_case = build_pipeline_use_case()
    result = use_case.execute(
        name=args.name,
        num_instructions=args.num_insts,
        output_dir=args.out_dir,
        vlen=args.vlen,
        seed=args.seed,
        compile_and_test=not args.no_compile,
    )

    if HAS_RICH:
        table = Table(title="Synthesized V-ISA Pipeline Summary", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="dim", width=25)
        table.add_column("Value", style="bold")

        table.add_row("ISA Specification Name", result.spec_name)
        table.add_row("Instructions Synthesized", str(result.instruction_count))
        table.add_row("Sail Specification File", result.sail_file_path)
        table.add_row("Generated C++ Files", ", ".join(result.emitted_files))
        table.add_row("C++ Compilation", "[green]PASSED[/green]" if result.compilation_success else "[red]FAILED/SKIPPED[/red]")
        
        console.print(table)

        if result.execution_output:
            console.print(Panel(
                result.execution_output,
                title="[bold green]C++ Emulator Test Execution Output[/bold green]",
                border_style="green"
            ))
        elif result.compiler_output:
            console.print(Panel(
                result.compiler_output,
                title="[bold red]Compiler Output[/bold red]",
                border_style="red"
            ))
    else:
        print(f"\nPipeline execution complete:")
        print(f"  Sail Spec: {result.sail_file_path}")
        print(f"  C++ Directory: {args.out_dir}")
        print(f"  Compilation Success: {result.compilation_success}")
        if result.execution_output:
            print("\nExecution Output:\n" + result.execution_output)

    return 0 if result.compilation_success or args.no_compile else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="visa-gen",
        description="Hexagonal DDD: Random Sail (V-ISA) -> C++ Emulator Generator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Pipeline command
    pipe_parser = subparsers.add_parser("pipeline", help="Run full synthesis and generation pipeline")
    pipe_parser.add_argument("--name", default="RVV_Random_ISA", help="Name of synthesized ISA")
    pipe_parser.add_argument("-n", "--num-insts", type=int, default=12, help="Number of random vector instructions")
    pipe_parser.add_argument("--vlen", type=int, default=128, help="Vector register width in bits")
    pipe_parser.add_argument("--seed", type=int, default=42, help="Randomization seed")
    pipe_parser.add_argument("-o", "--out-dir", default="generated_emulator", help="Output directory")
    pipe_parser.add_argument("--no-compile", action="store_true", help="Skip C++ compilation and test execution")

    args = parser.parse_args()
    if args.command == "pipeline":
        sys.exit(run_pipeline_cmd(args))


def cli_entrypoint() -> None:
    main()


if __name__ == "__main__":
    main()
