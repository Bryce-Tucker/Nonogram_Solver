import solver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def _pN_getInstructions(taskTop, taskLeft):
    colInstructions = []
    topTasks = taskTop.find_elements_by_class_name("task-group")
    for task in topTasks:
        cells = task.find_elements_by_class_name("task-cell")
        colInstructions.append([])
        for cell in cells:
            if (cell.text != ""):
                colInstructions[-1].append(int(cell.text))
    leftTasks = taskLeft.find_elements_by_class_name("task-group")

    rowInstructions = []
    for task in leftTasks:
        cells = task.find_elements_by_class_name("task-cell")
        rowInstructions.append([])
        for cell in cells:
            if (cell.text != ""):
                rowInstructions[-1].append(int(cell.text))

    return(colInstructions, rowInstructions)


def _pN_populateBoard(solution, cells):
    flattened = solution.flatten()
    for index in range(len(flattened)):
        if (flattened[index] == 1):
            cells[index].click()

def puzzle_nonograms(size = 0):
    link = "https://www.puzzle-nonograms.com/?size=" + str(size)

    browser = webdriver.Firefox()
    browser.get(link)

    time.sleep(5)


    taskTop = browser.find_element_by_id("taskTop")
    taskLeft = browser.find_element_by_id("taskLeft")

    colInstructions, rowInstructions = _pN_getInstructions(taskTop, taskLeft)

    solvedBoard = solver.solvePuzzle(colInstructions, rowInstructions)

    cells = browser.find_elements_by_class_name("cell")

    _pN_populateBoard(solvedBoard, cells)


    done = browser.find_element_by_id("btnReady")
    done.click()


def main():
    puzzle_nonograms()

if __name__ == '__main__':
    main()
