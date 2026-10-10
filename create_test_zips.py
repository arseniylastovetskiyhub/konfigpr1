"""Скрипт для создания тестовых ZIP-архивов в папке VFS."""
import os
import zipfile


def create_minimal_zip():
    """Создаёт минимальный ZIP с одним файлом."""
    path = os.path.join("VFS", "vfs_minimal.zip")
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("hello.txt", "Привет, мир!")


def create_files_zip():
    """Создаёт ZIP с несколькими файлами."""
    path = os.path.join("VFS", "vfs_files.zip")
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("readme.txt", "Описание проекта")
        zf.writestr("data.txt", "12345")
        zf.writestr("notes.txt", "Заметки")


def create_nested_zip():
    """Создаёт ZIP с 3 уровнями вложенности."""
    path = os.path.join("VFS", "vfs_nested.zip")
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("root_file.txt", "Файл в корне")
        zf.writestr("docs/readme.txt", "Документация")
        zf.writestr("docs/guide.txt", "Руководство")
        zf.writestr("docs/api/endpoints.txt", "API")
        zf.writestr("docs/api/auth.txt", "Авторизация")
        zf.writestr("src/main.py", "print('hello')")
        zf.writestr("src/utils/helper.py", "def help(): pass")


def main():
    """Создаёт все тестовые архивы в папке VFS."""
    os.makedirs("VFS", exist_ok=True)
    create_minimal_zip()
    create_files_zip()
    create_nested_zip()
    print("Созданы архивы в папке VFS/:")
    for name in os.listdir("VFS"):
        if name.endswith(".zip"):
            print(" - " + name)


if __name__ == "__main__":
    main()
