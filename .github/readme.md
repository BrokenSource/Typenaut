<div align="center">
  <img src="https://raw.githubusercontent.com/BrokenSource/Typenaut/main/typenaut/resources/images/logo.png" width="210">
  <h1 style="margin-top: 0">Typenaut</h1>
  <p>Typst documents from python classes</p>
  <a href="https://pypi.org/project/typenaut/"><img src="https://img.shields.io/pypi/v/typenaut?label=PyPI&color=blue"></a>
  <a href="https://pypi.org/project/typenaut/"><img src="https://img.shields.io/pypi/dw/typenaut?label=Installs&color=blue"></a>
  <a href="https://github.com/BrokenSource/Typenaut/"><img src="https://img.shields.io/github/v/tag/BrokenSource/Typenaut?label=GitHub&color=orange"></a>
  <a href="https://github.com/BrokenSource/Typenaut/stargazers/"><img src="https://img.shields.io/github/stars/BrokenSource/Typenaut?label=Stars&style=flat&color=orange"></a>
  <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
</div>

> [!IMPORTANT]
> This project is under active development. While basic functionality works, most features are missing, no documentation exists, and anything may (and will) change anytime! Feedback is welcome 🙂

## 🔥 Description

An experiment on [typst](https://typst.app/) metaprogramming within python for heavy templating.

```python
from typenaut import Document, Rectangle, Text

class Minimal(Document):
    def build(self):
        with Rectangle(self) as rect:
            Text(rect, value="Hi, I'm inside the rectangle")

# Automated usage!
document = Minimal()
document.build()
document.pdf(output="output.pdf")
```

## 📦 Installation

> Use `pip install git+https://github.com/BrokenSource/Typenaut` until further PyPI releases are made.

## 🚀 Usage

Your best chance is on exploring the [**examples**](../examples) directory likely for a good while.

- Upstream [typst](https://typst.app/docs/) documentation is always a valuable resource!

<sup><b>Note:</b> I really do not have the time to write structured documentation, but the code contains quality type hints and docstrings.</sup>

## ⚖️ License

Still deciding, currently source available.

Likely same as Typst, still studying libraries compliances.
