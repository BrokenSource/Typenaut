from typenaut import Document, Text, length
from typenaut.packages.curvly import ArcText, CircleText
from typenaut.packages.shadowed import Shadowed


class Example(Document):
    def build(self):
        with Shadowed(self) as shadowed:
            Text(shadowed, value="#lorem(50)")
            ArcText(shadowed,
                value="Surfing in the Flow",
                width=length.cm(10)
            )
        CircleText(self)

def main():
    document = Example()
    document.build()
    document.pdf(output="output.pdf")
    print(document.code())

if __name__ == "__main__":
    main()
