<div align="center">

# ♻️ Makemore

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![cookiecutter chef](https://img.shields.io/badge/cookiecutter-chef-D4AA00?logo=cookiecutter&logoColor=fff)](https://github.com/baggiponte/chef)
<br>
[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![imports isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy.readthedocs.io/en/stable/)
[![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
<br>
[![documentation mkdocs](https://img.shields.io/badge/documentation-mkdocs-0094F5)](https://www.mkdocs.org/)
[![docstyle google](https://img.shields.io/badge/%20style-google-459db9.svg)](https://numpydoc.readthedocs.io/en/latest/format.html)

</div>

## ⚡ Features

`makemore` generates more of the same stuff.

## 📦 How to install

```bash
pdm add makemore
```

## 🏫 Tutorials

* [Fundamentals of Python](./notebooks/00-intro-to-python.ipynb): [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/baggiponte/makemore/blob/main/notebooks/00-intro-to-python.ipynb)
* [A data processing example](./notebooks/01-data-processing.ipynb): [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/baggiponte/makemore/blob/main/notebooks/01-data-processing.ipynb)
* [Multilayer Perceptron](./notebooks/02-mlp.ipynb): [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/baggiponte/makemore/blob/main/notebooks/02-mlp.ipynb)

## 🤗 Contributing

### Development

1. Clone the repository:

```bash
# using github cli
gh repo clone baggiponte/makemore

# using git (SSH recommended)
git clone git@github.com:baggiponte/makemore
```

> **Note**
>
> 🎬 How to configure SSH
>
> Cloning over SSH is safer. Follow [this guide](https://www.youtube.com/watch?v=5o9ltH6YmtM).
> Alternatively, you can follow the steps in [this](https://github.com/git-merge-workshops/simplify-signing-with-ssh/blob/main/exercises/01-setup-workstation.md) workshop of GitHub's.

2. Install `pdm`:

```bash
pipx install pdm
```

> **Warning**
>
> 🔎 Why `pipx`?
> `pip install --user` is not recommended, as it does not ensure dependency isolation. For this purpose, the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/) advises to use [`pipx`](https://pypa.github.io/pipx/). `pipx` installs and runs python CLIs in isolated environments. To install it, follow the instructions [here](https://pypa.github.io/pipx/#install-pipx).

3. Install production and development dependencies.

The recommended approach is to use [`just`](https://github.com/casey/just). Install `just` with your favourite package manager, then run the following:

```
just install
```
