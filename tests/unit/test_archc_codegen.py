"""Unit tests for ArchC ADL and SystemC Simulator Generation in random_vISA."""

import os
import subprocess
import pytest
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.archc.archc_emitter_adapter import ArchCEmitterAdapter


def test_archc_emitter_generates_files(tmp_path):
    gen_service = RandomVisaGeneratorService(seed=777)
    spec, _ = gen_service.generate_spec(
        name="ArchCTest_ISA",
        num_instructions=6,
        config=VectorConfig(vlen=128),
    )

    out_dir = str(tmp_path / "archc_out")
    emitter = ArchCEmitterAdapter()
    emitted = emitter.emit_archc_project(spec, out_dir)

    basenames = [os.path.basename(p) for p in emitted]
    assert "archctest_isa.ac" in basenames
    assert "archctest_isa.isa" in basenames
    assert "archctest_isa_isa.cpp" in basenames
    assert "main.cpp" in basenames
    assert "build.sh" in basenames

    # Verify content of .ac file
    with open(os.path.join(out_dir, "archctest_isa.ac"), "r", encoding="utf-8") as f:
        ac_txt = f.read()
        assert "AC_ARCH(archctest_isa)" in ac_txt
        assert "ac_regbank VRB:32;" in ac_txt

    # Verify content of .isa file
    with open(os.path.join(out_dir, "archctest_isa.isa"), "r", encoding="utf-8") as f:
        isa_txt = f.read()
        assert "AC_ISA(archctest_isa)" in isa_txt
        for inst in spec.instructions:
            assert inst.mnemonic in isa_txt


@pytest.mark.skipif(
    not os.path.exists("/Volumes/External/Code/ArchC/src/acsim/acsim"),
    reason="ArchC acsim binary not found on local environment",
)
def test_archc_acsim_and_systemc_compilation(tmp_path):
    gen_service = RandomVisaGeneratorService(seed=888)
    spec, _ = gen_service.generate_spec(
        name="SystemC_Vector_ISA",
        num_instructions=4,
        config=VectorConfig(vlen=128),
    )

    out_dir = str(tmp_path / "archc_sim_out")
    emitter = ArchCEmitterAdapter()
    emitter.emit_archc_project(spec, out_dir)

    # Run build.sh
    res = subprocess.run(["/bin/sh", "build.sh"], cwd=out_dir, capture_output=True, text=True)
    assert res.returncode == 0, f"ArchC build failed: {res.stderr}\n{res.stdout}"
    assert "Successfully built SystemC simulator: systemc_vector_isa.x" in res.stdout

    # Verify binary exists and responds to --help
    sim_bin = os.path.join(out_dir, "systemc_vector_isa.x")
    assert os.path.exists(sim_bin)
    help_proc = subprocess.run([os.path.abspath(sim_bin), "--help"], cwd=out_dir, capture_output=True, text=True)
    assert "SystemC" in help_proc.stderr or "SystemC" in help_proc.stdout
