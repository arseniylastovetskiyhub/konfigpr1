# Shell Emulator

Эмулятор командной оболочки с графическим интерфейсом.
Вариант 18.

## Структура проекта

```text
my-shell/
├── src/
│   ├── __init__.py                # Делает папку src модулем Python
│   └── main.py                    # Главный файл эмулятора (GUI + VFS + команды)
├── tests/
│   ├── __init__.py                # Делает папку tests модулем Python
│   ├── test_with_vfs_minimal.bat  # Тест: минимальный VFS (1 файл)
│   ├── test_with_vfs_files.bat    # Тест: VFS с несколькими файлами (3 файла)
│   ├── test_with_vfs_nested.bat   # Тест: вложенный VFS (3 уровня)
│   ├── test_all_params.bat        # Тест: --vfs + --script вместе
│   ├── test_new_commands.bat      # Тест: новые команды echo, tail, wc
├── VFS/
│   └── test_all_commands.txt      # Стартовый скрипт с командами для эмулятора
├── run.bat                        # Скрипт запуска для Windows
├── create_test_zips.py            # Скрипт создания тестовых ZIP-архивов
├── README.md                      # Документация проекта
└── .gitignore                     # Список файлов, игнорируемых Git
```

## Запуск

Запуск делается через:

```text
run.bat, test_all_params.bat, test_new_commands.bat, test_with_vfs_nested.bat, test_with_vfs_files.bat и test_with_vfs_minimal.bat
```


## Поддерживаемые команды

`ls` - показывает список файлов и папок
	
`cd` - Переходит в другую папку внутри VFS

`echo` - Выводит текст

`tail` - Показывает последние строки файла из VFS

`wc` - Считает строки, слова и байты в файле

`exit` - Закрывает программу
