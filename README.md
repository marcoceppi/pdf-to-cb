# PDF to Comic Book format

Python CLI to convert PDFs to either CBZ or CBR.

## Install

### Pre-requisites

poppler needs to be installed and available in path before using pdf-to-cb.

**Debian / Ubuntu**
```sh
sudo apt install poppler-utils
```

**RHEL / CentOS / Fedora**
```sh
sudo dnf install poppler poppler-utils
```

**Arch**
```sh
sudo pacman -S poppler
```

**Mac / OSX**
```sh
brew install poppler
```

**Windows**
This isn't tested or fully supported for this package. However, downloading and installing [poppler-windows](https://github.com/oschwartz10612/poppler-windows) into the system path may work.

### pipx

pipx is available for Linux, OSX, and Windows. Follow the [install instructions first for pipx](https://pipx.pypa.io/stable/installation/) then the following:

```
pipx install pdf-to-cb
```

## Usage

```sh
pdf-to-cb --format cbz *.pdf ~/complete/
```


Original inspiration: https://github.com/mathewskevin/pdf-to-cbz
