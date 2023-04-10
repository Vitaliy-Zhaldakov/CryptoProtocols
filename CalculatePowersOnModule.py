import PySimpleGUI as gui

class PowerIntegers:
    """Класс вычисления целых степеней по заданному модулю"""
    def __init__(self, mod):
        self.mod = mod

    def mul_mod(self, a, b):
        """Умножение по модулю"""
        return (a * b) % self.mod

    def add_mod(self, a, b):
        """Сложение по модулю"""
        return (a + b) % self.mod

    def power_positive_mod(self, base, power):
        """Малая теорема Ферма для вычисления положительной степени"""
        result = 1
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % self.mod
            base = (base * base) % self.mod
            power //= 2
        return result

    def power_negative_mod(self, base, power):
        """Теорема Эйлера для вычисления отрицательной степени"""
        mod = self.mod
        result = 1
        power = self.euler_function(mod) - power
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % mod
            base = base **2 % mod
            power //= 2
        return result

    def euler_function(self, n):
        """Функция Эйлера"""
        phi = n
        i = 2
        while i * i <= n:
            if n % i == 0:
                phi -= phi // i
                while n % i == 0:
                    n //= i
            i += 1
        if n > 1:
            phi -= phi // n
        return phi

if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Вычисление степеней по заданному модулю", justification='center', size=(45, 1),
                  font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Введите основание:", font=('ComicSans', 12), size=(17, 1)),
         gui.InputText(font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Введите показатель:", font=('ComicSans', 12), size=(17, 1)),
         gui.InputText(font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Введите модуль:", font=('ComicSans', 12), size=(17, 1)),
         gui.InputText(font=('ComicSans', 12), size=(10, 1))],
         [gui.Text(key='result', font=('ComicSans', 12))],
         [gui.T("   ")],
         [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Вычисление степеней по заданному модулю', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            # Основание
            number = int(values[0])
            # Показатель
            power = int(values[1])
            # Модуль
            module = int(values[2])
            powerIntegers = PowerIntegers(module)
            if power > 0:
                result = powerIntegers.power_positive_mod(number, power)
            else:
                result = powerIntegers.power_negative_mod(number, power)
            window['result'].update(f"Ответ: {result}")

    window.close()