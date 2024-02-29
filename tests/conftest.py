import uuid
from pathlib import Path

import pytest


@pytest.fixture
def pdf(tmp_path) -> Path:
    """Create a copy of the test PDF file"""
    orig = Path("tests/data/somatosensory.pdf")
    f = tmp_path / f"{uuid.uuid4()}.pdf"
    f.write_bytes(orig.read_bytes())
    return f
