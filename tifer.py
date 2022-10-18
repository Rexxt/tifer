# TIny File Editor Runtime - Python module for text editors

class FileEditor:
    def __init__(self,
        text='',       # text to edit
        cursor=(0, 0), # initial position of the cursor (line, character)
        selection=None # text to select ((startline, startcharacter), (endline, endcharacter))
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

if __name__ == '__main__':
    ed = FileEditor(open('readme.md', encoding='utf-8').read())
    print(ed.text)
    print(ed.cursor)
    print(ed.selection)
    print(ed)