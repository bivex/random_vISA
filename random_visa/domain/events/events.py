"""Domain Events for V-ISA Lifecycle."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class DomainEvent:
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class InstructionSynthesizedEvent(DomainEvent):
    mnemonic: str = ""
    funct6: int = 0
    funct3: int = 0
    format_name: str = ""


@dataclass(frozen=True)
class IsaSpecCompletedEvent(DomainEvent):
    spec_name: str = ""
    instruction_count: int = 0
    vlen: int = 128


@dataclass(frozen=True)
class CppEmulatorEmittedEvent(DomainEvent):
    spec_name: str = ""
    output_dir: str = ""
    files_emitted: int = 0
