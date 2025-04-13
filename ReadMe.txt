REQUIREMENTS
You need Python installed.
You need the package venv installed.
You need the package Kivy installed.

INSTALLATION
----------------------------------------------
1. Ensure Python is installed.
2. Open the CMD (Command Prompt) at the main directory of the project.
3. To initialize venv, run: python -m venv MyVenv
4. Press Enter.
5. To activate the virtual environment:
   on Windows: .\MyVenv\Scripts\activate
   on macOS/Linux: source MyVenv/bin/activate
6. Press Enter.
7. Install Kivy with: pip install kivy
8. Press Enter.

TO START THE GAME
----------------------------------------------
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

Notes
----------------------------------------------
I have added some solver code. 
A fetcher that stops more flags being added then there are mines,
and if all mines are fanged correctly an automatic win, for blind luck cases.
