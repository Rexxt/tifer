from blessed import Terminal
from tifer import FileEditor
from sys import argv

term = Terminal()

if len(argv) < 2:
    print('Missing required file argument')
    exit(1)

file_path = argv[1]
editor = FileEditor(open(file_path, encoding='utf-8').read())

with term.fullscreen(), term.hidden_cursor():
    while True:
        render = ''
        for i in range(term.height - 1):
            if i >= len(editor.text):
                break
            for j in range(len(editor.text[i])):
                if j > term.width:
                    break
                if editor.cursor == [i, j]:
                    render += term.on_white
                render += editor.text[i][j] + term.normal

            if editor.cursor[1] == j and editor.cursor[0] >= len(editor.text[i]):
                render += term.on_white(' ')
            render += '\n'
        render += term.move_xy(0, term.height - 1) + term.on_blue(file_path) + ' ' + term.bold_blue(f'L{editor.cursor[0] + 1}, C{editor.cursor[1] + 1}')

        print(term.home+term.clear+render, end='')

        with term.cbreak():
            key = term.inkey(timeout=0)
            if str(key) == 'q':
                exit()
            elif key.name == u'KEY_LEFT':
                editor.move_xy(-1, 0)
            elif key.name == u'KEY_RIGHT':
                editor.move_xy(1, 0)
            elif key.name == u'KEY_DOWN':
                editor.move_xy(0, 1)
            elif key.name == u'KEY_UP':
                editor.move_xy(0, -1)
            elif key.name == u'KEY_ENTER':
                editor.write('\n')
            else:
                editor.write(str(key))