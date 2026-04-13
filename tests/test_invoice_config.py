from pathlib import Path


from tims_cli_tools.invoice_config import InvoiceConfig


class TestInvoiceConfig:
    def test_default_output_dir_is_home_documents(self):
        config = InvoiceConfig()
        assert config.output_dir == Path.home() / "Documents"

    def test_custom_output_dir(self):
        custom_path = Path("/custom/path")
        config = InvoiceConfig(output_dir=custom_path)
        assert config.output_dir == custom_path
