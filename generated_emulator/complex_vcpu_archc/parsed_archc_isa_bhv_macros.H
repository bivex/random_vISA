#ifndef _PARSED_ARCHC_ISA_BHV_MACROS_H
#define _PARSED_ARCHC_ISA_BHV_MACROS_H

typedef ac_memport<parsed_archc_isa_parms::ac_word, parsed_archc_isa_parms::ac_Hword> ac_memory;

#define ac_behavior(instr) AC_BEHAVIOR_##instr ()

#define AC_BEHAVIOR_instruction() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_instruction(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t funct3, uint8_t vd, uint8_t opcode)

#define AC_BEHAVIOR_begin() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_begin()
#define AC_BEHAVIOR_end() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_end()

#define AC_BEHAVIOR_Type_VV() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_parsed_archc_isa_Type_VV(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_Type_VX() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_parsed_archc_isa_Type_VX(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_Type_VI() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_parsed_archc_isa_Type_VI(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t imm, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_Type_MVV() parsed_archc_isa_parms::parsed_archc_isa_isa::_behavior_parsed_archc_isa_Type_MVV(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)

#define AC_BEHAVIOR_vclz_m_0() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vclz_m_0(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vor_vi_1() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vor_vi_1(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t imm, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vxor_vx_2() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vxor_vx_2(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmin_vx_3() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmin_vx_3(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsadd_vx_4() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsadd_vx_4(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsra_vx_5() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsra_vx_5(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vrem_vx_6() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vrem_vx_6(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vabs_m_7() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vabs_m_7(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vclz_m_8() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vclz_m_8(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsrl_vx_9() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsrl_vx_9(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vcpop_m_10() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vcpop_m_10(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vcpop_m_11() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vcpop_m_11(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vrem_vv_12() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vrem_vv_12(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vxor_vx_13() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vxor_vx_13(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmax_vx_14() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmax_vx_14(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vrem_vv_15() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vrem_vv_15(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vxor_vx_16() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vxor_vx_16(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vdiv_vv_17() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vdiv_vv_17(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vabs_m_18() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vabs_m_18(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vxor_vv_19() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vxor_vv_19(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vclz_m_20() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vclz_m_20(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vnot_m_21() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vnot_m_21(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmin_vv_22() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmin_vv_22(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vcpop_m_23() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vcpop_m_23(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vor_vx_24() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vor_vx_24(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmul_vv_25() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmul_vv_25(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vcpop_m_26() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vcpop_m_26(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vdiv_vx_27() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vdiv_vx_27(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vclz_m_28() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vclz_m_28(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsrl_vx_29() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsrl_vx_29(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsadd_vv_30() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsadd_vv_30(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vadd_vx_31() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vadd_vx_31(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)


#endif //_PARSED_ARCHC_ISA_BHV_MACROS_H

