"""Integration tests for all CLI subcommands."""

import os
import sys
import tempfile
import pytest
from random_visa.adapters.inbound.cli.main import (
    main,
    build_composition_root,
    run_synthesize_cmd,
    run_parse_cmd,
    run_compile_sail_cmd,
    run_compile_c_cmd,
    run_assemble_cmd,
    run_exec_bytecode_cmd,
    run_pipeline_cmd,
)
import argparse


def test_cli_synthesize_and_parse(tmp_path):
    sail_path = str(tmp_path / "test_synth.sail")
    args_synth = argparse.Namespace(
        name="TestCLI_ISA",
        num_insts=6,
        vlen=128,
        seed=100,
        out_file=sail_path,
    )
    ret = run_synthesize_cmd(args_synth)
    assert ret == 0
    assert os.path.exists(sail_path)

    args_parse = argparse.Namespace(
        file=sail_path,
        name="TestCLI_ISA",
    )
    ret = run_parse_cmd(args_parse)
    assert ret == 0


def test_cli_pipeline_and_exec_bytecode(tmp_path):
    out_dir = str(tmp_path / "pipeline_out")
    args_pipe = argparse.Namespace(
        name="PipelineCLI_ISA",
        num_insts=4,
        vlen=128,
        seed=200,
        out_dir=out_dir,
        no_compile=False,
    )
    ret = run_pipeline_cmd(args_pipe)
    assert ret == 0
    assert os.path.exists(os.path.join(out_dir, "visa_test_runner"))

    # Test assembling and executing bytecode on the compiled runner
    sail_file = os.path.join(out_dir, "pipelinecli_isa.sail")
    asm_file = str(tmp_path / "prog.asm")
    vbc_file = str(tmp_path / "prog.vbc")

    # Read the sail file to find a valid mnemonic
    gen_use_case, sail_writer, _, _, _, _, sail_parser, assembler = build_composition_root()
    spec = sail_parser.parse_sail_file(sail_file)
    first_inst = spec.instructions[0]

    with open(asm_file, "w") as f:
        f.write(f"{first_inst.mnemonic} v3, v2, v1\n")

    args_asm = argparse.Namespace(
        spec=sail_file,
        file=asm_file,
        out=vbc_file,
    )
    ret_asm = run_assemble_cmd(args_asm)
    assert ret_asm == 0
    assert os.path.exists(vbc_file)

    args_exec = argparse.Namespace(
        emu_dir=out_dir,
        file=vbc_file,
        hex=None,
    )
    ret_exec = run_exec_bytecode_cmd(args_exec)
    assert ret_exec == 0


def test_cli_compile_c(tmp_path):
    sail_path = str(tmp_path / "test_c.sail")
    c_out_dir = str(tmp_path / "c_out")
    args_synth = argparse.Namespace(
        name="C_CLI_ISA",
        num_insts=4,
        vlen=128,
        seed=300,
        out_file=sail_path,
    )
    run_synthesize_cmd(args_synth)

    args_c = argparse.Namespace(
        file=sail_path,
        name="C_CLI_ISA",
        out_dir=c_out_dir,
        no_compile=False,
    )
    ret_c = run_compile_c_cmd(args_c)
    assert ret_c == 0
    assert os.path.exists(os.path.join(c_out_dir, "visa_c_runner"))
