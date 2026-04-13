from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class InvoiceConfig:
    output_dir: Path = field(default_factory=lambda: Path.home() / "Documents")
