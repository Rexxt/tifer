from blessed import Terminal
from tifer import FileEditor
from sys import argv

term = Terminal()

if len(argv) < 2:
    print('Missing required file argument')
    exit(1)

file_path = argv[1]
editor = FileEditor(open(file_path, encoding='utf-8').read())

def utf8len(s):
    return len(s.encode('utf-8'))

with term.fullscreen(), term.hidden_cursor():
    oy = 0
    while True:
        render = ''
        for i in range(oy, term.height - 1 + oy):
            if i >= len(editor.text):
                render += term.bold_grey(f'{len(editor.text)} line(s)')
                break
            for j in range(len(editor.text[i])):
                if j > term.width:
                    break
                if editor.cursor == [i, j]:
                    render += term.on_white
                render += editor.text[i][j] + term.normal

            if editor.cursor[0] == i and editor.cursor[1] >= len(editor.text[i]):
                render += term.on_white(' ')
            render += '\n'
        render += term.move_xy(0, term.height - 1) + term.on_blue(file_path) + ' ' + term.bold_blue(f'L{editor.cursor[0] + 1}, C{editor.cursor[1] + 1}') + ' ' + term.green(str(utf8len(str(editor))) + ' B')

        print(term.home+term.clear+render, end='')

        with term.cbreak():
            key = term.inkey()
            if key.name == 'KEY_ESCAPE':
                exit()
            elif key.name == u'KEY_LEFT':
                editor.move_xy(-1, 0)
            elif key.name == u'KEY_RIGHT':
                editor.move_xy(1, 0)
            elif key.name == u'KEY_DOWN':
                editor.move_xy(0, 1)
                if editor.cursor[0] - oy >= term.height - 1:
                    oy += 1
            elif key.name == u'KEY_UP':
                editor.move_xy(0, -1)
                if editor.cursor[0] - oy < 0:
                    oy -= 1
            elif key.name == u'KEY_ENTER':
                editor.write('\n')
                if editor.cursor[0] - oy >= term.height - 1:
                    oy += 1
            elif key.name == u'KEY_BACKSPACE':
                if editor.cursor[0] - oy < 0:
                    oy -= 1
                editor.backspace()
            else:
                editor.write(str(key))