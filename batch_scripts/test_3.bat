echo.
echo "Test 1: VFS loading - minimal"
echo exit | python emulator.py --vfs-path minimal.csv

echo.
echo "Test 2: VFS loading - deep structure" 
echo exit | python emulator.py --vfs-path deep_structure.csv

echo.
echo "Test 3: VFS loading - few files"
echo exit | python emulator.py --vfs-path few_files.csv

