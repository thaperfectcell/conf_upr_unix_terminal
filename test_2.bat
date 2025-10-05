@echo off
echo === Testing Emulator on Windows ===

echo.
echo Test 1: No arguments
echo exit | python emulator.py

echo.
echo Test 2: Only VFS path
echo exit | python emulator.py --vfs-path test_vfs.csv

echo.
echo Test 3: Only start script
echo exit | python emulator.py --start-script test_script_st2.txt

echo.
echo Test 4: Both arguments
echo exit | python emulator.py --vfs-path test_vfs.csv --start-script test_script_st2.txt

echo.
echo Test 5: Non-existent files
echo exit | python emulator.py --vfs-path not_exist.csv --start-script not_exist.txt