# pylint: disable=C0301
"""CLI module"""

from pathlib import Path
from importlib.metadata import version

import typer
from rich.console import Console
from typing_extensions import Annotated

from pdf2cb.app import Pdf2Cb, ArchiveFormat


app = typer.Typer(rich_markup_mode="rich")
console = Console()


@app.command(
    epilog=f"Version {version('pdf-to-cb')}. Made with :star2: [link=https://github.com/marcoceppi/pdf-to-cb]github.com/marcoceppi/pdf-to-cb[/link]"
)
def convert(
    inputs: Annotated[list[Path], typer.Argument(help="PDFs to convert")],
    output: Annotated[
        Path, typer.Argument(help="where to place converted PDFs")
    ] = None,
    fmt: Annotated[
        ArchiveFormat, typer.Option("--format", help="format to convert the PDF to")
    ] = ArchiveFormat.CBZ,
):
    """Convert PDF to Comic Book formats"""
    if fmt is ArchiveFormat.CBR:
        raise ValueError("CBR format not supported yet")

    if output.is_file():
        inputs.append(output)
        output = None
        console.print(
            "[yellow bold]:warning: No output directory specified, converted files will be placed next to the PDF"
        )

    if output:
        output.mkdir(parents=True, exist_ok=True)

    status = console.status("")
    for f in inputs:
        comic = Pdf2Cb(f, fmt)
        status.update(f"[bold green](extracting)[/] [purple]{f.name}")
        status.start()
        comic.extract()
        status.update(f"[bold green](compressing)[/] [purple]{f.name}")
        archive_path = comic.archive(output)
        status.stop()
        console.print(f":white_check_mark: [purple]{archive_path}")
