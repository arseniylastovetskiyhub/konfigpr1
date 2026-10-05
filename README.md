# Shell Emulator

Эмулятор командной оболочки с графическим интерфейсом.
Вариант 18.

## Структура проекта

```text
my-shell/
├── src/
│   ├── __init__.py       # Делает папку src модулем Python
│   └── main.py           # Главный файл эмулятора (GUI + логика)
├── tests/
│   ├── __init__.py       # Делает папку tests модулем Python
│   └── test_all_params.bat   # Тест: запуск с обоими параметрами
│   ├── test_with_script.bat  # Тест: запуск со скриптом
│   ├── test_with_vfs.bat     # Тест: запуск с --vfs
├── VFS/
│   └── test_script.txt   # Тестовый скрипт с командами для эмулятора
├── run.bat               # Скрипт запуска для Windows
├── README.md             # Документация проекта
└── .gitignore            # Список файлов, игнорируемых Git
```

## Запуск

Запуск делается через:

```text
run.bat, test_with_script.bat, test_with_vfs.bat или test_all_params.bat
```

## Поддерживаемые команды

Команды-заглушки - `ls` и `cd`.

Команда-выход - `exit`.

