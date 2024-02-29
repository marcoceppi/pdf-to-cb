import pytest
import zipfile
from unittest import mock
from pathlib import Path
from pdf2cb.app import Pdf2Cb, ArchiveFormat


def test_pdf2cb_init(pdf):
    """Pdf2Cb validates inputs"""
    with pytest.raises(ValueError):
        Pdf2Cb("/tmp/does-not-exist/dddd")

    with pytest.raises(ValueError):
        Pdf2Cb(pdf, "rar")

    t1 = Pdf2Cb(pdf, "cbz")
    assert t1.source == pdf
    assert t1.pages == []
    assert t1.format == "cbz"

    t2 = Pdf2Cb(pdf, ArchiveFormat.CBZ)
    assert t2.format == "cbz"


def test_pdf2cb_extract(pdf):
    """Pdf2Cb can extract a PDF"""
    t = Pdf2Cb(pdf)
    assert len(t.pages) == 0
    t.extract()
    assert len(t.pages) == 4


def test_pdf2cb_extract_dest(pdf, tmp_path):
    """Pdf2Cb can extract a PDF to a path"""
    dest_dir = tmp_path / "extract"
    dest_dir.mkdir(exist_ok=True, parents=True)
    t = Pdf2Cb(pdf)
    assert len(t.pages) == 0
    t.extract(dest_dir)
    assert len(t.pages) == 4
    assert len(list(dest_dir.iterdir())) == len(t.pages)


def test_pdf2cb_extract_dest_is_file(pdf):
    """Pdf2Cb can extract a PDF to a path"""
    t = Pdf2Cb(pdf)
    with pytest.raises(ValueError):
        t.extract(pdf)


def test_pdf2cb_archive(pdf):
    """Pdf2Cb picks the correct archiver"""
    t = Pdf2Cb(pdf, "cbz")
    expected = Path("/test") / f"{pdf.stem}.cbz"
    with mock.patch.object(t, "_create_cbz") as fn:
        ret = t.archive("/test")
        fn.assert_called_with(expected)
        assert ret == expected


def test_pdf2cb_convert(pdf):
    """Pdf2Cb converts correctly"""
    t = Pdf2Cb(pdf)
    with mock.patch.multiple(t, extract=mock.DEFAULT, archive=mock.DEFAULT) as m:
        t.convert()
        m["extract"].assert_called_once()
        m["archive"].assert_called_once()


def test_pdf2cb_create_cbr(pdf):
    """Pdf2Cb cbr creation fails"""

    t = Pdf2Cb(pdf)
    with pytest.raises(NotImplementedError):
        t._create_cbr()


def test_pdf2cb_create_cbz(pdf):
    """Pdf2Cb cbz creation works"""

    t = Pdf2Cb(pdf)
    t.extract()
    archive = pdf.with_suffix(".zip")
    t._create_cbz(archive)
    assert archive.is_file()
    z = zipfile.ZipFile(archive)
    assert len(z.filelist) == len(t.pages)
    assert len(z.filelist) > 1
