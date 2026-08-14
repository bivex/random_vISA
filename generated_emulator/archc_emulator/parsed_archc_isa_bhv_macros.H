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

#define AC_BEHAVIOR_vand_vv_0() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vand_vv_0(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmax_vx_1() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmax_vx_1(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vdiv_vx_2() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vdiv_vx_2(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vxor_vx_3() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vxor_vx_3(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vdiv_vx_4() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vdiv_vx_4(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmax_vv_5() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmax_vv_5(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vdiv_vx_6() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vdiv_vx_6(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vor_vx_7() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vor_vx_7(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsrl_vx_8() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsrl_vx_8(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vclz_m_9() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vclz_m_9(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmin_vx_10() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmin_vx_10(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmul_vv_11() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmul_vv_11(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsrl_vv_12() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsrl_vv_12(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vsadd_vx_13() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vsadd_vx_13(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmul_vv_14() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmul_vv_14(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t vs1, uint8_t funct3, uint8_t vd, uint8_t opcode)
#define AC_BEHAVIOR_vmax_vx_15() parsed_archc_isa_parms::parsed_archc_isa_isa::behavior_vmax_vx_15(uint8_t funct6, uint8_t vm, uint8_t vs2, uint8_t rs1, uint8_t funct3, uint8_t vd, uint8_t opcode)


#endif //_PARSED_ARCHC_ISA_BHV_MACROS_H

