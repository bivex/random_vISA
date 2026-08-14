"""Outbound Adapter: C++20 Emulator Code Emitter using Jinja2 Templates."""

import os
from typing import Dict, List, Any
from jinja2 import Environment, DictLoader
from random_visa.domain.model.types import InstructionFormat, BinaryOp, UnaryOp
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.ports.outbound.ports import CppCodeEmitterPort


TEMPLATES = {
"isa_state.hpp": r"""#pragma once
#include <cstdint>
#include <cstddef>
#include <array>
#include <vector>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <algorithm>

namespace visa_emulator {

constexpr size_t VLEN = {{ config.vlen }};
constexpr size_t VLEN_BYTES = VLEN / 8;
constexpr size_t NUM_VREGS = {{ config.num_vregs }};
constexpr size_t NUM_XREGS = 32;

struct CSRState {
    uint64_t vl{ {{ config.vlen // config.default_sew.value }} };
    uint64_t vtype{0};
    uint64_t vstart{0};
    uint64_t vxrm{0};
    uint64_t vxsat{0};
    uint64_t pc{0x80000000};
};

class VRegFile {
public:
    std::array<std::array<uint8_t, VLEN_BYTES>, NUM_VREGS> regs{};

    void reset() {
        for (auto& r : regs) {
            r.fill(0);
        }
    }

    template <typename T>
    T get_elem(size_t reg_idx, size_t elem_idx) const {
        if (reg_idx >= NUM_VREGS) return 0;
        size_t offset = elem_idx * sizeof(T);
        if (offset + sizeof(T) > VLEN_BYTES) return 0;
        T val;
        std::memcpy(&val, &regs[reg_idx][offset], sizeof(T));
        return val;
    }

    template <typename T>
    void set_elem(size_t reg_idx, size_t elem_idx, T val) {
        if (reg_idx >= NUM_VREGS) return;
        size_t offset = elem_idx * sizeof(T);
        if (offset + sizeof(T) > VLEN_BYTES) return;
        std::memcpy(&regs[reg_idx][offset], &val, sizeof(T));
    }

    bool is_mask_set(size_t mask_reg, size_t elem_idx) const {
        if (mask_reg >= NUM_VREGS) return false;
        size_t byte_idx = elem_idx / 8;
        size_t bit_idx = elem_idx % 8;
        if (byte_idx >= VLEN_BYTES) return false;
        return (regs[mask_reg][byte_idx] & (1 << bit_idx)) != 0;
    }

    void dump(std::ostream& os = std::cout) const {
        for (size_t i = 0; i < NUM_VREGS; ++i) {
            os << "v" << std::setw(2) << std::setfill('0') << i << ": [ ";
            for (int b = static_cast<int>(VLEN_BYTES) - 1; b >= 0; --b) {
                os << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(regs[i][b]) << " ";
            }
            os << std::dec << "]\n";
        }
    }
};

struct EmulatorState {
    VRegFile vregs;
    std::array<uint64_t, NUM_XREGS> xregs{};
    CSRState csr;

    void reset() {
        vregs.reset();
        xregs.fill(0);
        csr = CSRState{};
    }

    uint64_t get_xreg(size_t idx) const {
        if (idx == 0 || idx >= NUM_XREGS) return 0;
        return xregs[idx];
    }

    void set_xreg(size_t idx, uint64_t val) {
        if (idx > 0 && idx < NUM_XREGS) {
            xregs[idx] = val;
        }
    }
};

} // namespace visa_emulator
""",

"decoder.hpp": r"""#pragma once
#include <cstdint>
#include <string_view>
#include <optional>

namespace visa_emulator {

enum class InstId {
    UNKNOWN = 0,
{% for inst in instructions %}
    {{ inst.mnemonic.upper() }},
{% endfor %}
};

struct DecodedInstruction {
    InstId id{InstId::UNKNOWN};
    std::string_view mnemonic{"unknown"};
    uint8_t opcode{0};
    uint8_t funct3{0};
    uint8_t funct6{0};
    uint8_t vd{0};
    uint8_t vs2{0};
    uint8_t vs1{0};
    uint8_t rs1{0};
    int8_t imm{0};
    uint8_t vm{1};
    uint32_t raw_word{0};
};

class Decoder {
public:
    static DecodedInstruction decode(uint32_t word) {
        DecodedInstruction dec;
        dec.raw_word = word;
        dec.opcode = word & 0x7F;
        dec.vd = (word >> 7) & 0x1F;
        dec.funct3 = (word >> 12) & 0x7;
        dec.vs1 = (word >> 15) & 0x1F;
        dec.rs1 = dec.vs1;
        int32_t imm5 = static_cast<int32_t>((word >> 15) & 0x1F);
        if (imm5 & 0x10) imm5 |= ~0x1F;
        dec.imm = static_cast<int8_t>(imm5);
        dec.vs2 = (word >> 20) & 0x1F;
        dec.vm = (word >> 25) & 0x1;
        dec.funct6 = (word >> 26) & 0x3F;

        if (dec.opcode != 0x57) {
            return dec;
        }

        switch (dec.funct6) {
{% for inst in instructions %}
        case {{ inst.funct6 }}:
            if (dec.funct3 == {{ inst.funct3 }}) {
                dec.id = InstId::{{ inst.mnemonic.upper() }};
                dec.mnemonic = "{{ inst.mnemonic }}";
                return dec;
            }
            break;
{% endfor %}
        default:
            break;
        }
        return dec;
    }
};

} // namespace visa_emulator
""",

"instructions.hpp": r"""#pragma once
#include "isa_state.hpp"
#include "decoder.hpp"

namespace visa_emulator {

class InstructionExecutor {
public:
    static bool execute(EmulatorState& state, const DecodedInstruction& inst);

private:
{% for inst in instructions %}
    static void exec_{{ inst.mnemonic }}(EmulatorState& state, const DecodedInstruction& inst);
{% endfor %}
};

} // namespace visa_emulator
""",

"instructions.cpp": r"""#include "instructions.hpp"
#include <algorithm>

namespace visa_emulator {

bool InstructionExecutor::execute(EmulatorState& state, const DecodedInstruction& inst) {
    switch (inst.id) {
{% for inst in instructions %}
    case InstId::{{ inst.mnemonic.upper() }}:
        exec_{{ inst.mnemonic }}(state, inst);
        return true;
{% endfor %}
    default:
        return false;
    }
}

{% for inst in instructions %}
void InstructionExecutor::exec_{{ inst.mnemonic }}(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
{% if inst.binary_op %}
    {% if inst.format.value == "OPIVV" or inst.format.value == "OPRED" or inst.format.value == "OPWVV" %}
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);
    {% elif inst.format.value == "OPIVX" %}
        elem_t op1 = static_cast<elem_t>(state.get_xreg(inst.rs1));
    {% elif inst.format.value == "OPIVI" %}
        elem_t op1 = static_cast<elem_t>(inst.imm);
    {% else %}
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);
    {% endif %}
{% endif %}

        elem_t result = 0;
{% if inst.binary_op %}
    {% if inst.binary_op.name == "ADD" %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) + static_cast<uint32_t>(op1));
    {% elif inst.binary_op.name == "SUB" %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) - static_cast<uint32_t>(op1));
    {% elif inst.binary_op.name == "MUL" %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) * static_cast<uint32_t>(op1));
    {% elif inst.binary_op.name == "DIV" %}
        if (op1 == 0) {
            result = -1;
        } else if (op2 == INT32_MIN && op1 == -1) {
            result = INT32_MIN;
        } else {
            result = op2 / op1;
        }
    {% elif inst.binary_op.name == "REM" %}
        if (op1 == 0) {
            result = op2;
        } else if (op2 == INT32_MIN && op1 == -1) {
            result = 0;
        } else {
            result = op2 % op1;
        }
    {% elif inst.binary_op.name == "AND" %}
        result = op2 & op1;
    {% elif inst.binary_op.name == "OR" %}
        result = op2 | op1;
    {% elif inst.binary_op.name == "XOR" %}
        result = op2 ^ op1;
    {% elif inst.binary_op.name == "SLL" %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) << (static_cast<uint32_t>(op1) & 31u));
    {% elif inst.binary_op.name == "SRL" %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) >> (static_cast<uint32_t>(op1) & 31u));
    {% elif inst.binary_op.name == "SRA" %}
        result = static_cast<elem_t>(op2 >> (static_cast<uint32_t>(op1) & 31u));
    {% elif inst.binary_op.name == "MIN" %}
        result = std::min(op2, op1);
    {% elif inst.binary_op.name == "MAX" %}
        result = std::max(op2, op1);
    {% elif inst.binary_op.name == "SADD" %}
        int64_t sum = static_cast<int64_t>(op2) + static_cast<int64_t>(op1);
        result = static_cast<elem_t>(std::clamp<int64_t>(sum, INT32_MIN, INT32_MAX));
    {% elif inst.binary_op.name == "SSUB" %}
        int64_t diff = static_cast<int64_t>(op2) - static_cast<int64_t>(op1);
        result = static_cast<elem_t>(std::clamp<int64_t>(diff, INT32_MIN, INT32_MAX));
    {% else %}
        result = static_cast<elem_t>(static_cast<uint32_t>(op2) + static_cast<uint32_t>(op1));
    {% endif %}
{% elif inst.unary_op %}
    {% if inst.unary_op.name == "NEG" %}
        result = static_cast<elem_t>(0u - static_cast<uint32_t>(op2));
    {% elif inst.unary_op.name == "NOT" %}
        result = ~op2;
    {% elif inst.unary_op.name == "ABS" %}
        result = (op2 == INT32_MIN) ? INT32_MIN : ((op2 < 0) ? -op2 : op2);
    {% elif inst.unary_op.name == "CLZ" %}
        result = (op2 == 0) ? 32 : __builtin_clz(static_cast<uint32_t>(op2));
    {% elif inst.unary_op.name == "CTZ" %}
        result = (op2 == 0) ? 32 : __builtin_ctz(static_cast<uint32_t>(op2));
    {% elif inst.unary_op.name == "CPOP" %}
        result = __builtin_popcount(static_cast<uint32_t>(op2));
    {% else %}
        result = op2;
    {% endif %}
{% else %}
        result = op2;
{% endif %}

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
{% endfor %}

} // namespace visa_emulator
""",

"emulator.hpp": r"""#pragma once
#include "isa_state.hpp"
#include "decoder.hpp"
#include "instructions.hpp"
#include <vector>
#include <string>

namespace visa_emulator {

class VectorEmulator {
public:
    EmulatorState state;

    VectorEmulator() {
        state.reset();
    }

    void reset() {
        state.reset();
    }

    bool step(uint32_t instruction_word) {
        DecodedInstruction dec = Decoder::decode(instruction_word);
        if (dec.id == InstId::UNKNOWN) {
            return false;
        }
        return InstructionExecutor::execute(state, dec);
    }

    size_t run_program(const std::vector<uint32_t>& program) {
        size_t executed = 0;
        for (uint32_t word : program) {
            if (!step(word)) {
                break;
            }
            executed++;
            state.csr.pc += 4;
        }
        return executed;
    }
};

} // namespace visa_emulator
""",

"main.cpp": r"""#include "emulator.hpp"
#include "decoder.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cassert>

using namespace visa_emulator;

void run_custom_bytecode(VectorEmulator& emu, const std::vector<uint32_t>& program) {
    std::cout << "Executing Bytecode Program (" << program.size() << " instructions)...\n";
    for (size_t idx = 0; idx < program.size(); ++idx) {
        uint32_t word = program[idx];
        DecodedInstruction dec = Decoder::decode(word);
        std::cout << "  [" << idx + 1 << "] PC=0x" << std::hex << emu.state.csr.pc
                  << " Word=0x" << word << " (" << dec.mnemonic << ")... " << std::dec;
        bool ok = emu.step(word);
        if (ok) {
            std::cout << "OK -> vd (v" << static_cast<int>(dec.vd) << "): [ ";
            for (size_t elem = 0; elem < static_cast<size_t>(emu.state.csr.vl); ++elem) {
                std::cout << emu.state.vregs.get_elem<int32_t>(dec.vd, elem) << " ";
            }
            std::cout << "]\n";
            emu.state.csr.pc += 4;
        } else {
            std::cout << "DECODE/EXECUTION FAILED!\n";
            return;
        }
    }

    std::cout << "\n[Final Vector Register File Dump]:\n";
    emu.state.vregs.dump(std::cout);
}

int main(int argc, char** argv) {
    VectorEmulator emu;
    emu.reset();
    emu.state.csr.vl = 4; // Set vector length to 4 elements (32-bit each)

    // Pre-populate source registers v1 and v2 with test data
    for (size_t i = 0; i < 4; ++i) {
        emu.state.vregs.set_elem<int32_t>(1, i, static_cast<int32_t>((i + 1) * 10)); // v1 = [10, 20, 30, 40]
        emu.state.vregs.set_elem<int32_t>(2, i, static_cast<int32_t>((i + 1) * 2));  // v2 = [2, 4, 6, 8]
    }
    emu.state.set_xreg(1, 5); // x1 = 5

    // Check for --bin <filename> argument
    if (argc >= 3 && std::string(argv[1]) == "--bin") {
        std::string filename = argv[2];
        std::ifstream file(filename, std::ios::binary);
        if (!file.is_open()) {
            std::cerr << "Error: cannot open binary bytecode file " << filename << "\n";
            return 1;
        }
        std::vector<uint32_t> program;
        uint32_t word;
        while (file.read(reinterpret_cast<char*>(&word), sizeof(uint32_t))) {
            program.push_back(word);
        }
        run_custom_bytecode(emu, program);
        return 0;
    }

    // Check for --hex <word1> <word2> ... argument
    if (argc >= 3 && std::string(argv[1]) == "--hex") {
        std::vector<uint32_t> program;
        for (int i = 2; i < argc; ++i) {
            uint32_t word = static_cast<uint32_t>(std::stoul(argv[i], nullptr, 0));
            program.push_back(word);
        }
        run_custom_bytecode(emu, program);
        return 0;
    }

    // Default verification suite
    std::cout << "============================================================\n";
    std::cout << "Starting Vector ISA ({{ spec.name }}) Emulator Verification Suite\n";
    std::cout << "VLEN = " << VLEN << " bits, Num VRegs = " << NUM_VREGS << "\n";
    std::cout << "============================================================\n";

    std::cout << "[Initial Register State]\n";
    std::cout << "v1: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(1, i) << " ";
    std::cout << "\nv2: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(2, i) << " ";
    std::cout << "\nx1: " << emu.state.get_xreg(1) << "\n\n";

    std::vector<uint32_t> test_words = {
{% for inst in instructions %}
        // {{ inst.mnemonic }} (funct6={{ inst.funct6 }}, funct3={{ inst.funct3 }})
        {{ "0x%08X" % inst.encode(vd=3, vs2=2, vs1_or_rs1_or_imm=1, vm=1) }}u,
{% endfor %}
    };

    size_t passed = 0;
    for (size_t idx = 0; idx < test_words.size(); ++idx) {
        uint32_t word = test_words[idx];
        DecodedInstruction dec = Decoder::decode(word);
        std::cout << "[Test " << idx + 1 << "/" << test_words.size() << "] Executing "
                  << dec.mnemonic << " (0x" << std::hex << word << std::dec << ")... ";

        bool ok = emu.step(word);
        if (ok) {
            std::cout << "SUCCESS -> v3: [ ";
            for (size_t elem = 0; elem < 4; ++elem) {
                std::cout << emu.state.vregs.get_elem<int32_t>(3, elem) << " ";
            }
            std::cout << "]\n";
            passed++;
        } else {
            std::cout << "FAILED to decode/execute!\n";
        }
    }

    std::cout << "\n============================================================\n";
    std::cout << "Results: " << passed << "/" << test_words.size() << " instructions executed successfully.\n";
    std::cout << "============================================================\n";

    return (passed == test_words.size()) ? 0 : 1;
}
""",

"CMakeLists.txt": r"""cmake_minimum_required(VERSION 3.16)
project({{ spec.name }}_emulator CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -Wextra")

add_executable(visa_test_runner
    main.cpp
    instructions.cpp
)

target_include_directories(visa_test_runner PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
"""
}


class CppEmulatorEmitterAdapter(CppCodeEmitterPort):
    """C++20 Emulator Code Emitter implementation using Jinja2."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=DictLoader(TEMPLATES),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False,
        )

    def emit_emulator_project(
        self,
        spec: VectorIsaSpec,
        destination_dir: str,
    ) -> Dict[str, str]:
        os.makedirs(destination_dir, exist_ok=True)
        results: Dict[str, str] = {}

        context = {
            "spec": spec,
            "config": spec.config,
            "instructions": spec.instructions,
        }

        for template_name in TEMPLATES.keys():
            tmpl = self.env.get_template(template_name)
            content = tmpl.render(context)
            out_file = os.path.join(destination_dir, template_name)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(content)
            results[template_name] = content

        return results
