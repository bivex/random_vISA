#ifndef VISA_EMULATOR_H
#define VISA_EMULATOR_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>

#define VISA_VLEN 256
#define VISA_VLEN_BYTES (VISA_VLEN / 8)
#define VISA_NUM_VREGS 32
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