#include "visa_emulator.h"
#include <limits.h>

static inline int32_t clamp_i32(int64_t val) {
    if (val < (int64_t)INT32_MIN) return INT32_MIN;
    if (val > (int64_t)INT32_MAX) return INT32_MAX;
    return (int32_t)val;
}

static bool exec_vand_vv_0(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = op2 & op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = op2 & op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmax_vx_1(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vdiv_vx_2(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vxor_vx_3(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = op2 ^ op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = op2 ^ op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vdiv_vx_4(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmax_vv_5(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vdiv_vx_6(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op1 == 0) ? -1 : ((op2 == INT32_MIN && op1 == -1) ? INT32_MIN : (op2 / op1));
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vor_vx_7(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = op2 | op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = op2 | op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vsrl_vx_8(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vclz_m_9(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];


    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t res = 0;
            res = (op2 == 0) ? 32 : __builtin_clz((uint32_t)op2);
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t res = 0;
            res = (op2 == 0) ? 32 : __builtin_clz((uint32_t)op2);
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmin_vx_10(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 < op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 < op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmul_vv_11(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vsrl_vv_12(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 >> (op1 & 31u));
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vsadd_vx_13(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = clamp_i32((int64_t)op2 + (int64_t)op1);
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = clamp_i32((int64_t)op2 + (int64_t)op1);
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmul_vv_14(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t* vs1_ptr = (const int32_t*)state->vregs.regs[inst->vs1];

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = vs1_ptr[i];
            int32_t res = 0;
            res = (int32_t)((uint32_t)op2 * (uint32_t)op1);
            vd_ptr[i] = res;
        }
    }
    return true;
}
static bool exec_vmax_vx_15(EmulatorState* state, const DecodedInstruction* inst) {
    const size_t vl = (size_t)state->csr.vl;
    int32_t* vd_ptr  = (int32_t*)state->vregs.regs[inst->vd];
    const int32_t* vs2_ptr = (const int32_t*)state->vregs.regs[inst->vs2];

    const int32_t op1_scalar = (int32_t)visa_get_xreg(state, inst->rs1);

    if (__builtin_expect(inst->vm == 1, 1)) {
        // Fast-path: Unmasked loop with compiler auto-vectorization
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    } else {
        // Slow-path: Masked loop
        for (size_t i = 0; i < vl; ++i) {
            if (!visa_is_mask_set(state, 0, i)) continue;
            int32_t op2 = vs2_ptr[i];
            int32_t op1 = op1_scalar;
            int32_t res = 0;
            res = (op2 > op1) ? op2 : op1;
            vd_ptr[i] = res;
        }
    }
    return true;
}

// Direct Dispatch Table (64 funct6 x 8 funct3)
static const visa_instruction_handler_t dispatch_table[64][8] = {
    {
                exec_vand_vv_0,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vmax_vx_1,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vdiv_vx_2,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vxor_vx_3,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vdiv_vx_4,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
                exec_vmax_vv_5,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vdiv_vx_6,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vor_vx_7,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vsrl_vx_8,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
                exec_vclz_m_9,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vmin_vx_10,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
                exec_vmul_vv_11,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
                exec_vsrl_vv_12,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vsadd_vx_13,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
                exec_vmul_vv_14,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
                exec_vmax_vx_15,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
    {
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
    },
};

bool visa_execute(EmulatorState* state, const DecodedInstruction* inst) {
    if (inst->funct6 >= 64 || inst->funct3 >= 8) return false;
    visa_instruction_handler_t handler = dispatch_table[inst->funct6][inst->funct3];
    if (handler == NULL) return false;
    return handler(state, inst);
}