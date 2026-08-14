"""Outbound Adapter: Sail Specification File Writer."""

import os
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.ports.outbound.ports import SailSpecWriterPort


class SailFileAdapter(SailSpecWriterPort):
    """Adapter for writing Sail language specification files."""

    def write_spec(self, spec: VectorIsaSpec, target_file_path: str) -> str:
        parent = os.path.dirname(os.path.abspath(target_file_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
            
        content = spec.to_sail_specification()
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return target_file_path
