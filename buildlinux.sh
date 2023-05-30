pyinstaller --onefile ./src/DawnLang.py ./src/strings_with_arrows.py
cp -r ./src/dawnLibs/ ./dist/
cp ./src/syntaxlist.txt ./dist/