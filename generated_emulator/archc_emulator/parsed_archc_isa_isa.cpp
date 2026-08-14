/******************************************************
 * Behavior implementation for ArchC parsed_archc_isa model  *
 * Generated automatically by random_vISA               *
 ******************************************************/

#include <iostream>
#include <cstdio>
#include <cstdint>
#include <algorithm>
#include "parsed_archc_isa_isa.H"
#include "parsed_archc_isa_isa_init.cpp"
#include "parsed_archc_isa_bhv_macros.H"

using namespace parsed_archc_isa_parms;

static inline int32_t clamp_i32(int64_t val) {
    if (val < INT32_MIN) return INT32_MIN;
    if (val > INT32_MAX) return INT32_MAX;
    return static_cast<int32_t>(val);
}

void ac_behavior(begin) {
    std::cout << "[ArchC] Simulation Starting: parsed_archc_isa" << std::endl;
}

void ac_behavior(end) {
    std::cout << "[ArchC] Simulation Completed: parsed_archc_isa" << std::endl;
}

void ac_behavior(instruction) {
    ac_pc += 4;
}
void ac_behavior(Type_VV) {}
void ac_behavior(Type_VX) {}
void ac_behavior(Type_VI) {}
void ac_behavior(Type_MVV) {}


void ac_behavior(vand_vv_0) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));

    int32_t res = 0;
    res = op2 & op1;

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vand_vv_0", vd, res, vs2, op2);
}
void ac_behavior(vmax_vx_1) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = std::max(op2, op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmax_vx_1", vd, res, vs2, op2);
}
void ac_behavior(vdiv_vx_2) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = (op1 == 0) ? -1 : (op2 == INT32_MIN && op1 == -1 ? INT32_MIN : op2 / op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vdiv_vx_2", vd, res, vs2, op2);
}
void ac_behavior(vxor_vx_3) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = op2 ^ op1;

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vxor_vx_3", vd, res, vs2, op2);
}
void ac_behavior(vdiv_vx_4) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = (op1 == 0) ? -1 : (op2 == INT32_MIN && op1 == -1 ? INT32_MIN : op2 / op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vdiv_vx_4", vd, res, vs2, op2);
}
void ac_behavior(vmax_vv_5) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));

    int32_t res = 0;
    res = std::max(op2, op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmax_vv_5", vd, res, vs2, op2);
}
void ac_behavior(vdiv_vx_6) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = (op1 == 0) ? -1 : (op2 == INT32_MIN && op1 == -1 ? INT32_MIN : op2 / op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vdiv_vx_6", vd, res, vs2, op2);
}
void ac_behavior(vor_vx_7) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = op2 | op1;

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vor_vx_7", vd, res, vs2, op2);
}
void ac_behavior(vsrl_vx_8) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = static_cast<int32_t>(static_cast<uint32_t>(op2) >> (op1 & 31));

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vsrl_vx_8", vd, res, vs2, op2);
}
void ac_behavior(vclz_m_9) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));

    int32_t res = 0;
    res = (op2 == 0) ? 32 : __builtin_clz(static_cast<uint32_t>(op2));

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vclz_m_9", vd, res, vs2, op2);
}
void ac_behavior(vmin_vx_10) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = std::min(op2, op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmin_vx_10", vd, res, vs2, op2);
}
void ac_behavior(vmul_vv_11) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));

    int32_t res = 0;
    res = op2 * op1;

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmul_vv_11", vd, res, vs2, op2);
}
void ac_behavior(vsrl_vv_12) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));

    int32_t res = 0;
    res = static_cast<int32_t>(static_cast<uint32_t>(op2) >> (op1 & 31));

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vsrl_vv_12", vd, res, vs2, op2);
}
void ac_behavior(vsadd_vx_13) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = clamp_i32(static_cast<int64_t>(op2) + static_cast<int64_t>(op1));

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vsadd_vx_13", vd, res, vs2, op2);
}
void ac_behavior(vmul_vv_14) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(VRB.read(vs1));

    int32_t res = 0;
    res = op2 * op1;

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmul_vv_14", vd, res, vs2, op2);
}
void ac_behavior(vmax_vx_15) {
    int32_t op2 = static_cast<int32_t>(VRB.read(vs2));
    int32_t op1 = static_cast<int32_t>(XRB.read(rs1));

    int32_t res = 0;
    res = std::max(op2, op1);

    VRB.write(vd, static_cast<uint32_t>(res));
    printf("[ArchC] Executed %s: v%d = %d (from vs2=v%d[%d])\n",
           "vmax_vx_15", vd, res, vs2, op2);
}
