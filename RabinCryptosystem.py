import random
from functools import reduce
import PySimpleGUI as gui

def CRT(n, r):
    total = 0
    prod = reduce(lambda r, b: r * b, n)

    for n_i, r_i in zip(n, r):
        p = prod // n_i
        total += r_i * modInv(p, n_i) * p
    return total % prod


# Qin Jiushao's algorithm (大衍求一术 Dayan qiuyi method)
def modInv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1

# Returns the greatest common divisor of two integers a and b
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Returns (x, y, gcd) such that ax + by = gcd
def extended_gcd(a, b):
    if a == 0:
        return (0, 1, b)
    x, y, gcd = extended_gcd(b % a, a)
    return (y - (b // a) * x, x, gcd)

# Returns the modular inverse of a modulo m
def mod_inv(a, m):
    x, y, gcd = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("No modular inverse exists!")
    return x % m

# Returns a random prime number between min_val and max_val
def generate_prime(min_val, max_val):
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p) and (p % 4 == 3):
            return p

# Returns True if n is a prime number, False otherwise
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Generates the public and private keys for the Rabin cryptosystem
def generate_keys():
    p = generate_prime(0, 30)
    q = generate_prime(0, 30)
    n = p * q
    return (n, p, q)

# Encrypts a message using the Rabin cryptosystem
def encrypt(msg, n, language):
    char_list = list(msg.upper().replace(" ", ""))
    ciphertext = []
    for char in char_list:
        num = language.index(char)
        ciphertext.append(pow(num, 2, n))
    return ciphertext

# Decrypts a message using the Rabin cryptosystem
def decrypt(ciphertext, p, q, language):
    n = p * q
    decryption_list = []
    for num in ciphertext:
        a1 = pow(num, (p + 1) // 4, p)
        a2 = p - a1
        b1 = pow(num, (q + 1) // 4, q)
        b2 = q - b1

        try:
            m1 = CRT([p, q], [a1, b1])
            m2 = CRT([p, q], [a1, b2])
            m3 = CRT([p, q], [a2, b1])
            m4 = CRT([p, q], [a2, b2])
            possible_messages = [m1, m2, m3, m4]
            for msg in possible_messages:
                if msg <= len(language):
                    decryption_list.append(msg)
                    break
        except:
            return 0

    decryption_msg = ""
    for index in decryption_list:
        decryption_msg += language[index]
    return decryption_msg


if __name__ == "__main__":
    english = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    russian = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф",
               "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Криптосистема Рабина", justification='center', size=(45, 1),
                  font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Введите сообщение:", font=('ComicSans', 12), size=(17, 1)),
         gui.InputText(font=('ComicSans', 12), size=(20, 1)),
         gui.Text("Открытый ключ:", key="key", font=('ComicSans', 12))],
        [gui.Text("Шифртекст:", key="cipher", font=('ComicSans', 12))],
        [gui.Text("Расшифрованное сообщение:", key="result", font=('ComicSans', 12))],
         [gui.T("   ")],
         [gui.Button('Запуск', font=('ComicSans', 12))]]

    window = gui.Window('Криптосистема Рабина', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Запуск':
            # Сообщение
            msg = values[0]
            if english.__contains__(msg[1].upper()):
                language = english
            else:
                language = russian
            keys = generate_keys()
            with open("keys.txt", "w") as f:
                f.write(f"{keys[1]}, {keys[2]}")
            window['key'].update(f"Открытый ключ: {keys[0]}")
            cipher = encrypt(msg, keys[0], language)
            window['cipher'].update(f"Шифртекст: {cipher}")
            decryption = decrypt(cipher, keys[1],keys[2], language)
            if decryption == 0:
                window['result'].update(f"Расшифрованное сообщение: {msg.upper()}")
            else:
                window['result'].update(f"Расшифрованное сообщение: {decryption}")

    window.close()
