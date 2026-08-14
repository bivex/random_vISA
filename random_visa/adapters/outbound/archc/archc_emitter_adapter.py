"""Outbound Adapter: ArchC Architecture Description Language (ADL) and SystemC Generator."""

import os
from typing import Dict, List, Any
from jinja2 import Environment, DictLoader
from random_visa.domain.model.types import InstructionFormat, BinaryOp, UnaryOp
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.ports.outbound.ports import ArchCCodeEmitterPort


ARCHC_TEMPLATES = {
"archc.ac": r"""AC_ARCH({{ model_name }}) {
  ac_mem DM:512M;
  ac_regbank VRB:{{ config.num_vregs }};
  ac_regbank XRB:32;
  ac_wordsize 32;

  ARCH_CTOR({{ model_name }}) {
    ac_isa("{{ model_name }}.isa");
    set_endian("little");
  };
};
""",

"archc.isa": r"""AC_ISA({{ model_name }}) {
  ac_format Type_VV = "%funct6:6 %vm:1 %vs2:5 %vs1:5 %funct3:3 %vd:5 %opcode:7";
  ac_format Type_VX = "%funct6:6 %vm:1 %vs2:5 %rs1:5 %funct3:3 %vd:5 %opcode:7";
  ac_format Type_VI = "%funct6:6 %vm:1 %vs2:5 %imm:5 %funct3:3 %vd:5 %opcode:7";
  ac_format Type_MVV = "%funct6:6 %vm:1 %vs2:5 %vs1:5 %funct3:3 %vd:5 %opcode:7";

  // Instruction Declarations
{% for inst in instructions %}
  ac_instr<Type_{{ inst.format_tag }}> {{ inst.mnemonic }};
{% endfor %}

  ac_asm_map reg {
    "$"[0..31] = [0..31];
    "v"[0..31] = [0..31];
  }

  ISA_CTOR({{ model_name }}) {
{% for inst in instructions %}
    {{ inst.mnemonic }}.set_asm("{{ inst.mnemonic }} %vd, %vs2, %{{ inst.src_op_name }}");
    {{ inst.mnemonic }}.set_decoder(funct6={{ inst.funct6 }}, funct3={{ inst.funct3 }}, opcode=0x57);
{% endfor %}
  };
};
""",

"archc_isa.cpp": r"""/******************************************************
 * Behavior implementation for ArchC {{ model_name }} model  *
 * Generated automatically by random_vISA               *
 ******************************************************/

#include <iostream>
#include <cstdio>
#include <cstdint>
#include <algorithm>
#include "{{ model_name }}_isa.H"
#include "{{ model_name }}_isa_init.cpp"
#include "{{ model_name }}_bhv_macros.H"

using namespace {{ model_name }}_parms;

static inline int32_t clamp_i32(int64_t val) {
    if (val < INT32_MIN) return INT32_MIN;
    if (val > INT32_MAX) return INT32_MAX;
    return static_cast<int32_t>(val);
}

void ac_behavior(begin) {
    std::cout << "[ArchC] Simulation Starting: {{ model_name }}" << std::endl;
}

void ac_behavior(end) {
    std::cout << "[ArchC] Simulation Completed: {{ model_name }}" << std::endl;
}

void ac_behavior(instruction) {
    ac_pc += 4;
}
void ac_behavior(Type_VV) {}
void ac_behavior(Type_VX) {}
void ac_behavior(Type_VI) {}
void ac_behavior(Type_MVV) {}


{% for inst in instructions %}
void ac_behavior({{ inst.mnemonic }}) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
{% if inst.binary_op %}
    {% if inst.format.value == "OPIVX" %}
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));
    {% elif inst.format.value == "OPIVI" %}
    int32_t op1 = (imm & 0x10) ? (imm - 0x20) : imm;
    {% else %}
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));
    {% endif %}
{% endif %}

    int32_t res = 0;
{% if inst.binary_op %}
    {% if inst.binary_op.name == "ADD" %}
    res = op2 + op1;
    {% elif inst.binary_op.name == "SUB" %}
    res = op2 - op1;
    {% elif inst.binary_op.name == "MUL" %}
    res = op2 * op1;
    {% elif inst.binary_op.name == "DIV" %}
    res = (op1 == 0) ? -1 : (op2 == INT32_MIN && op1 == -1 ? INT32_MIN : op2 / op1);
    {% elif inst.binary_op.name == "REM" %}
    res = (op1 == 0) ? op2 : (op2 == INT32_MIN && op1 == -1 ? 0 : op2 % op1);
    {% elif inst.binary_op.name == "AND" %}
    res = op2 & op1;
    {% elif inst.binary_op.name == "OR" %}
    res = op2 | op1;
    {% elif inst.binary_op.name == "XOR" %}
    res = op2 ^ op1;
    {% elif inst.binary_op.name == "SLL" %}
    res = op2 << (op1 & 31);
    {% elif inst.binary_op.name == "SRL" %}
    res = static_cast<int32_t>(static_cast<uint32_t>(op2) >> (op1 & 31));
    {% elif inst.binary_op.name == "SRA" %}
    res = op2 >> (op1 & 31);
    {% elif inst.binary_op.name == "MIN" %}
    res = std::min(op2, op1);
    {% elif inst.binary_op.name == "MAX" %}
    res = std::max(op2, op1);
    {% elif inst.binary_op.name == "SADD" %}
    res = clamp_i32(static_cast<int64_t>(op2) + static_cast<int64_t>(op1));
    {% elif inst.binary_op.name == "SSUB" %}
    res = clamp_i32(static_cast<int64_t>(op2) - static_cast<int64_t>(op1));
    {% else %}
    res = op2 + op1;
    {% endif %}
{% elif inst.unary_op %}
    {% if inst.unary_op.name == "NEG" %}
    res = 0 - op2;
    {% elif inst.unary_op.name == "NOT" %}
    res = ~op2;
    {% elif inst.unary_op.name == "ABS" %}
    res = (op2 == INT32_MIN) ? INT32_MIN : std::abs(op2);
    {% elif inst.unary_op.name == "CLZ" %}
    res = (op2 == 0) ? 32 : __builtin_clz(static_cast<uint32_t>(op2));
    {% elif inst.unary_op.name == "CTZ" %}
    res = (op2 == 0) ? 32 : __builtin_ctz(static_cast<uint32_t>(op2));
    {% elif inst.unary_op.name == "CPOP" %}
    res = __builtin_popcount(static_cast<uint32_t>(op2));
    {% else %}
    res = op2;
    {% endif %}
{% else %}
    res = op2;
{% endif %}

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "{{ inst.mnemonic }}", vd, res, vs2, op2);
}
{% endfor %}
""",

"main.cpp": r"""/******************************************************
 * SystemC Main Entrypoint for ArchC {{ model_name }} model  *
 * Generated automatically by random_vISA             *
 ******************************************************/

const char *project_name = "{{ model_name }}";
const char *project_file = "{{ model_name }}.ac";
const char *archc_version = "2.4.1";
const char *archc_options = "";

#include <iostream>
#include <fstream>
#include <string>
#include <systemc.h>
#include "ac_stats_base.H"
#include "{{ model_name }}.H"

static inline void write_word({{ model_name }} &proc, uint32_t addr, uint32_t val) {
    ac_ptr ptr(&val);
    proc.DM.write(ptr, addr, 32);
}

int sc_main(int ac, char *av[]) {
    std::cout << "============================================================" << std::endl;
    std::cout << "ArchC SystemC Simulator for {{ model_name }}" << std::endl;
    std::cout << "WordSize = 32 bits, Num Vector Regs = 32" << std::endl;
    std::cout << "============================================================" << std::endl;

    {{ model_name }} proc1("{{ model_name }}");

    bool has_app = false;
    std::string bin_path = "";
    for (int i = 1; i < ac; ++i) {
        std::string arg = av[i];
        if (arg.find("--load=") == 0) {
            has_app = true;
            break;
        } else if (arg == "--" && i + 1 < ac) {
            has_app = true;
            break;
        } else if (arg.find("--bin=") == 0) {
            bin_path = arg.substr(6);
        } else if (arg == "--bin" && i + 1 < ac) {
            bin_path = av[++i];
        }
    }

    if (has_app) {
        proc1.init(ac, av);
        proc1.set_prog_args();
    } else {
        std::cout << "\n[ArchC] Initializing SystemC Vector Processing Core..." << std::endl;
        proc1.init();
        proc1.dec_cache_size = 1048576;
        proc1.init_dec_cache();

        // Zero-initialize all register banks
        for (int i = 0; i < {{ config.num_vregs }}; ++i) {
            proc1.VRB.write(i, 0);
        }
        for (int i = 0; i < 32; ++i) {
            proc1.XRB.write(i, 0);
        }

        // Setup test register values
        proc1.VRB.write(1, 10);
        proc1.VRB.write(2, 2);
        proc1.XRB.write(1, 5);
        std::cout << "  State initialized: VRB[1] = 10, VRB[2] = 2, XRB[1] = 5" << std::endl;

        // NOTE: Load base is 0x100 to avoid ArchC reserved syscall stubs at 0x00-0xFF
        // (ac_forbidden is mapped to 0x3C by ArchC, so programs must start above that)
        if (!bin_path.empty()) {
            std::ifstream bf(bin_path, std::ios::binary);
            if (bf.is_open()) {
                uint32_t word = 0;
                uint32_t addr = 0x100;
                uint32_t n = 0;
                while (bf.read(reinterpret_cast<char*>(&word), 4)) {
                    write_word(proc1, addr, word);
                    addr += 4;
                    n++;
                }
                std::cout << "  Loaded " << n << " bytecode instructions from " << bin_path
                          << " at base 0x100" << std::endl;
            }
        } else {
            // Load all synthesized test instructions into DM (base 0x100)
            uint32_t addr = 0x100;
{% for inst in instructions %}
            // Instruction {{ inst.mnemonic }}
            uint32_t w{{ loop.index0 }} = (({{ inst.funct6 }} & 0x3F) << 26) | (1 << 25) | (2 << 20) | ({% if inst.format.value == "OPIVX" %}1{% elif inst.format.value == "OPIVI" %}5{% else %}1{% endif %} << 15) | ({{ inst.funct3 }} << 12) | (({{ (loop.index0 % (config.num_vregs - 4)) + 4 }}) << 7) | 0x57;
            write_word(proc1, addr, w{{ loop.index0 }});
            addr += 4;
{% endfor %}
            // Append halt sentinel
            write_word(proc1, addr, 0);
            addr += 4;
            std::cout << "  Loaded " << ((addr - 0x100) / 4 - 1) << " synthesized vector instructions into Memory DM." << std::endl;
        }

        proc1.set_ac_pc(0x100);
    }

    std::cout << "\n[ArchC] Starting SystemC Simulation Kernel (sc_start)..." << std::endl;
    sc_start();

    std::cout << "\n============================================================" << std::endl;
    std::cout << "[ArchC SystemC Register State Dump]:" << std::endl;
    for (int r = 0; r < {{ config.num_vregs }}; ++r) {
        int32_t val = static_cast<int32_t>(proc1.VRB.read(r));
        if (val != 0 || r <= 2)
            std::cout << "  VRB[" << r << "] = " << val << std::endl;
    }
    for (int r = 0; r < 4; ++r) {
        std::cout << "  XRB[" << r << "] = " << proc1.XRB.read(r) << std::endl;
    }
    std::cout << "============================================================" << std::endl;

    proc1.PrintStat();
    return 0;
}
""",

"build.sh": r"""#!/bin/sh
set -e

ARCHC_PATH="${ARCHC_PATH:-/Volumes/External/Code/ArchC}"
SYSTEMC_PATH="${SYSTEMC_PATH:-/opt/homebrew/opt/systemc}"
ACSIM_BIN="${ARCHC_PATH}/src/acsim/acsim"

echo "=== Running ArchC Simulator Generator (acsim -nw -nci) ==="
mkdir -p ~/.archc
cp -f "${ARCHC_PATH}/archc.conf" ~/.archc/archc.conf 2>/dev/null || true
"${ACSIM_BIN}" "{{ model_name }}.ac" -nw -nci

# Setup syscall stubs if missing
if [ ! -f {{ model_name }}_syscall.H ] && [ -f {{ model_name }}_syscall.H.tmpl ]; then
    cp {{ model_name }}_syscall.H.tmpl {{ model_name }}_syscall.H
fi
if [ ! -f {{ model_name }}_syscall.cpp ] && [ -f {{ model_name }}_syscall.cpp.tmpl ]; then
    cp {{ model_name }}_syscall.cpp.tmpl {{ model_name }}_syscall.cpp
fi

echo "=== Compiling SystemC Simulator with Clang++ (-O3 -march=native) ==="
clang++ -std=c++17 -O3 -march=native -DAC_MATCH_ENDIANNESS -Wno-deprecated \
  -Dstat64=stat -Dlstat64=lstat -Dfstat64=fstat \
  -I. \
  -I"${ARCHC_PATH}/src/aclib/ac_core" \
  -I"${ARCHC_PATH}/src/aclib/ac_decoder" \
  -I"${ARCHC_PATH}/src/aclib/ac_storage" \
  -I"${ARCHC_PATH}/src/aclib/ac_syscall" \
  -I"${ARCHC_PATH}/src/aclib/ac_utils" \
  -I"${ARCHC_PATH}/src/aclib/ac_stats" \
  -I"${ARCHC_PATH}/src/aclib/ac_gdb" \
  -I"${ARCHC_PATH}/src/aclib/ac_tlm" \
  -I"${ARCHC_PATH}/src/aclib/ac_rtld" \
  -I"${ARCHC_PATH}/src/aclib/ac_cache" \
  -I"${ARCHC_PATH}/src/aclib" \
  -I"${SYSTEMC_PATH}/include" \
  main.cpp {{ model_name }}_arch.cpp {{ model_name }}_arch_ref.cpp {{ model_name }}.cpp {{ model_name }}_syscall.cpp \
  "${ARCHC_PATH}/src/aclib/.libs/libarchc.a" \
  -L"${SYSTEMC_PATH}/lib" -lsystemc -lm \
  -o {{ model_name }}.x

echo "=== Successfully built SystemC simulator: {{ model_name }}.x ==="
"""
}


class ArchCEmitterAdapter(ArchCCodeEmitterPort):
    """Adapter for generating ArchC ADL specification files and SystemC simulator projects."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=DictLoader(ARCHC_TEMPLATES),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False,
        )

    def _get_format_tag(self, fmt: InstructionFormat) -> str:
        if fmt == InstructionFormat.OP_VV:
            return "VV"
        elif fmt == InstructionFormat.OP_VX:
            return "VX"
        elif fmt == InstructionFormat.OP_VI:
            return "VI"
        elif fmt == InstructionFormat.OP_MVV:
            return "MVV"
        return "VV"

    def _get_src_op_name(self, fmt: InstructionFormat) -> str:
        if fmt == InstructionFormat.OP_VX:
            return "rs1"
        elif fmt == InstructionFormat.OP_VI:
            return "imm"
        return "vs1"

    def emit_archc_project(self, spec: VectorIsaSpec, destination_dir: str) -> List[str]:
        os.makedirs(destination_dir, exist_ok=True)
        emitted_paths = []

        model_name = spec.name.lower()

        instructions_ctx = []
        for inst in spec.instructions:
            instructions_ctx.append({
                "mnemonic": inst.mnemonic,
                "format": inst.format,
                "format_tag": self._get_format_tag(inst.format),
                "src_op_name": self._get_src_op_name(inst.format),
                "funct6": inst.funct6,
                "funct3": inst.funct3,
                "binary_op": inst.binary_op,
                "unary_op": inst.unary_op,
            })

        context = {
            "model_name": model_name,
            "spec": spec,
            "config": spec.config,
            "instructions": instructions_ctx,
        }

        # 1. Emit <model_name>.ac
        ac_content = self.env.get_template("archc.ac").render(context)
        ac_path = os.path.join(destination_dir, f"{model_name}.ac")
        with open(ac_path, "w", encoding="utf-8") as f:
            f.write(ac_content)
        emitted_paths.append(ac_path)

        # 2. Emit <model_name>.isa
        isa_content = self.env.get_template("archc.isa").render(context)
        isa_path = os.path.join(destination_dir, f"{model_name}.isa")
        with open(isa_path, "w", encoding="utf-8") as f:
            f.write(isa_content)
        emitted_paths.append(isa_path)

        # 3. Emit <model_name>_isa.cpp
        bhv_content = self.env.get_template("archc_isa.cpp").render(context)
        bhv_path = os.path.join(destination_dir, f"{model_name}_isa.cpp")
        with open(bhv_path, "w", encoding="utf-8") as f:
            f.write(bhv_content)
        emitted_paths.append(bhv_path)

        # 4. Emit main.cpp
        main_content = self.env.get_template("main.cpp").render(context)
        main_path = os.path.join(destination_dir, "main.cpp")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(main_content)
        emitted_paths.append(main_path)

        # 5. Emit build.sh
        build_content = self.env.get_template("build.sh").render(context)
        build_path = os.path.join(destination_dir, "build.sh")
        with open(build_path, "w", encoding="utf-8") as f:
            f.write(build_content)
        os.chmod(build_path, 0o755)
        emitted_paths.append(build_path)

        return emitted_paths
