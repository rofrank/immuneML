from dataclasses import dataclass, field
from typing import List

from source.reports.ReportOutput import ReportOutput


@dataclass
class ReportResult:
    name: str = None
    output_figures: List[ReportOutput] = field(default_factory=lambda: [])
    output_tables: List[ReportOutput] = field(default_factory=lambda: [])
    output_text: List[ReportOutput] = field(default_factory=lambda: [])
    other_output: List[ReportOutput] = field(default_factory=lambda: [])
