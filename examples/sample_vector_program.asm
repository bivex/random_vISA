# Example Vector Assembly Program for Synthesized VCPU
# Registers: v1 = [10, 20, 30, 40], v2 = [2, 4, 6, 8], x1 = 5

# Step 1: Multiply vector elements: v4 = v2 * v1 -> [20, 80, 180, 320]
vmul_vv_5  v4, v2, v1

# Step 2: Shift vector elements by scalar x1: v5 = v2 << x1 -> [64, 128, 192, 256]
vsll_vx_2  v5, v2, x1

# Step 3: Add results: v6 = v4 + v5 -> [84, 208, 372, 576]
vadd_vv_3  v6, v4, v5

# Step 4: Negate: v7 = -v6 -> [-84, -208, -372, -576]
vneg_m_0   v7, v6
