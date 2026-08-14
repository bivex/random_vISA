#include "instructions.hpp"
#include <algorithm>

namespace visa_emulator {

bool InstructionExecutor::execute(EmulatorState& state, const DecodedInstruction& inst) {
    switch (inst.id) {
    case InstId::VADD_VI_0:
        exec_vadd_vi_0(state, inst);
        return true;
    case InstId::VAND_VV_1:
        exec_vand_vv_1(state, inst);
        return true;
    case InstId::VMAX_VV_2:
        exec_vmax_vv_2(state, inst);
        return true;
    case InstId::VADD_VV_3:
        exec_vadd_vv_3(state, inst);
        return true;
    case InstId::VNOT_M_4:
        exec_vnot_m_4(state, inst);
        return true;
    case InstId::VSADD_VX_5:
        exec_vsadd_vx_5(state, inst);
        return true;
    case InstId::VCTZ_M_6:
        exec_vctz_m_6(state, inst);
        return true;
    case InstId::VADD_VV_7:
        exec_vadd_vv_7(state, inst);
        return true;
    default:
        return false;
    }
}

void InstructionExecutor::exec_vadd_vi_0(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = static_cast<elem_t>(inst.imm);

        elem_t result = 0;
        result = op2 + op1;

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vand_vv_1(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);

        elem_t result = 0;
        result = op2 & op1;

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vmax_vv_2(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);

        elem_t result = 0;
        result = std::max(op2, op1);

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vadd_vv_3(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);

        elem_t result = 0;
        result = op2 + op1;

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vnot_m_4(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);

        elem_t result = 0;
        result = ~op2;

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vsadd_vx_5(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = static_cast<elem_t>(state.get_xreg(inst.rs1));

        elem_t result = 0;
        int64_t sum = static_cast<int64_t>(op2) + static_cast<int64_t>(op1);
        result = static_cast<elem_t>(std::clamp<int64_t>(sum, INT32_MIN, INT32_MAX));

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vctz_m_6(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);

        elem_t result = 0;
        result = (op2 == 0) ? 32 : __builtin_ctz(static_cast<uint32_t>(op2));

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}
void InstructionExecutor::exec_vadd_vv_7(EmulatorState& state, const DecodedInstruction& inst) {
    using elem_t = int32_t;
    const size_t vl = static_cast<size_t>(state.csr.vl);
    
    for (size_t i = 0; i < vl; ++i) {
        if (inst.vm == 0 && !state.vregs.is_mask_set(0, i)) {
            continue; // Masked out
        }
        
        elem_t op2 = state.vregs.get_elem<elem_t>(inst.vs2, i);
        elem_t op1 = state.vregs.get_elem<elem_t>(inst.vs1, i);

        elem_t result = 0;
        result = op2 + op1;

        state.vregs.set_elem<elem_t>(inst.vd, i, result);
    }
}

} // namespace visa_emulator