#include "instructions.hpp"
#include <algorithm>

namespace visa_emulator {

bool InstructionExecutor::execute(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    switch (inst.id) {
    case InstId::VAND_VV_0:
        exec_vand_vv_0(state, inst);
        return true;
    case InstId::VMAX_VX_1:
        exec_vmax_vx_1(state, inst);
        return true;
    case InstId::VDIV_VX_2:
        exec_vdiv_vx_2(state, inst);
        return true;
    case InstId::VXOR_VX_3:
        exec_vxor_vx_3(state, inst);
        return true;
    case InstId::VDIV_VX_4:
        exec_vdiv_vx_4(state, inst);
        return true;
    case InstId::VMAX_VV_5:
        exec_vmax_vv_5(state, inst);
        return true;
    case InstId::VDIV_VX_6:
        exec_vdiv_vx_6(state, inst);
        return true;
    case InstId::VOR_VX_7:
        exec_vor_vx_7(state, inst);
        return true;
    case InstId::VSRL_VX_8:
        exec_vsrl_vx_8(state, inst);
        return true;
    case InstId::VCLZ_M_9:
        exec_vclz_m_9(state, inst);
        return true;
    case InstId::VMIN_VX_10:
        exec_vmin_vx_10(state, inst);
        return true;
    case InstId::VMUL_VV_11:
        exec_vmul_vv_11(state, inst);
        return true;
    case InstId::VSRL_VV_12:
        exec_vsrl_vv_12(state, inst);
        return true;
    case InstId::VSADD_VX_13:
        exec_vsadd_vx_13(state, inst);
        return true;
    case InstId::VMUL_VV_14:
        exec_vmul_vv_14(state, inst);
        return true;
    case InstId::VMAX_VX_15:
        exec_vmax_vx_15(state, inst);
        return true;
    default:
        return false;
    }
}

void InstructionExecutor::exec_vand_vv_0(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const auto* vs1_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = op2 & op1;
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = op2 & op1;
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmax_vx_1(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vdiv_vx_2(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vxor_vx_3(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = op2 ^ op1;
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = op2 ^ op1;
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vdiv_vx_4(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmax_vv_5(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const auto* vs1_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vdiv_vx_6(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            if (op1 == 0) {
                result = -1;
            } else if (op2 == INT32_MIN && op1 == -1) {
                result = INT32_MIN;
            } else {
                result = op2 / op1;
            }
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vor_vx_7(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = op2 | op1;
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = op2 | op1;
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vsrl_vx_8(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) >> (op1 & 31u));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) >> (op1 & 31u));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vclz_m_9(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));


    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t result = 0;
            result = (op2 == 0) ? 32 : __builtin_clz(static_cast<uint32_t>(op2));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t result = 0;
            result = (op2 == 0) ? 32 : __builtin_clz(static_cast<uint32_t>(op2));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmin_vx_10(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::min(op2, op1);
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::min(op2, op1);
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmul_vv_11(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const auto* vs1_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) * static_cast<uint32_t>(op1));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) * static_cast<uint32_t>(op1));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vsrl_vv_12(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const auto* vs1_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) >> (op1 & 31u));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) >> (op1 & 31u));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vsadd_vx_13(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = static_cast<elem_t>(std::clamp<int64_t>(static_cast<int64_t>(op2) + op1, INT32_MIN, INT32_MAX));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = static_cast<elem_t>(std::clamp<int64_t>(static_cast<int64_t>(op2) + op1, INT32_MIN, INT32_MAX));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmul_vv_14(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const auto* vs1_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) * static_cast<uint32_t>(op1));
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = vs1_ptr[i];
            elem_t result = 0;
            result = static_cast<elem_t>(static_cast<uint32_t>(op2) * static_cast<uint32_t>(op1));
            vd_ptr[i] = result;
        }
    }
}
void InstructionExecutor::exec_vmax_vx_15(EmulatorState& state, const DecodedInstruction& inst) noexcept {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    auto* vd_ptr  = reinterpret_cast<elem_t*>(state.vregs.get_reg_ptr(inst.vd));
    const auto* vs2_ptr = reinterpret_cast<const elem_t*>(state.vregs.get_reg_ptr(inst.vs2));

    const elem_t op1_scalar = static_cast<elem_t>(state.get_xreg(inst.rs1));

    if (__builtin_expect(inst.vm == 1, 1)) {
        // Fast-path: Unmasked vectorized execution
        #pragma clang loop vectorize(enable)
        for (size_t i = 0; i < vl; ++i) {
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    } else {
        // Slow-path: Masked execution
        for (size_t i = 0; i < vl; ++i) {
            if (!state.vregs.is_mask_set(0, i)) continue;
            elem_t op2 = vs2_ptr[i];
            elem_t op1 = op1_scalar;
            elem_t result = 0;
            result = std::max(op2, op1);
            vd_ptr[i] = result;
        }
    }
}

} // namespace visa_emulator