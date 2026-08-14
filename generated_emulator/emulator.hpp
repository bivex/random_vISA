#pragma once
#include "isa_state.hpp"
#include "decoder.hpp"
#include "instructions.hpp"
#include <vector>
#include <string>

namespace visa_emulator {

class VectorEmulator {
public:
    EmulatorState state;

    VectorEmulator() {
        state.reset();
    }

    void reset() {
        state.reset();
    }

    bool step(uint32_t instruction_word) {
        DecodedInstruction dec = Decoder::decode(instruction_word);
        if (dec.id == InstId::UNKNOWN) {
            return false;
        }
        return InstructionExecutor::execute(state, dec);
    }

    size_t run_program(const std::vector<uint32_t>& program) {
        size_t executed = 0;
        for (uint32_t word : program) {
            if (!step(word)) {
                break;
            }
            executed++;
            state.csr.pc += 4;
        }
        return executed;
    }
};

} // namespace visa_emulator