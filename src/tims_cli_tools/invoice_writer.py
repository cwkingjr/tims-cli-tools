from pathlib import Path
from typing import Protocol, runtime_checkable

import pandas as pd


@runtime_checkable
class InvoiceWriter(Protocol):
    def write(self, df: pd.DataFrame, output_path: Path) -> None: ...


class XlsxInvoiceWriter:
    def write(self, df: pd.DataFrame, output_path: Path) -> None:
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            df.to_excel(
                writer,
                sheet_name="Sheet1",
                startrow=1,
                header=False,
                index=False,
            )

            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            self._write_headers(df, workbook, worksheet)
            self._set_column_widths(df, workbook, worksheet)

    def _write_headers(self, df: pd.DataFrame, workbook, worksheet) -> None:
        dark_purple_header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "font_color": "white",
                "fg_color": "#700AAF",
                "border": 1,
            }
        )

        blue_header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#B4CAF4",
                "border": 1,
            }
        )

        light_purple_header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D4C2ED",
                "border": 1,
            }
        )

        orange_header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#F3906B",
                "border": 1,
            }
        )

        for col_num, value in enumerate(df.columns.values):
            if col_num in [1, 2, 3, 4]:
                worksheet.write(0, col_num, value, dark_purple_header_format)
            elif col_num in [13, 15, 16]:
                worksheet.write(0, col_num, value, blue_header_format)
            elif col_num in [0, 17, 18]:
                worksheet.write(0, col_num, value, orange_header_format)
            else:
                worksheet.write(0, col_num, value, light_purple_header_format)

    def _set_column_widths(self, df: pd.DataFrame, workbook, worksheet) -> None:
        currency_format = workbook.add_format(
            {"num_format": "#,##0.00", "valign": "vcenter"}
        )
        align_format = workbook.add_format({"align": "center", "valign": "vcenter"})
        v_align_format = workbook.add_format({"valign": "vcenter"})
        xcans_format = workbook.add_format({"align": "left", "valign": "vcenter"})

        for i, col in enumerate(df.columns):
            if i == 0:
                worksheet.set_column(i, i, len(col) + 1, align_format)
            elif i == 1:
                worksheet.set_column(i, i, len(col) + 7, align_format)
            elif i == 2:
                worksheet.set_column(i, i, len(col) + 1, v_align_format)
            elif i == 3:
                worksheet.set_column(i, i, len(col) + 40, v_align_format)
            elif i == 7:
                worksheet.set_column(i, i, len(col) + 5, currency_format)
            elif i in [5, 6, *range(8, 15), 16]:
                worksheet.set_column(i, i, len(col) + 1, currency_format)
            elif i == 15:
                worksheet.set_column(i, i, len(col) + 1, align_format)
            elif i == 18:
                worksheet.set_column(i, i, len(col) + 1, xcans_format)
            else:
                worksheet.set_column(i, i, len(col) + 1, v_align_format)
