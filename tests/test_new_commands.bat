@echo off 
echo Тест: новые команды echo, tail, wc 
python ..\src\main.py --vfs ..\VFS\vfs_nested.zip --script ..\VFS\test_all_commands.txt 
pause 
