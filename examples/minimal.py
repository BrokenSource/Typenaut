from typenaut import Document, Rectangle, Text


class Minimal(Document):
    def build(self):
        with Rectangle(self) as rect:
            Text(rect, value="Hi, I'm inside the rectangle")

def main():
    document = Minimal()
    document.build()

    print("Code:", '\n'.join(document.typst()))
    document.pdf(output="output.pdf")

if __name__ == "__main__":
    main()
