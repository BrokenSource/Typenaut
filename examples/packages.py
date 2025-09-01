from typenaut import Document, Text, length
from typenaut.packages import curvly, shadowed


class Example(Document):
    def build(self):
        with shadowed.Shadowed(self) as shadowbox:
            Text(shadowbox, value="#lorem(50)")
            curvly.ArcText(shadowbox,
                value="Surfing in the Flow",
                width=length.cm(10)
            )
        curvly.CircleText(self)

def main():
    document = Example()
    document.build()
    document.pdf(output="output.pdf")
    print(document.code())

if __name__ == "__main__":
    main()
