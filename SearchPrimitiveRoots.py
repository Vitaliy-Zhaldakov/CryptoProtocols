import PySimpleGUI as gui

def is_simple(number):
    """Проверка числа на простоту"""
    k = 0
    for i in range(2, number // 2 + 1):
        if (number % i == 0):
            k = k + 1
    if (k <= 0):
        return True
    else:
       return False

"""Поиск всех первообразных корней заданного простого модуля"""
if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Поиск первообразных корней заданного модуля", justification='center', size=(45, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Введите простой модуль:", font=('ComicSans', 12), size=(21, 1)),
         gui.InputText(font=('ComicSans', 12), size=(10, 1)),
         gui.Button('Вычислить', font=('ComicSans', 12))],
        [gui.T("   ")],
        [gui.Text(key='phi', font=('ComicSans', 12))],
        [gui.MLine(key='search', font=('ComicSans', 12), size=(60, 5))],
        [gui.Text(key='roots', font=('ComicSans', 12))]]

    window = gui.Window('Поиск первообразных корней', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            window['search'].update("")
            # Простой модуль
            module = int(values[0])
            # Проверка модуля на простоту
            if is_simple(module) == True:
                # Инициализация списка корней
                roots = []

                # Функция Эйлера заданного модуля
                phi = module - 1
                window['phi'].update(f"Функция Эйлера заданного модуля: {phi}")

                for root in range(2, module):
                    flag = 0
                    for degree in range(1, phi):
                        window['search'].print(f"{root}^{degree} = {root ** degree % module} (mod {module})", end=" ")
                        if root ** degree % module == 1:
                            flag = 1
                            break
                    if flag == 0:
                        roots.append(root)
                    window['search'].print("\n", end="")

                window['roots'].update(f"Все первообразные корни: {roots}")
            else:
                window['roots'].update("Ошибка: введен непростой модуль!")

    window.close()