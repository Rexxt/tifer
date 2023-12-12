# TIny File Editor Runtime - Python module for text editors

class FileEditor:
    def __init__(self,
        text: str = '',        # text to edit
        cursor: list = [0, 0], # initial position of the cursor (line, character)
        selection: list = None # text to select ((startline, startcharacter), (endline, endcharacter))
    ):
        self.text = []
        lines = text.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            self.text.insert(i, [])
            for j in range(len(line)):
                char = line[j]
                self.text[i].insert(j, char)
        
        self.cursor = cursor
        self.selection = selection

    def __str__(self):
        s = ''
        for i in range(len(self.text)):
            line = self.text[i]
            for j in range(len(line)):
                char = line[j]
                s += char
            s += '\n'
        
        return s

    def __repr__(self):
        return self.__str__()

    def write(self, text: str):
        """Write some text to the buffer at the cursor position, and automatically move the cursor. Will automatically split at `\\n`.
        Returns the current state of the buffer.

        Args:
            text (str): the text to write.
        """

        for char in text:
            line = self.cursor[0]
            cx = self.cursor[1]
            if char == '\n':
                # take everything after the index
                remainder = self.text[line][cx:]
                self.text[line] = self.text[line][:cx]
                self.text.insert(line + 1, remainder)
                self.cursor[1] = 0
                self.cursor[0] += 1
            else:
                self.text[line].insert(cx, char)
                self.cursor[1] += 1
        
        return self.text
    
    def backspace(self, n: int =1):
        """Backspace (ie delete the character before the cursor) n times (1 by default).

        Args:
            n (int, optional): Number of times to backspace. Defaults to 1.
        """

        for i in range(n):
            line = self.cursor[0]
            cx = self.cursor[1]
            if len(self.text[line][:cx]) == 0 and self.cursor[0] > 0:
                remainder = self.text[line][cx:]
                self.text.pop(line)
                self.move_xy(-1, 0)
                self.text[self.cursor[0]] += remainder
            elif len(self.text[line]) > 0:
                self.move_xy(-1, 0)
                self.text[line].pop(cx - 1)
    
    def move_end(self):
        """Moves to the end of the buffer."""

        self.cursor = [len(self.text) - 1, len(self.text[-1])]
    
    def move_xy(self, x: int, y: int):
        """Moves the cursor by x columns and y lines. Moves the cursor column to the end if needed.

        Args:
            x (int): number of columns to move
            y (int): number of lines to move
        """

        if y > 0:
            for i in range(y):
                self.cursor[0] += 1
                if self.cursor[1] > len(self.text[i + self.cursor[0]]):
                    self.cursor[1] = len(self.text[i + self.cursor[0]])
                if self.cursor[0] >= len(self.text):
                    self.cursor[0] -= 1
                    break
        elif y < 0:
            for i in range(-y):
                self.cursor[0] -= 1
                if self.cursor[1] > len(self.text[i + self.cursor[0]]):
                    self.cursor[1] = len(self.text[i + self.cursor[0]])
                if self.cursor[0] < 0:
                    self.cursor[0] += 1
                    break
        
        if x > 0:
            for i in range(x):
                self.cursor[1] += 1
                if self.cursor[1] > len(self.text[i + self.cursor[0]]):
                    self.cursor[1] = 0
                    self.cursor[0] += 1
                    if self.cursor[0] >= len(self.text):
                        self.cursor[0] -= 1
                        self.cursor[1] = len(self.text[i + self.cursor[0]])
                        break
        elif x < 0:
            for i in range(-x):
                self.cursor[1] -= 1
                if self.cursor[1] < 0:
                    self.cursor[0] -= 1
                    self.cursor[1] = len(self.text[i + self.cursor[0]])
                    if self.cursor[0] < 0:
                        self.cursor[0] += 1
                        self.cursor[1] = 0
                        break

if __name__ == '__main__':
    ed = FileEditor(open('readme.md', encoding='utf-8').read())
    print(ed)
    ed.move_end()
    ed.write('\nTesting\n`tifer`\'s\nediting\ncapacities')
    print(ed)