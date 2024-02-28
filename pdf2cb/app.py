"""pdf2cb module"""

import enum
import zipfile
from pathlib import Path
from io import BytesIO

import pdf2image


class ArchiveFormat(enum.StrEnum):
    CBR = "cbr"
    CBZ = "cbz"


class Pdf2Cb:
    def __init__(self, pdf: Path, format: ArchiveFormat = ArchiveFormat.CBZ):
        """Convert a PDF file to a ComicBook archive"""
        self.source = Path(pdf)
        self.pages: list = []
        if not self.source.is_file():
            raise ValueError(f"pdf_file {self.source} is not a file")

        if format not in ArchiveFormat:
            raise ValueError(f"{format} is not one of {ArchiveFormat}")

        self.format = format

    def extract(self, dest: Path | None = None, **kwargs):
        """Extract a PDF to images"""
        if dest and not dest.is_dir():
            raise ValueError(f"dest {dest} is not a directory")

        default_args = {"fmt": "jpg", "output_folder": dest}
        self.images = pdf2image.convert_from_path(
            pdf_path=self.source,
            **(default_args | kwargs),
        )

    def archive(self, output_dir: Path | None = None) -> Path:
        """Create an archive of an extracted PDF"""
        archive_file = self.source.with_suffix(f".{self.format}")
        if output_dir:
            archive_file = Path(output_dir) / archive_file.name

        fn = getattr(self, f"_create_{self.format}")
        fn(archive_file)
        return archive_file

    def convert(self) -> Path:
        """Convert the PDF to a CB archive"""
        self.extract()
        return self.archive()

    def _create_cbr(self):
        """Create a CBR archive from a directory"""
        raise NotImplementedError

    def _create_cbz(self, output: Path):
        """Create a CBZ archive from a directory"""
        archive = zipfile.ZipFile(output, mode="w")
        for id, image in enumerate(self.images, 1):
            image_fp = BytesIO()
            image.save(image_fp, format="JPEG")
            archive.writestr(
                f"{self.source.stem}_{id}.jpg",
                image_fp.getvalue(),
                compress_type=zipfile.ZIP_DEFLATED,
            )
