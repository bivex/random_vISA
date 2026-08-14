"""Outbound Adapter: Pure C11/C99 Emulator Code Emitter using Jinja2 Templates."""

import os
from typing import Dict, List, Any
from jinja2 import Environment, DictLoader
from random_visa.domain.model.types import InstructionFormat, BinaryOp, UnaryOp
from random_visa.domain.model.isa_spec import VectorIsaSpec


C_TEMPLATES = {
"visa_emulator.h": r"""#ifndef VISA_EMULATOR_H
#define VISA_EMULATOR_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>

#define VISA_VLEN {{ config.vlen }}
#define VISA_VLEN_BYTES (VISA_VLEN / 8)
#define VISA_NUM_VREGS {{ config.num_vregs }}
#define VISA_NUM_XREGS 32

typedef struct {
    uint64_t vl;
    uint64_t vtype;
    uint64_t vstart;
    uint64_t vxrm;
    uint64_t vxsat;
    uint64_t pc;
} CSRState;

typedef struct {
    _Alignas(64) uint8_t regs[VISA_NUM_VREGS][VISA_VLEN_BYTES];
} VRegFile;

typedef struct {
    VRegFile vregs;
    uint64_t xregs[VISA_NUM_XREGS];
    CSRState csr;
} EmulatorState;

typedef struct {
    const char* mnemonic;
    uint8_t opcode;
    uint8_t funct3;
    uint8_t funct6;
    uint8_t vd;
    uint8_t vs2;
    uint8_t vs1;
    uint8_t rs1;
    int8_t imm;
    uint8_t vm;
    uint32_t raw_word;
} DecodedInstruction;

// Function pointer type for direct dispatch
typedef bool (*visa_instruction_handler_t)(EmulatorState* state, const DecodedInstruction* inst);

void visa_emulator_init(EmulatorState* state);
void visa_emulator_reset(EmulatorState* state);
uint64_t visa_get_xreg(const EmulatorState* state, size_t idx);
void visa_set_xreg(EmulatorState* state, size_t idx, uint64_t val);
bool visa_is_mask_set(const EmulatorState* state, size_t mask_reg, size_t elem_idx);
void visa_dump_vregs(const EmulatorState* state);

DecodedInstruction visa_decode(uint32_t word);
bool visa_execute(EmulatorState* state, const DecodedInstruction* inst);
bool visa_step(EmulatorState* state, uint32_t word);
size_t visa_run_program(EmulatorState* state, const uint32_t* program, size_t count);

#endif // VISA_EMULATOR_H
""",

"visa_instructions.c": r"""#include "visa_emulator.h"
#include <limits.h>

static inline int32_t clamp_i32(int64_t val) {
    if (val < (int64_t)INT32_MIN) return INT32_MIN;
    if (val > (int64_t)INT32_MAX) return INT32_MAX;
    return (int32_t)val;
}

{% for inst in instructions %}
static bool exec_{{ inst.mnemonic }}(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

{% if inst.binary_op %}
    {% if inst.format.value == "OPIVV" or inst.format.value == "OPRED" or inst.format.value == "OPWVV" %}
    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];
    {% elif inst.format.value == "OPIVX" %}
    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);
    {% elif inst.format.value == "OPIVI" %}
    const int32_t op1_scalar = (int32_t)inst->imm;
    {% else %}
    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];
    {% endif %}
{% endif %}

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
{% if inst.binary_op %}
    {% if inst.format.value == "OPIVX" or inst.format.value == "OPIVI" %}
            int32_t op1 = op1_scalar;
    {% else %}
            int32_t op1 = vs1_ptr[i];
    {% endif %}
{% endif %}
            int32_t res = 0;
{% if inst.binary_op %}
    {% if inst.binary_op.name == "ADD" %}
            res = (int32_t)((uint32_t)op2 + (uint32_t)op1);
    {% elif inst.binary_op.name == "SUB" %}
            res = (int32_t)((uint32_t)op2 - (uint32_t)op1);
    {% elif inst.binary_op.name == "MUL" %}
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
    {% elif inst.binary_op.name == "DIV" %}
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
    {% elif inst.binary_op.name == "REM" %}
            res = (op1 == 0) ? op2 : ((op2 == INT32_MIN && op1 == -1) ? 0 : (op2 % op1));
    {% elif inst.binary_op.name == "AND" %}
            res = op2 & op1;
    {% elif inst.binary_op.name == "OR" %}
            res = op2 | op1;
    {% elif inst.binary_op.name == "XOR" %}
            res = op2 ^ op1;
    {% elif inst.binary_op.name == "SLL" %}
            res = (int32_t)((uint32_t)op2 << (op1 & 31u));
    {% elif inst.binary_op.name == "SRL" %}
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
    {% elif inst.binary_op.name == "SRA" %}
            res = (int32_t)(op2 >> (op1 & 31u));
    {% elif inst.binary_op.name == "MIN" %}
            res = (op2 < op1) ? op2 : op1;
    {% elif inst.binary_op.name == "MAX" %}
            res = (op2 > op1) ? op2 : op1;
    {% elif inst.binary_op.name == "SADD" %}
            res = clamp_i32((int64_t)op2 + (int64_t)op1);
    {% elif inst.binary_op.name == "SSUB" %}
            res = clamp_i32((int64_t)op2 - (int64_t)op1);
    {% else %}
            res = (int32_t)((uint32_t)op2 + (uint32_t)op1);
    {% endif %}
{% elif inst.unary_op %}
    {% if inst.unary_op.name == "NEG" %}
            res = (int32_t)(0u - (uint32_t)op2);
    {% elif inst.unary_op.name == "NOT" %}
            res = ~op2;
    {% elif inst.unary_op.name == "ABS" %}
            res = (op2 == INT32_MIN) ? INT32_MIN : ((op2 < 0) ? -op2 : op2);
    {% elif inst.unary_op.name == "CLZ" %}
            res = (op2 == 0) ? 32 : __builtin_clz((uint32_t)op2);
    {% elif inst.unary_op.name == "CTZ" %}
            res = (op2 == 0) ? 32 : __builtin_ctz((uint32_t)op2);
    {% elif inst.unary_op.name == "CPOP" %}
            res = __builtin_popcount((uint32_t)op2);
    {% else %}
            res = op2;
    {% endif %}
{% else %}
            res = op2;
{% endif %}
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
{% if inst.binary_op %}
    {% if inst.format.value == "OPIVX" or inst.format.value == "OPIVI" %}
            int32_t op1 = op1_scalar;
    {% else %}
            int32_t op1 = vs1_ptr[i];
    {% endif %}
{% endif %}
            int32_t res = 0;
{% if inst.binary_op %}
    {% if inst.binary_op.name == "ADD" %}
            res = (int32_t)((uint32_t)op2 + (uint32_t)op1);
    {% elif inst.binary_op.name == "SUB" %}
            res = (int32_t)((uint32_t)op2 - (uint32_t)op1);
    {% elif inst.binary_op.name == "MUL" %}
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
    {% elif inst.binary_op.name == "DIV" %}
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
    {% elif inst.binary_op.name == "REM" %}
            res = (op1 == 0) ? op2 : ((op2 == INT32_MIN && op1 == -1) ? 0 : (op2 % op1));
    {% elif inst.binary_op.name == "AND" %}
            res = op2 & op1;
    {% elif inst.binary_op.name == "OR" %}
            res = op2 | op1;
    {% elif inst.binary_op.name == "XOR" %}
            res = op2 ^ op1;
    {% elif inst.binary_op.name == "SLL" %}
            res = (int32_t)((uint32_t)op2 << (op1 & 31u));
    {% elif inst.binary_op.name == "SRL" %}
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
    {% elif inst.binary_op.name == "SRA" %}
            res = (int32_t)(op2 >> (op1 & 31u));
    {% elif inst.binary_op.name == "MIN" %}
            res = (op2 < op1) ? op2 : op1;
    {% elif inst.binary_op.name == "MAX" %}
            res = (op2 > op1) ? op2 : op1;
    {% elif inst.binary_op.name == "SADD" %}
            res = clamp_i32((int64_t)op2 + (int64_t)op1);
    {% elif inst.binary_op.name == "SSUB" %}
            res = clamp_i32((int64_t)op2 - (int64_t)op1);
    {% else %}
            res = (int32_t)((uint32_t)op2 + (uint32_t)op1);
    {% endif %}
{% elif inst.unary_op %}
    {% if inst.unary_op.name == "NEG" %}
            res = (int32_t)(0u - (uint32_t)op2);
    {% elif inst.unary_op.name == "NOT" %}
            res = ~op2;
    {% elif inst.unary_op.name == "ABS" %}
            res = (op2 == INT32_MIN) ? INT32_MIN : ((op2 < 0) ? -op2 : op2);
    {% elif inst.unary_op.name == "CLZ" %}
            res = (op2 == 0) ? 32 : __builtin_clz((uint32_t)op2);
    {% elif inst.unary_op.name == "CTZ" %}
            res = (op2 == 0) ? 32 : __builtin_ctz((uint32_t)op2);
    {% elif inst.unary_op.name == "CPOP" %}
            res = __builtin_popcount((uint32_t)op2);
    {% else %}
            res = op2;
    {% endif %}
{% else %}
            res = op2;
{% endif %}
            vd_ptr[i] = res;
        }
    }
    return true;
}
{% endfor %}

// Direct Dispatch Table (64 funct6 x 8 funct3)
static const visa_instruction_handler_t dispatch_table[64][8] = {
{% for f6 in range(64) %}
    {
    {% for f3 in range(8) %}
        {% set matched = false %}
        {% for inst in instructions %}
            {% if inst.funct6 == f6 and inst.funct3 == f3 %}
                exec_{{ inst.mnemonic }},
                {% set matched = true %}
            {% endif %}
        {% endfor %}
        {% if not matched %}
            NULL,
        {% endif %}
    {% endfor %}
    },
{% endfor %}
};

bool visa_execute(EmulatorState* state, const DecodedInstruction* inst) {
    if (inst->funct6 >= 64 || inst->funct3 >= 8) return false;
    visa_instruction_handler_t handler = dispatch_table[inst->funct6][inst->funct3];
    if (handler == NULL) return false;
    return handler(state, inst);
}
""",

"visa_emulator.c": r"""#include "visa_emulator.h"

void visa_emulator_init(EmulatorState* state) {
    memset(state, 0, sizeof(EmulatorState));
    state->csr.vl = VISA_VLEN / 32;
    state->csr.pc = 0x80000000;
}

void visa_emulator_reset(EmulatorState* state) {
    visa_emulator_init(state);
}

uint64_t visa_get_xreg(const EmulatorState* state, size_t idx) {
    if (idx == 0 || idx >= VISA_NUM_XREGS) return 0;
    return state->xregs[idx];
}

void visa_set_xreg(EmulatorState* state, size_t idx, uint64_t val) {
    if (idx > 0 && idx < VISA_NUM_XREGS) {
        state->xregs[idx] = val;
    }
}

bool visa_is_mask_set(const EmulatorState* state, size_t mask_reg, size_t elem_idx) {
    if (mask_reg >= VISA_NUM_VREGS) return false;
    size_t byte_idx = elem_idx / 8;
    size_t bit_idx = elem_idx % 8;
    if (byte_idx >= VISA_VLEN_BYTES) return false;
    return (state->vregs.regs[mask_reg][byte_idx] & (1 << bit_idx)) != 0;
}

void visa_dump_vregs(const EmulatorState* state) {
    for (size_t i = 0; i < VISA_NUM_VREGS; ++i) {
        printf("v%02zu: [ ", i);
        for (int b = (int)VISA_VLEN_BYTES - 1; b >= 0; --b) {
            printf("%02x ", state->vregs.regs[i][b]);
        }
        printf("]\n");
    }
}

DecodedInstruction visa_decode(uint32_t word) {
    DecodedInstruction dec;
    memset(&dec, 0, sizeof(DecodedInstruction));
    dec.raw_word = word;
    dec.opcode = word & 0x7F;
    dec.vd = (word >> 7) & 0x1F;
    dec.funct3 = (word >> 12) & 0x7;
    dec.vs1 = (word >> 15) & 0x1F;
    dec.rs1 = dec.vs1;
    int32_t imm5 = (int32_t)((word >> 15) & 0x1F);
    if (imm5 & 0x10) imm5 |= ~0x1F;
    dec.imm = (int8_t)imm5;
    dec.vs2 = (word >> 20) & 0x1F;
    dec.vm = (word >> 25) & 0x1;
    dec.funct6 = (word >> 26) & 0x3F;
    dec.mnemonic = "unknown";

    switch (dec.funct6) {
{% for inst in instructions %}
    case {{ inst.funct6 }}:
        if (dec.funct3 == {{ inst.funct3 }}) {
            dec.mnemonic = "{{ inst.mnemonic }}";
        }
        break;
{% endfor %}
    default:
        break;
    }
    return dec;
}

bool visa_step(EmulatorState* state, uint32_t word) {
    DecodedInstruction dec = visa_decode(word);
    if (dec.opcode != 0x57) return false;
    return visa_execute(state, &dec);
}

size_t visa_run_program(EmulatorState* state, const uint32_t* program, size_t count) {
    size_t executed = 0;
    for (size_t i = 0; i < count; ++i) {
        if (!visa_step(state, program[i])) break;
        executed++;
        state->csr.pc += 4;
    }
    return executed;
}
""",

"visa_main.c": r"""#include "visa_emulator.h"
#include <stdlib.h>

static void run_bytecode_file(EmulatorState* state, const char* filename) {
    FILE* f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Error: cannot open bytecode file %s\n", filename);
        return;
    }
    uint32_t program[4096];
    size_t count = fread(program, sizeof(uint32_t), 4096, f);
    fclose(f);

    printf("Executing C11 Bytecode Program (%zu instructions)...\n", count);
    for (size_t i = 0; i < count; ++i) {
        DecodedInstruction dec = visa_decode(program[i]);
        printf("  [%zu] PC=0x%llx Word=0x%08x (%s)... ", i + 1, (unsigned long long)state->csr.pc, program[i], dec.mnemonic);
        if (visa_step(state, program[i])) {
            int32_t* vd_ptr = (int32_t*)state->vregs.regs[dec.vd];
            printf("OK -> vd (v%d): [ ", (int)dec.vd);
            for (size_t e = 0; e < (size_t)state->csr.vl; ++e) {
                printf("%d ", vd_ptr[e]);
            }
            printf("]\n");
            state->csr.pc += 4;
        } else {
            printf("DECODE/EXECUTION FAILED!\n");
            return;
        }
    }
    printf("\n[Final Vector Register File Dump]:\n");
    visa_dump_vregs(state);
}

int main(int argc, char** argv) {
    EmulatorState state;
    visa_emulator_init(&state);
    state.csr.vl = 4;

    // Set initial test data: v1 = [10, 20, 30, 40], v2 = [2, 4, 6, 8], x1 = 5
    int32_t* v1 = (int32_t*)state.vregs.regs[1];
    int32_t* v2 = (int32_t*)state.vregs.regs[2];
    for (size_t i = 0; i < 4; ++i) {
        v1[i] = (int32_t)((i + 1) * 10);
        v2[i] = (int32_t)((i + 1) * 2);
    }
    visa_set_xreg(&state, 1, 5);

    if (argc >= 3 && strcmp(argv[1], "--bin") == 0) {
        run_bytecode_file(&state, argv[2]);
        return 0;
    }

    printf("============================================================\n");
    printf("Starting C11 Pure Vector ISA ({{ spec.name }}) Verification\n");
    printf("VLEN = %d bits, Num VRegs = %d\n", VISA_VLEN, VISA_NUM_VREGS);
    printf("============================================================\n");

    const uint32_t test_words[] = {
{% for inst in instructions %}
        {{ "0x%08X" % inst.encode(vd=3, vs2=2, vs1_or_rs1_or_imm=1, vm=1) }}u, // {{ inst.mnemonic }}
{% endfor %}
    };
    const size_t num_tests = sizeof(test_words) / sizeof(test_words[0]);
    size_t passed = 0;

    for (size_t i = 0; i < num_tests; ++i) {
        DecodedInstruction dec = visa_decode(test_words[i]);
        printf("[Test %zu/%zu] Executing %s (0x%08X)... ", i + 1, num_tests, dec.mnemonic, test_words[i]);
        if (visa_step(&state, test_words[i])) {
            int32_t* v3 = (int32_t*)state.vregs.regs[3];
            printf("SUCCESS -> v3: [ ");
            for (size_t e = 0; e < 4; ++e) {
                printf("%d ", v3[e]);
            }
            printf("]\n");
            passed++;
        } else {
            printf("FAILED!\n");
        }
    }

    printf("\nResults: %zu/%zu C11 tests passed.\n", passed, num_tests);
    return (passed == num_tests) ? 0 : 1;
}
""",

"Makefile": r"""CC ?= clang
CFLAGS ?= -std=c11 -O3 -Wall -Wextra -I.

SRCS = visa_emulator.c visa_instructions.c visa_main.c
OBJS = $(SRCS:.c=.o)
TARGET = visa_c_runner

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

%.o: %.c visa_emulator.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
"""
}


class CCodeEmitterAdapter:
    """Outbound adapter emitting pure C11 / C99 vector emulator projects."""

    def __init__(self):
        self.env = Environment(
            loader=DictLoader(C_TEMPLATES),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def emit_c_project(self, spec: VectorIsaSpec, output_dir: str) -> List[str]:
        """Emit all C11 source files into output_dir."""
        os.makedirs(output_dir, exist_ok=True)
        emitted: List[str] = []

        context = {
            "spec": spec,
            "config": spec.config,
            "instructions": spec.instructions,
            "range": range,
        }

        for filename in C_TEMPLATES.keys():
            template = self.env.get_template(filename)
            content = template.render(context)
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            emitted.append(filepath)

        return emitted
