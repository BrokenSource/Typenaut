<div align="center">
  <img src="https://raw.githubusercontent.com/BrokenSource/Typenaut/main/typenaut/resources/images/logo.png" width="210">
  <h1 style="margin-top: 0">Typenaut</h1>
  <p>Typst documents from python classes</p>
</div>

> [!WARNING]
> This project is no longer maintained:
>
> - Typst's native [`sys.inputs`](https://typst.app/docs/reference/foundations/sys)  solved my needs, feeding pydantic models for dynamic content.
> - Not worth it to mirror what typst already does internally - _it's turtles all the way down!_
> - Pure library usage will likely improve in the future with community or official effort.
>
> I'm archiving the repository as it got some clever tricks and a rough idea in how a meta programming library and utils would look like. Feel free to base off a continuation or rewrite under the MIT license (requires including original copyright notice and attribution).
>
> **Since I own the PyPI package**, get in touch for a name transfer for any purpose shall you be worthy!
>
> <sup><b>Note:</b> Please change the logo on a fork, as I _will_ use it elsewhere planned.</sup>

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

## 🚀 Usage

Your best chance is on exploring the [**examples**](../examples) directory likely for a good while.

- Upstream [typst](https://typst.app/docs/) documentation is always a valuable resource!

<sup><b>Note:</b> I really do not have the time to write structured documentation, but the code contains quality type hints and docstrings.</sup>
