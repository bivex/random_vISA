#pragma once
#include <cstdint>
#include <cstddef>
#include <array>
#include <vector>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <algorithm>

namespace visa_emulator {

constexpr size_t VLEN = 256;
constexpr size_t VLEN_BYTES = VLEN / 8;
constexpr size_t NUM_VREGS = 32;
constexpr size_t NUM_XREGS = 32;

struct CSRState {
    uint64_t vl{ 8 };
    uint64_t vtype{0};
    uint64_t vstart{0};
    uint64_t vxrm{0};
    uint64_t vxsat{0};
    uint64_t pc{0x80000000};
};

class VRegFile {
public:
    alignas(64) std::array<std::array<uint8_t, VLEN_BYTES>, NUM_VREGS> regs{};

    void reset() noexcept {
        for (auto& r : regs) {
            r.fill(0);
        }
    }

    inline uint8_t* get_reg_ptr(size_t reg_idx) noexcept {
        return regs[reg_idx].data();
    }

    inline const uint8_t* get_reg_ptr(size_t reg_idx) const noexcept {
        return regs[reg_idx].data();
    }

    template <typename T>
    inline T get_elem(size_t reg_idx, size_t elem_idx) const noexcept {
        if (reg_idx >= NUM_VREGS) return 0;
        size_t offset = elem_idx * sizeof(T);
        if (offset + sizeof(T) > VLEN_BYTES) return 0;
        T val;
        std::memcpy(&val, &regs[reg_idx][offset], sizeof(T));
        return val;
    }

    template <typename T>
    inline void set_elem(size_t reg_idx, size_t elem_idx, T val) noexcept {
        if (reg_idx >= NUM_VREGS) return;
        size_t offset = elem_idx * sizeof(T);
        if (offset + sizeof(T) > VLEN_BYTES) return;
        std::memcpy(&regs[reg_idx][offset], &val, sizeof(T));
    }

    inline bool is_mask_set(size_t mask_reg, size_t elem_idx) const noexcept {
        if (mask_reg >= NUM_VREGS) return false;
        size_t byte_idx = elem_idx / 8;
        size_t bit_idx = elem_idx % 8;
        if (byte_idx >= VLEN_BYTES) return false;
        return (regs[mask_reg][byte_idx] & (1 << bit_idx)) != 0;
    }

    void dump(std::ostream& os = std::cout) const {
        for (size_t i = 0; i < NUM_VREGS; ++i) {
            os << "v" << std::setw(2) << std::setfill('0') << i << ": [ ";
            for (int b = static_cast<int>(VLEN_BYTES) - 1; b >= 0; --b) {
                os << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(regs[i][b]) << " ";
            }
            os << std::dec << "]\n";
        }
    }
};

struct EmulatorState {
    VRegFile vregs;
    std::array<uint64_t, NUM_XREGS> xregs{};
    CSRState csr;

    void reset() noexcept {
        vregs.reset();
        xregs.fill(0);
        csr = CSRState{};
    }

    inline uint64_t get_xreg(size_t idx) const noexcept {
        if (idx == 0 || idx >= NUM_XREGS) return 0;
        return xregs[idx];
    }

    inline void set_xreg(size_t idx, uint64_t val) noexcept {
        if (idx > 0 && idx < NUM_XREGS) {
            xregs[idx] = val;
        }
    }
};

} // namespace visa_emulator