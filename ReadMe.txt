REQUIREMENTS
You need Python installed.
You need the package venv installed.
You need the package Kivy installed.

INSTALLATION
----------------------------------------------
1. Ensure Python is installed.
2. After extracting the folder if it was downloaded as a .zip
3. If the 'MyVenv' folder exists, you need to delete it, you need your own instance of a venv
4. Open the CMD (Command Prompt) at the main directory of the project.

5. To initialize venv, run: python -m venv MyVenv
6. Press Enter.
7. To activate the virtual environment:
   on Windows: .\MyVenv\Scripts\activate
   on macOS/Linux: source MyVenv/bin/activate
8. Press Enter.
9. Install Kivy with: pip install kivy
10. Press Enter.

TO START THE GAME
----------------------------------------------
If the installation process is complete you can use the StartApp.bat
you just need to click it like an icon.
alternatively
If the virtual environment is still active, start at step 3.
1. Open the CMD at the main directory of the project.
2. To activate the virtual environment:
   on Windows: .\MyVenv\Scripts\activate
   on macOS/Linux: source MyVenv/bin/activate
3. Start the game by running: python src/minesweeper.py
4. Press Enter.

CLOSING THE VIRTUAL ENVIRONMENT
1: To deactivate MyVenv, type: deactivate
4. Press Enter.

BUG
----------------------------------------------
I have experanced a problem when trying to start the project from CMD,
I used VSCode to create the project, starting the project from the VSCode terminal does work for me anyway.


