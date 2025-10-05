# Эмулятор Командной Строки UNIX

Эмулятор командной строки UNIX-подобной оболочки. Разработан в рамках учебного задания по дисциплине "Конфигурационное управление" в РТУ МИРЭА.

## Функционал
* команды `ls`, `cd`, `exit`, `du`, `whoami`, `uptime`, `echo`, `chmod`, `cp`
* виртуальная файловая система на основе csv-файла
* возможность смены исходной vfs во время работы эмулятора при помощи `vfs-load`

Для сборки запустить следующие команды

```bash
git clone git@github.com:thaperfectcell/conf_upr_unix_terminal.git
cd conf_upr_unix_terminal
python emulator.py --vfs-path vfs_variants/minimal.csv --start-script start_scripts/test_script_st5.txt
```

