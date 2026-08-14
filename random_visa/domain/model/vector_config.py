"""Vector Configuration Value Object."""

from dataclasses import dataclass
from random_visa.domain.model.types import SEW, LMUL, TailPolicy, MaskPolicy


@dataclass(frozen=True)
class VectorConfig:
    """Immutable configuration representing the vector engine parameters."""
    vlen: int = 128          # Vector register length in bits (e.g. 128, 256, 512)
    elen: int = 64           # Maximum element width in bits
    default_sew: SEW = SEW.E32
    default_lmul: LMUL = LMUL.M1
    tail_policy: TailPolicy = TailPolicy.AGNOSTIC
    mask_policy: MaskPolicy = MaskPolicy.AGNOSTIC
    num_vregs: int = 32

    def __post_init__(self) -> None:
        if self.vlen <= 0 or (self.vlen & (self.vlen - 1)) != 0:
            raise ValueError(f"VLEN must be a power of 2, got {self.vlen}")
        if self.elen > self.vlen:
            raise ValueError(f"ELEN ({self.elen}) cannot exceed VLEN ({self.vlen})")
        if self.num_vregs < 8 or (self.num_vregs & (self.num_vregs - 1)) != 0:
            raise ValueError(f"num_vregs must be a power of 2 >= 8, got {self.num_vregs}")

    @property
    def vlen_bytes(self) -> int:
        return self.vlen // 8

    def calculate_vlmax(self, sew: SEW, lmul: LMUL) -> int:
        """Calculate VLMAX = (VLEN / SEW) * LMUL."""
        return int((self.vlen / sew.value) * lmul.multiplier_val)
