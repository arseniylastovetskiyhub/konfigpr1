import os
import zipfile
import tkinter as tk
import argparse

def get_title():
    """Формирует заголовок окна."""
    user = os.environ.get("USERNAME")
    host = os.environ.get("COMPUTERNAME")
    return "Эмулятор-[" + user + "@" + host + "]"


def expand_vars(text):
    """Заменяет $VAR на значения переменных окружения."""
    for name, value in os.environ.items():
        text = text.replace("$" + name, value)
    return text


def parse(line):
    """Разбирает строку на команду и аргументы."""
    line = expand_vars(line.strip())
    if not line:
        return None, []
    parts = line.split()
    return parts[0], parts[1:]


def load_vfs_from_zip(zip_path):
    """Загружает ZIP-архив в память как VFS.
    Не распаковывает файлы на диск."""
    try:
        zf = zipfile.ZipFile(zip_path, "r")
        names = zf.namelist()
        print("Загружено файлов в VFS:", len(names))
        return zf
    except FileNotFoundError:
        print("Ошибка: ZIP не найден:", zip_path)
        return None
    except zipfile.BadZipFile:
        print("Ошибка: некорректный ZIP:", zip_path)
        return None


def run_command(output, line):
    """Выполняет команду и пишет результат в output."""
    cmd, args = parse(line)
    if cmd is None:
        return ""
    output.insert(tk.END, "> " + line + "\n")
    if cmd == "exit":
        raise SystemExit(0)
    if cmd == "ls":
        res = "[ls] args: " + str(args)
        output.insert(tk.END, res + "\n")
        return res
    if cmd == "cd":
        res = "[cd] args: " + str(args)
        output.insert(tk.END, res + "\n")
        return res
    msg = "Ошибка: неизвестная команда '" + cmd + "'"
    output.insert(tk.END, msg + "\n")
    return msg


def run_script(output, script_path):
    """Выполняет команды из файла. Останавливается при ошибке."""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        output.insert(tk.END, "Ошибка: файл скрипта не найден\n")
        return
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        result = run_command(output, clean_line)
        if result.startswith("Ошибка"):
            break
    output.see(tk.END)


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs",help="Путь к ZIP-архиву VFS")
    parser.add_argument("--script",help="Путь к стартовому скрипту")
    return parser.parse_args()


def print_debug(args, vfs):
    """Выводит отладочную информацию в консоль."""
    print("VFS путь:", args.vfs)
    print("VFS загружен:", vfs is not None)
    print("Скрипт:", args.script)


def main():
    """Точка входа в программу."""
    args = parse_args()

    vfs = None
    if args.vfs:
        vfs = load_vfs_from_zip(args.vfs)

    print_debug(args, vfs)

    window = tk.Tk()
    window.title(get_title())

    output = tk.Text(window, height=20, width=80)
    output.pack(padx=10, pady=10)

    entry = tk.Entry(window, width=80)
    entry.pack(padx=10, pady=(0, 10))

    def on_enter(event):
        line = entry.get()
        entry.delete(0, tk.END)
        try:
            run_command(output, line)
        except SystemExit:
            window.destroy()

    entry.bind("<Return>", on_enter)
    entry.focus_set()

    if args.script:
        run_script(output, args.script)

    window.mainloop()


if __name__ == "__main__":
    main()
