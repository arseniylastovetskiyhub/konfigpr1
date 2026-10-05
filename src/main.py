import os
import tkinter as tk


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


def run_command(output, line):
    """Выполняет команду и пишет результат в output."""
    cmd, args = parse(line)
    if cmd is None:
        return
    output.insert(tk.END, "> " + line + "\n")
    if cmd == "exit":
        raise SystemExit(0)
    if cmd == "ls":
        output.insert(tk.END, "[ls] args: " + str(args) + "\n")
    elif cmd == "cd":
        output.insert(tk.END, "[cd] args: " + str(args) + "\n")
    else:
        msg = "Ошибка: неизвестная команда '" + cmd + "'\n"
        output.insert(tk.END, msg)
    output.see(tk.END)


def on_enter(entry, output, event):
    """Обработчик нажатия Enter."""
    line = entry.get()
    entry.delete(0, tk.END)
    try:
        run_command(output, line)
    except SystemExit:
        entry.winfo_toplevel().destroy()


def main():
    """Точка входа в программу."""
    window = tk.Tk()
    window.title(get_title())
    output = tk.Text(window, height=20, width=80)
    output.pack(padx=10, pady=10)
    entry = tk.Entry(window, width=80)
    entry.pack(padx=10, pady=(0, 10))
    entry.bind("<Return>", lambda e: on_enter(entry, output, e))
    entry.focus_set()
    window.mainloop()


if __name__ == "__main__":
    main()
