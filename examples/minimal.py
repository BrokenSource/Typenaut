from typenaut import Document, Rectangle, Text


class Minimal(Document):
    def build(self):
        with Rectangle(self) as rect:
            Text(rect, value="Hi, I'm inside the rectangle")

def main():
    document = Minimal()
    document.build()
    document.pdf(output="output.pdf")
    print(document.code())

if __name__ == "__main__":
    main()
