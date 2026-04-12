from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PayrollConfig:
    config_file: Path = field(
        default_factory=lambda: Path.home() / ".config/tims_tools/tims_payroll.toml"
    )
    db_file: Path = field(
        default_factory=lambda: Path.home() / ".config/tims_tools/tmp_payroll.db"
    )
    output_dir: Path = field(default_factory=lambda: Path.home() / "Documents")
