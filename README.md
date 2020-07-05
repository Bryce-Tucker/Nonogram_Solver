# Nonogram Solver
## Cheating your way to the top of the leaderboards

---

 ![Gif of program in action](demo.gif)
 
 ### Required Python Modules
This program requires two third party modules:
1. **Selenium** : A module that allows for automated interaction with web pages
2. **Numpy** : A module being used here for handling multi-dimensional arrays

These modules can be installed with throught pip using the command `pip install selenium numpy`

Selenium also requires a compatible driver for the browser of choice to be installed, this code calls for a Firefox driver.
Detailed installation instructions can be found here: https://selenium-python.readthedocs.io/installation.html

### Running the Program
Once the required modules are installed, navigate to the folder containing the script in the Command Prompt.

The command `python scraper.py` will open the browser and solve a puzzle from https://www.puzzle-nonograms.com/
The command `python solver.py` will solve the demo puzzle included with the program.

### Changing Settings
The scraper program will load and solve a 5x5 puzzle by default. To change the size of the puzzle, provide the `puzzle_nonograms` function call with a size the desired size argument in the `main` function in `scraper.py`

The size arguments are as follows:
- 0 (or no argument): 5x5
- 1: 10x10
- 2: 15x15
- 3: 20x20
- 4: 25x25
- 5: Special Weekly Nonograms
- 6: Special Daily Nonograms
- 7: Special Monthly Nonograms

