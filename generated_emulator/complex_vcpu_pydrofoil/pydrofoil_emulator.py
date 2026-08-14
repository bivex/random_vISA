# Pydrofoil Vector ISA Emulator Core Engine
import struct
from typing import List, Optional
try:
    from .pydrofoil_state import PydrofoilState
    from .pydrofoil_decoder import decode, DecodedInstruction
    from .pydrofoil_instructions import execute
except (ImportError, ValueError):
    from pydrofoil_state import PydrofoilState
    from pydrofoil_decoder import decode, DecodedInstruction
    from pydrofoil_instructions import execute

class PydrofoilVectorEmulator:
    def __init__(self):
        self.state = PydrofoilState()

    def reset(self):
        self.state.reset()

    def step(self, instruction_word: int) -> bool:
        dec = decode(instruction_word)
        if not dec:
            return False
        ok = execute(self.state, dec)
        if ok:
            self.state.csr.pc += 4
        return ok

    def run_bytecode(self, bytecode_bytes: bytes) -> int:
        count = len(bytecode_bytes) // 4
        executed = 0
        for i in range(count):
            word = struct.unpack_from("<I", bytecode_bytes, i * 4)[0]
            if not self.step(word):
                break
            executed += 1
        return executed