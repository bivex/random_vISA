"""Inbound Driving Adapter: CLI Interface using Rich and Argparse."""

import argparse
import sys
import os
import subprocess
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
from random_visa.domain.services.assembler import VectorAssemblerService
from random_visa.application.use_cases.pipeline import (
    GenerateRandomVisaUseCase, EmitCppEmulatorUseCase, RunFullPipelineUseCase
)
from random_visa.adapters.outbound.sail.sail_file_adapter import SailFileAdapter
from random_visa.adapters.outbound.cpp_codegen.cpp_emitter_adapter import CppEmulatorEmitterAdapter
from random_visa.adapters.outbound.compiler.clang_runner_adapter import ClangCompilerRunnerAdapter
from random_visa.adapters.inbound.parser.sail_antlr_adapter import AntlrSailParserAdapter


from random_visa.adapters.outbound.c_codegen.c_code_emitter_adapter import CCodeEmitterAdapter
from random_visa.adapters.outbound.pydrofoil.pydrofoil_emitter_adapter import PydrofoilEmitterAdapter


def build_composition_root():
    """Dependency Injection / Composition Root."""
    gen_service = RandomVisaGeneratorService()
    gen_use_case = GenerateRandomVisaUseCase(gen_service)
    sail_writer = SailFileAdapter()
    cpp_emitter = CppEmulatorEmitterAdapter()
    c_emitter = CCodeEmitterAdapter()
    pydrofoil_emitter = PydrofoilEmitterAdapter()
    compiler_runner = ClangCompilerRunnerAdapter()
    sail_parser = AntlrSailParserAdapter()
    assembler = VectorAssemblerService()

    pipeline_use_case = RunFullPipelineUseCase(
        generate_use_case=gen_use_case,
        sail_writer=sail_writer,
        cpp_emitter=cpp_emitter,
        compiler_runner=compiler_runner,
    )
    return gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler


def run_compile_pydrofoil_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    _, _, _, _, pydrofoil_emitter, _, _, sail_parser, _ = build_composition_root()

    if not os.path.exists(args.file):
        print(f"Error: file not found '{args.file}'")
        return 1

    spec = sail_parser.parse_sail_file(args.file, spec_name=args.name)
    emitted = pydrofoil_emitter.emit_pydrofoil_project(spec, args.out_dir)

    if not args.no_run:
        runner_path = os.path.join(args.out_dir, "pydrofoil_main.py")
        run_proc = subprocess.run([sys.executable, "-m", f"{os.path.basename(args.out_dir)}.pydrofoil_main"], cwd=os.path.dirname(os.path.abspath(args.out_dir)) or ".", capture_output=True, text=True)
        if run_proc.returncode != 0:
            # Fallback direct execution
            run_proc = subprocess.run([sys.executable, runner_path], cwd=args.out_dir, capture_output=True, text=True)

        if HAS_RICH:
            console.print(Panel(
                run_proc.stdout + run_proc.stderr,
                title="[bold green]Pydrofoil JIT Vector Emulator Verification Trace[/bold green]",
                border_style="green" if run_proc.returncode == 0 else "red"
            ))
        else:
            print(run_proc.stdout + run_proc.stderr)
        return run_proc.returncode
    else:
        print(f"Generated Pydrofoil JIT emulator in {args.out_dir} from {args.file}")
        return 0



def run_compile_c_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()

    if not os.path.exists(args.file):
        print(f"Error: file not found '{args.file}'")
        return 1

    spec = sail_parser.parse_sail_file(args.file, spec_name=args.name)
    emitted = c_emitter.emit_c_project(spec, args.out_dir)

    if not args.no_compile:
        # Compile with clang -std=c11
        compile_cmd = [
            "clang", "-std=c11", "-O3", "-Wall", "-Wextra", "-I.",
            "visa_emulator.c", "visa_instructions.c", "visa_main.c",
            "-o", "visa_c_runner"
        ]
        comp_proc = subprocess.run(compile_cmd, cwd=args.out_dir, capture_output=True, text=True)
        if comp_proc.returncode != 0:
            if HAS_RICH:
                console.print(Panel(comp_proc.stderr, title="[bold red]C11 Compiler Error[/bold red]", border_style="red"))
            else:
                print("C11 Compilation Failed:\n" + comp_proc.stderr)
            return 1

        run_proc = subprocess.run(["./visa_c_runner"], cwd=args.out_dir, capture_output=True, text=True)
        if HAS_RICH:
            console.print(Panel(
                run_proc.stdout + run_proc.stderr,
                title="[bold green]Pure C11 Vector Emulator Verification Trace[/bold green]",
                border_style="green" if run_proc.returncode == 0 else "red"
            ))
        else:
            print(run_proc.stdout + run_proc.stderr)
        return run_proc.returncode
    else:
        print(f"Generated Pure C11 emulator in {args.out_dir} from {args.file}")
        return 0


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

    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()
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
    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()
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
    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()

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
    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()

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


def run_assemble_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    gen_use_case, sail_writer, cpp_emitter, c_emitter, pydrofoil_emitter, compiler_runner, pipeline_use_case, sail_parser, assembler = build_composition_root()

    if not os.path.exists(args.spec):
        print(f"Error: spec file not found '{args.spec}'")
        return 1
    if not os.path.exists(args.file):
        print(f"Error: assembly file not found '{args.file}'")
        return 1

    spec = sail_parser.parse_sail_file(args.spec)
    with open(args.file, "r", encoding="utf-8") as f:
        asm_content = f.read()

    words = assembler.assemble_program(spec, asm_content)
    out_bin = args.out or "program.vbc"
    assembler.write_binary_bytecode(words, out_bin)

    if HAS_RICH:
        table = Table(title=f"Assembled Bytecode Program: {out_bin}", show_header=True, header_style="bold green")
        table.add_column("PC Offset", style="dim", width=10)
        table.add_column("Hex Word", style="bold yellow")
        table.add_column("Binary [31:0]", style="cyan")

        for idx, word in enumerate(words):
            table.add_row(f"+0x{idx * 4:04X}", f"0x{word:08X}", f"{word:032b}")
        console.print(table)
        console.print(f"[bold green]Successfully assembled {len(words)} instructions -> {out_bin}[/bold green]")
    else:
        print(f"Assembled {len(words)} instructions to {out_bin}")
        for idx, w in enumerate(words):
            print(f"  +0x{idx * 4:04X}: 0x{w:08X}")
    return 0


def run_exec_bytecode_cmd(args: argparse.Namespace) -> int:
    console = Console() if HAS_RICH else None
    runner_bin = os.path.join(args.emu_dir, "visa_test_runner")
    if not os.path.exists(runner_bin):
        print(f"Error: emulator binary not found at '{runner_bin}'. Build it first via pipeline or compile-sail.")
        return 1

    cmd = [os.path.abspath(runner_bin)]
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: bytecode file not found '{args.file}'")
            return 1
        cmd.extend(["--bin", os.path.abspath(args.file)])
    elif args.hex:
        cmd.extend(["--hex"] + args.hex)
    else:
        print("Error: specify either a binary bytecode file or --hex <words>")
        return 1

    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=args.emu_dir)
    if HAS_RICH:
        console.print(Panel(
            proc.stdout + proc.stderr,
            title="[bold green]VCPU Bytecode Execution Trace[/bold green]",
            border_style="green" if proc.returncode == 0 else "red"
        ))
    else:
        print(proc.stdout + proc.stderr)
    return proc.returncode


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

    # Assemble command
    asm_parser = subparsers.add_parser("assemble", help="Assemble text vector assembly into binary bytecode (.vbc)")
    asm_parser.add_argument("file", help="Path to text assembly file (.asm / .s)")
    asm_parser.add_argument("--spec", required=True, help="Path to .sail ISA specification file")
    asm_parser.add_argument("-o", "--out", default="program.vbc", help="Output binary bytecode (.vbc) file")

    # Exec-Bytecode command
    exec_parser = subparsers.add_parser("exec-bytecode", help="Execute binary bytecode on the C++ VCPU emulator")
    exec_parser.add_argument("file", nargs="?", default="", help="Path to binary bytecode (.vbc) file")
    exec_parser.add_argument("--emu-dir", default="generated_emulator", help="Path to emulator directory containing visa_test_runner")
    exec_parser.add_argument("--hex", nargs="*", help="Direct list of hex words to execute (e.g. 0x0220a1d7)")

    # Compile-C command (Direct Sail -> Pure C11 Emulator)
    cc_parser = subparsers.add_parser("compile-c", help="Parse a Sail (.sail) file and generate Pure C11 emulator")
    cc_parser.add_argument("file", help="Path to .sail specification file")
    cc_parser.add_argument("--name", default="Parsed_C_ISA", help="Name for the ISA")
    cc_parser.add_argument("-o", "--out-dir", default="c_emulator", help="Output directory for C11 emulator")
    cc_parser.add_argument("--no-compile", action="store_true", help="Skip C compilation")

    # Compile-Pydrofoil command (Direct Sail -> Pydrofoil JIT / Python Emulator)
    cp_parser = subparsers.add_parser("compile-pydrofoil", help="Parse a Sail (.sail) file and generate Pydrofoil JIT emulator")
    cp_parser.add_argument("file", help="Path to .sail specification file")
    cp_parser.add_argument("--name", default="Parsed_Pydrofoil_ISA", help="Name for the ISA")
    cp_parser.add_argument("-o", "--out-dir", default="pydrofoil_emulator", help="Output directory for Pydrofoil emulator")
    cp_parser.add_argument("--no-run", action="store_true", help="Skip test execution")

    args = parser.parse_args()
    if args.command == "pipeline":
        sys.exit(run_pipeline_cmd(args))
    elif args.command == "synthesize":
        sys.exit(run_synthesize_cmd(args))
    elif args.command == "parse":
        sys.exit(run_parse_cmd(args))
    elif args.command == "compile-sail":
        sys.exit(run_compile_sail_cmd(args))
    elif args.command == "compile-c":
        sys.exit(run_compile_c_cmd(args))
    elif args.command == "compile-pydrofoil":
        sys.exit(run_compile_pydrofoil_cmd(args))
    elif args.command == "assemble":
        sys.exit(run_assemble_cmd(args))
    elif args.command == "exec-bytecode":
        sys.exit(run_exec_bytecode_cmd(args))
    else:
        parser.print_help()
        sys.exit(1)


def cli_entrypoint() -> None:
    main()


if __name__ == "__main__":
    main()
