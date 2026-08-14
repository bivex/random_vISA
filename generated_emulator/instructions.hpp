#pragma once
#include "isa_state.hpp"
#include "decoder.hpp"

namespace visa_emulator {

class InstructionExecutor {
public:
    static bool execute(EmulatorState& state, const DecodedInstruction& inst) noexcept;

private:
    static void exec_vand_vv_0(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmax_vx_1(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vdiv_vx_2(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vxor_vx_3(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vdiv_vx_4(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmax_vv_5(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vdiv_vx_6(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vor_vx_7(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vsrl_vx_8(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vclz_m_9(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmin_vx_10(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmul_vv_11(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vsrl_vv_12(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vsadd_vx_13(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmul_vv_14(EmulatorState& state, const DecodedInstruction& inst) noexcept;
    static void exec_vmax_vx_15(EmulatorState& state, const DecodedInstruction& inst) noexcept;
};

} // namespace visa_emulator