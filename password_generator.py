import secrets
import string

try:
    import pyperclip
    HAVE_PYPERCLIP = True
except Exception:
    HAVE_PYPERCLIP = False

def ask_bool(prompt: str, default: bool = True) -> bool:
    suf = " [Y/n]: " if default else " [y/N]: "
    while True:
        val = input(prompt + suf).strip().lower()
        if val == "":
            return default
        if val in ("y", "yes"):
            return True
        if val in ("n", "no"):
            return False
        print("Responde 'y' o 'n'.")

def ask_int(prompt: str, default: int = None, minimum: int = None) -> int:
    while True:
        raw = input(f"{prompt}" + (f" (por defecto {default})" if default is not None else "") + ": ").strip()
        if raw == "" and default is not None:
            return default
        try:
            v = int(raw)
            if minimum is not None and v < minimum:
                print(f"El valor debe ser >= {minimum}.")
                continue
            return v
        except ValueError:
            print("Introduce un número entero válido.")

def generate_password(length: int, use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> str:
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%&*()-_=+[]{};:,.<>?/"

    if not pool:
        raise ValueError("Debes seleccionar al menos un tipo de carácter.")

    password = ''.join(secrets.choice(pool) for _ in range(length))
    return password

def main():
    print("=== Generador de Contraseñas Interactivo ===")
    length = ask_int("Longitud de la contraseña", default=16, minimum=4)

    include_upper = ask_bool("¿Incluir MAYÚSCULAS?", default=True)
    include_lower = ask_bool("¿Incluir minúsculas?", default=True)
    include_digits = ask_bool("¿Incluir dígitos?", default=True)
    include_symbols = ask_bool("¿Incluir símbolos (ej: !@#$...)?", default=True)

    count = ask_int("¿Cuántas contraseñas deseas generar?", default=1, minimum=1)

    passwords = []
    for i in range(count):
        pwd = generate_password(length, include_upper, include_lower, include_digits, include_symbols)
        passwords.append(pwd)

    print("\n=== Contraseñas generadas ===")
    for i, p in enumerate(passwords, 1):
        print(f"{i}) {p}")

    if ask_bool("¿Copiar la última contraseña al portapapeles?", default=False):
        if HAVE_PYPERCLIP:
            pyperclip.copy(passwords[-1])
            print("Contraseña copiada al portapapeles ✅")
        else:
            print("⚠️ pyperclip no está instalado. Instálalo con: pip install pyperclip")

if __name__ == "__main__":
    main()