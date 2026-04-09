@echo off
echo Check and install dependencies...
:: Ensure flet is installed (user has it, but good practice)
pip install flet pyinstaller

echo Cleaning up old build artifacts...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist output rd /s /q output
mkdir output

echo Generating app icon...
python create_icon.py

echo Packaging with 'flet pack' (using current venv)...
:: Using flet pack handles dependencies and assets better than raw PyInstaller
flet pack main.py --name DTCTool --icon app_icon.ico --product-name "DTC Tool" --file-description "DTC Fault Code Converter" --copyright "YangZL" 

echo Moving executable to output folder...
if exist dist\DTCTool.exe (
    move dist\DTCTool.exe output\DTCTool.exe
    echo Success! Executable created at output\DTCTool.exe
) else (
    echo Error: Packaging failed. Please check the output above.
)

pause