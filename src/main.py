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
    """Загружает ZIP в дерево папок (словарь)."""
    vfs = {}
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                parts = name.strip("/").split("/")
                current = vfs
                for i, part in enumerate(parts):
                    if not part:
                        continue
                    is_last = (i == len(parts) - 1)
                    if is_last:
                        if name.endswith("/"):
                            current[part] = {
                                "type": "dir",
                                "children": {}
                            }
                        else:
                            try:
                                data = zf.read(name).decode("utf-8")
                            except UnicodeDecodeError:
                                data = "<binary data>"
                            current[part] = {
                                "type": "file",
                                "content": data
                            }
                    else:
                        if part not in current:
                            current[part] = {
                                "type": "dir",
                                "children": {}
                            }
                        current = current[part]["children"]
    except FileNotFoundError:
        print("Ошибка: ZIP не найден:", zip_path)
        return None
    except zipfile.BadZipFile:
        print("Ошибка: некорректный ZIP:", zip_path)
        return None
    return vfs


def get_node_at(vfs, path_parts):
    """Находит узел VFS по списку частей пути."""
    current = vfs
    for part in path_parts:
        if part == "" or part == ".":
            continue
        if part == "..":
            return None
        if current.get("type") == "dir":
            children = current.get("children", current)
            if part in children:
                current = children[part]
            else:
                return None
        elif isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def read_file_from_vfs(cwd, path):
    """Читает файл из VFS. Возвращает (содержимое, ошибка)."""
    node = get_node_at(cwd, path.split("/"))
    if node is None:
        return None, "Файл не найден: " + path
    if node.get("type") != "file":
        return None, "Это не файл: " + path
    return node.get("content", ""), None


def run_command(output, line, vfs, cwd):
    """Выполняет команду. Возвращает (результат, новый_cwd)."""
    cmd, args = parse(line)
    if cmd is None:
        return "", cwd

    output.insert(tk.END, "> " + line + "\n")

    if cmd == "exit":
        raise SystemExit(0)

    if cmd == "ls":
        target = args[0] if args else "."
        if target == ".":
            node = cwd
        else:
            node = get_node_at(cwd, target.split("/"))
        if node is None:
            msg = "Ошибка: путь не найден '" + target + "'"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        if node.get("type") == "file":
            msg = "Ошибка: это файл, не папка"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        children = node.get("children", node)
        names = " ".join(sorted(children.keys()))
        output.insert(tk.END, names + "\n")
        return names, cwd

    if cmd == "cd":
        if not args:
            return "", cwd
        target = args[0]
        if target == "/":
            output.insert(tk.END, "Переход в корень\n")
            return "ok", vfs
        new_cwd = get_node_at(cwd, target.split("/"))
        if new_cwd is None:
            msg = "Ошибка: папка не найдена '" + target + "'"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        if new_cwd.get("type") == "file":
            msg = "Ошибка: это файл, не папка"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        output.insert(tk.END, "Переход в " + target + "\n")
        return "ok", new_cwd

    if cmd == "echo":
        text = " ".join(args) if args else ""
        output.insert(tk.END, text + "\n")
        return text, cwd

    if cmd == "tail":
        if not args:
            msg = "Ошибка: tail требует имя файла"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        n_lines = 10
        file_path = args[-1]
        if len(args) >= 3 and args[0] == "-n":
            try:
                n_lines = int(args[1])
                file_path = args[2]
            except ValueError:
                msg = "Ошибка: неверное число строк"
                output.insert(tk.END, msg + "\n")
                return msg, cwd
        content, err = read_file_from_vfs(cwd, file_path)
        if err:
            msg = "Ошибка: " + err
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        lines = content.split("\n")
        last = lines[-n_lines:] if len(lines) > n_lines else lines
        result = "\n".join(last)
        output.insert(tk.END, result + "\n")
        return result, cwd

    if cmd == "wc":
        if not args:
            msg = "Ошибка: wc требует имя файла"
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        file_path = args[0]
        content, err = read_file_from_vfs(cwd, file_path)
        if err:
            msg = "Ошибка: " + err
            output.insert(tk.END, msg + "\n")
            return msg, cwd
        n_lines = content.count("\n")
        if content and not content.endswith("\n"):
            n_lines += 1
        n_words = len(content.split())
        n_bytes = len(content.encode("utf-8"))
        result = str(n_lines) + " " + str(n_words) + " " + str(n_bytes)
        output.insert(tk.END, result + " " + file_path + "\n")
        return result, cwd

    msg = "Ошибка: неизвестная команда '" + cmd + "'"
    output.insert(tk.END, msg + "\n")
    return msg, cwd


def run_script(output, script_path, vfs, cwd):
    """Выполняет команды из файла. Останавливается при ошибке."""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        output.insert(tk.END, "Ошибка: файл скрипта не найден\n")
        return cwd

    current_cwd = cwd
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        result, current_cwd = run_command(
            output, clean_line, vfs, current_cwd
        )
        if result.startswith("Ошибка"):
            break
    output.see(tk.END)
    return current_cwd


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС"
    )
    parser.add_argument(
        "--vfs",
        help="Путь к ZIP-архиву VFS"
    )
    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту"
    )
    return parser.parse_args()


def print_debug(args, vfs):
    """Выводит отладочную информацию в консоль."""
    print("VFS путь:", args.vfs)
    print("VFS загружен:", vfs is not None)
    print("Скрипт:", args.script)


def main():
    """Точка входа в программу."""
    args = parse_args()

    vfs = {}
    if args.vfs:
        loaded = load_vfs_from_zip(args.vfs)
        if loaded is None:
            print("Ошибка: не удалось загрузить VFS")
            vfs = {}
        else:
            vfs = loaded

    print_debug(args, vfs)

    window = tk.Tk()
    window.title(get_title())

    output = tk.Text(window, height=20, width=80)
    output.pack(padx=10, pady=10)

    entry = tk.Entry(window, width=80)
    entry.pack(padx=10, pady=(0, 10))

    cwd = vfs

    def on_enter(event):
        nonlocal cwd
        line = entry.get()
        entry.delete(0, tk.END)
        try:
            result, new_cwd = run_command(
                output, line, vfs, cwd
            )
            cwd = new_cwd
        except SystemExit:
            window.destroy()

    entry.bind("<Return>", on_enter)
    entry.focus_set()

    if args.script:
        cwd = run_script(output, args.script, vfs, cwd)

    window.mainloop()


if __name__ == "__main__":
    main()
