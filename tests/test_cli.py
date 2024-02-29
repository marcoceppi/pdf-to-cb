from unittest import mock
from pathlib import Path
from typer.testing import CliRunner

from pdf2cb.app import ArchiveFormat
from pdf2cb.cli import app

runner = CliRunner()


def test_app_bad_args():
    """Test bad CLI invocation"""
    result = runner.invoke(app)
    assert result.exit_code == 2


def test_app_cbr_format(pdf):
    """Test normal CLI invocation"""
    result = runner.invoke(app, ["--format", "cbr", f"{pdf}", f"{pdf}"])
    assert result.exit_code == 1


@mock.patch("pdf2cb.cli.Pdf2Cb")
def test_app_output_is_file(m_pdf2cb: mock.MagicMock, pdf: Path):
    """Test CLI handles file lists"""
    result = runner.invoke(app, [f"{pdf}", f"{pdf}"])
    m_pdf2cb.return_value.archive.assert_called_with(None)
    m_pdf2cb.assert_has_calls(
        [mock.call(pdf, ArchiveFormat.CBZ), mock.call(pdf, ArchiveFormat.CBZ)],
        any_order=True,
    )

    assert result.exit_code == 0


@mock.patch("pdf2cb.cli.Pdf2Cb")
def test_app_output_is_dir(m_pdf2cb: mock.MagicMock, pdf: Path):
    """Test CLI handles file lists"""
    output = pdf.parent / "test"
    result = runner.invoke(app, [f"{pdf}", f"{output}"])
    m_pdf2cb.return_value.archive.assert_called_with(output)
    m_pdf2cb.assert_has_calls(
        [mock.call(pdf, ArchiveFormat.CBZ)],
        any_order=True,
    )
    assert result.exit_code == 0
