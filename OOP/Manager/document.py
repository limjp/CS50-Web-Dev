class Document:
    def __init__(self) -> None:
        self.characters = []
        self.cursor = Cursor(self)
        self.filename = ""

    def insert(self, character):
        self.characters.insert(self.cursor, character)
        self.cursor.forward()
    
    def delete(self):
        del self.characters[self.cursor.position]
    
    def save(self):
        with open(self.filename, "w") as f:
            f.write("".join(self.characters))
    
    def forward(self):
        self.cursor += 1
    
    def back(self):
        self.cursor -= 1

class Cursor:
    def __init__(self, document) -> None:
        self.document = document
        self.position = 0

    def forward(self):
        self.position += 1
    
    def back(self):
        self.position -= 1
    
    def home(self):
        while self.document.characters[self.position - 1].character != "\n":
            self.position -= 1
            if self.position == 0:
                # Got to beginning of file before newline
                break

    def end(self):
        while (
            self.position < len(self.document.characters)
            and self.document.characters[self.position] != "\n"
        ):
            self.position += 1