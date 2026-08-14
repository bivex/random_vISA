#include "visa_emulator.h"
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
    printf("Starting C11 Pure Vector ISA (Parsed_C_ISA) Verification\n");
    printf("VLEN = %d bits, Num VRegs = %d\n", VISA_VLEN, VISA_NUM_VREGS);
    printf("============================================================\n");

    const uint32_t test_words[] = {
        0x022081D7u, // vand_vv_0
        0x0620C1D7u, // vmax_vx_1
        0x0A20C1D7u, // vdiv_vx_2
        0x0E20C1D7u, // vxor_vx_3
        0x1220C1D7u, // vdiv_vx_4
        0x162081D7u, // vmax_vv_5
        0x1A20C1D7u, // vdiv_vx_6
        0x1E20C1D7u, // vor_vx_7
        0x2220C1D7u, // vsrl_vx_8
        0x2620A1D7u, // vclz_m_9
        0x2A20C1D7u, // vmin_vx_10
        0x2E2081D7u, // vmul_vv_11
        0x322081D7u, // vsrl_vv_12
        0x3620C1D7u, // vsadd_vx_13
        0x3A2081D7u, // vmul_vv_14
        0x3E20C1D7u, // vmax_vx_15
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