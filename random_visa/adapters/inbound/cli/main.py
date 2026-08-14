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
from random_visa.adapters.inbound.parser.sail_antlr_adapter import AntlrSailParserAdapter


def build_composition_root():
    """Dependency Injection / Composition Root."""
    gen_service = RandomVisaGeneratorService()
    gen_use_case = GenerateRandomVisaUseCase(gen_service)
    sail_writer = SailFileAdapter()
    cpp_emitter = CppEmulatorEmitterAdapter()
    compiler_runner = ClangCompilerRunnerAdapter()
    sail_parser = AntlrSailParserAdapter()

    pipeline_use_case = RunFullPipelineUseCase(
        generate_use_case=gen_use_case,
        sail_writer=sail_writer,
        cpp_emitter=cpp_emitter,
        compiler_runner=compiler_runner,
    )
    return gen_use_case, sail_writer, cpp_emitter, compiler_runner, pipeline_use_case, sail_parser


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

    _, _, _, _, pipeline_use_case, _ = build_composition_root()
    result = pipeline_use_case.execute(
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


def run_synthesize_cmd(args: argparse.Namespace) -> int:
    gen_use_case, sail_writer, _, _, _, _ = build_composition_root()
    spec = gen_use_case.generate(
        name=args.name,
        num_instructions=args.num_insts,
        vlen=args.vlen,
        seed=args.seed,
    )
    out_file = args.out_file or f"{args.name.lower()}.sail"
    sail_writer.write_spec(spec, out_file)
    print(f"Successfully generated Sail specification: {out_file} ({len(spec.instructions)} instructions)")
    return 0


def run_parse_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    _, _, _, _, _, sail_parser = build_composition_root()

    if not os.path.exists(args.file):
        print(f"Error: file not found '{args.file}'")
        return 1

    spec = sail_parser.parse_sail_file(args.file, spec_name=args.name)

    if HAS_RICH:
        table = Table(title=f"Parsed Sail Specification: {spec.name}", show_header=True, header_style="bold cyan")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Mnemonic", style="bold green")
        table.add_column("Format", style="yellow")
        table.add_column("Operation", style="magenta")
        table.add_column("Encoding (f6/f3)", style="blue")

        for idx, inst in enumerate(spec.instructions, start=1):
            op_str = inst.binary_op.name if inst.binary_op else (inst.unary_op.name if inst.unary_op else "CUSTOM")
            enc_str = f"f6={inst.funct6:02d}, f3={inst.funct3}"
            table.add_row(str(idx), inst.mnemonic, inst.format.value, op_str, enc_str)

        console.print(table)
        console.print(f"[bold green]Successfully parsed {len(spec.instructions)} instructions with VLEN={spec.config.vlen}b[/bold green]")
    else:
        print(f"Parsed {len(spec.instructions)} instructions from {args.file} (VLEN={spec.config.vlen}b)")
        for inst in spec.instructions:
            print(f"  - {inst.mnemonic} ({inst.format.value})")

    return 0


def run_compile_sail_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    _, _, cpp_emitter, compiler_runner, _, sail_parser = build_composition_root()

    if not os.path.exists(args.file):
        print(f"Error: file not found '{args.file}'")
        return 1

    spec = sail_parser.parse_sail_file(args.file, spec_name=args.name)
    emitted = cpp_emitter.emit_emulator_project(spec, args.out_dir)

    if not args.no_compile and compiler_runner:
        comp_res = compiler_runner.compile_and_run(args.out_dir)
        if HAS_RICH:
            console.print(Panel(
                comp_res.get("execution_output", "") or comp_res.get("compiler_output", ""),
                title="[bold green]C++ Emulator Execution from Parsed Sail Spec[/bold green]",
                border_style="green" if comp_res.get("success") else "red"
            ))
        else:
            print(comp_res.get("execution_output", ""))
        return 0 if comp_res.get("success") else 1
    else:
        print(f"Generated C++ emulator in {args.out_dir} from {args.file}")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="visa-gen",
        description="Hexagonal DDD: Random Sail (V-ISA) -> ANTLR4 Parser -> C++ Emulator Generator",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Pipeline command
    pipe_parser = subparsers.add_parser("pipeline", help="Run full synthesis, Sail export, and C++ generation")
    pipe_parser.add_argument("--name", default="RVV_Random_ISA", help="Name of synthesized ISA")
    pipe_parser.add_argument("-n", "--num-insts", type=int, default=12, help="Number of random vector instructions")
    pipe_parser.add_argument("--vlen", type=int, default=128, help="Vector register width in bits")
    pipe_parser.add_argument("--seed", type=int, default=42, help="Randomization seed")
    pipe_parser.add_argument("-o", "--out-dir", default="generated_emulator", help="Output directory")
    pipe_parser.add_argument("--no-compile", action="store_true", help="Skip C++ compilation and test execution")

    # Synthesize command
    syn_parser = subparsers.add_parser("synthesize", help="Synthesize Sail specification only")
    syn_parser.add_argument("--name", default="RVV_Random_ISA", help="Name of synthesized ISA")
    syn_parser.add_argument("-n", "--num-insts", type=int, default=12, help="Number of random vector instructions")
    syn_parser.add_argument("--vlen", type=int, default=128, help="Vector register width in bits")
    syn_parser.add_argument("--seed", type=int, default=42, help="Randomization seed")
    syn_parser.add_argument("-o", "--out-file", default="", help="Output .sail file path")

    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Parse any Sail (.sail) file using ANTLR4")
    parse_parser.add_argument("file", help="Path to .sail specification file")
    parse_parser.add_argument("--name", default="Parsed_Sail_ISA", help="Name for the parsed ISA")

    # Compile-Sail command (Direct Sail -> C++ Emulator)
    cs_parser = subparsers.add_parser("compile-sail", help="Parse a Sail (.sail) file and generate C++ emulator")
    cs_parser.add_argument("file", help="Path to .sail specification file")
    cs_parser.add_argument("--name", default="Parsed_Sail_ISA", help="Name for the ISA")
    cs_parser.add_argument("-o", "--out-dir", default="parsed_emulator", help="Output directory for C++ emulator")
    cs_parser.add_argument("--no-compile", action="store_true", help="Skip compilation")

    args = parser.parse_args()
    if args.command == "pipeline":
        sys.exit(run_pipeline_cmd(args))
    elif args.command == "synthesize":
        sys.exit(run_synthesize_cmd(args))
    elif args.command == "parse":
        sys.exit(run_parse_cmd(args))
    elif args.command == "compile-sail":
        sys.exit(run_compile_sail_cmd(args))
    else:
        parser.print_help()
        sys.exit(1)


def cli_entrypoint() -> None:
    main()


if __name__ == "__main__":
    main()
