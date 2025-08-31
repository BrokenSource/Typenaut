from typenaut import Custom, Document, Text, color, length
from typenaut.extra.card import Card


class Example(Document):
    def build(self):
        Custom(self, "#set page(fill: luma(6%))")

        with Card(self, height=length.auto()) as card:
            Text(card, color=color.gray(), value="#lorem(50)")


def main():
    document = Example()
    document.build()
    document.pdf(output="output.pdf")
    print(document.code())

if __name__ == "__main__":
    main()
