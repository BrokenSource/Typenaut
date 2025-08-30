from typenaut import Document, Text
from typenaut.packages.shadowed import Shadowed


class Shadow(Document):
    def build(self):
        with Shadowed(self) as shadowed:
            Text(shadowed, value="#lorem(50)")

def main():
    document = Shadow()
    document.build()
    document.pdf(output="output.pdf")
    print(document.code())

if __name__ == "__main__":
    main()
