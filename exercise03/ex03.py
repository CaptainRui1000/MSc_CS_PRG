# -*- coding: utf-8 -*-
"""
Created on Tue Nov 9 12:57:52 2021

@author: ryan
"""


def isPossible(above, nextColumn):
    """
    Determine if the ‘nextRow’ row and ‘nextColumn’ column can hold a queen.

    Parameters
    ----------
    above : List
        A list contains information on which column in each row the queen is in.
        e.g. above[1] == 4 means the Queen in the second row is on the fifth column.
    nextColumn : int
        Column number of the next queen.

    Returns
    -------
    bool
        IF True: available for a Queen.
        IF False: unavailable for a Queen.

    """
    nextRow = len(above)
    for row in range(len(above)):
        column = above[row]
        if abs(column - nextColumn) == 0 or abs(column - nextColumn) == nextRow - row:
            # Determine if there are queens in that column and on the diagonal.
            return False
    return True


def printGrid():
    """
    Print the boards in a more legible way.

    Returns
    -------
    None.

    """
    for row in range(boardSize):
        for column in range(boardSize):
            if positionOnColumn[row] == column:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        if row < boardSize - 1:
            print()
    input("More?")
    # Pause after completing the printing of a board.
    # Press any key to output the next board, e.g. the Enter key.


def recursion():
    """
    Using backtracking, recursively find the solution.

    Not using n as a parameter, because the length of positionOnColumn corresponds to it.

    Returns
    -------
    None.

    """
    global positionOnColumn
    global count
    for column in range(boardSize):
        if isPossible(positionOnColumn, column):
            positionOnColumn += [column]
            # Iterate over columns
            # If it is possible to place a queen, note down the column it is in.
            if len(positionOnColumn) < boardSize:
                recursion()
                # If it is not the last row
                # compute the column of the queen on the next row.
            else:
                count += 1
                printGrid()
                print()
                # Otherwise, +1 to the number of solutions.
                # Print the board and an empty row.
            positionOnColumn = positionOnColumn[: -1]
            # Backtracking and restoring the position information added at last.


def solve():
    """
    Call res() to start recursion and print Total number of solutions

    Returns
    -------
    None.

    """
    recursion()
    print(f"No more! There are ONLY {count} solutions for a board with side length {boardSize}")


boardSize = 8  # Board size
count = 0  # Boards counter
positionOnColumn = []
# A list contains information on which column in each row the queen is in.
# e.g. above[1] == 4 means the Queen in the second row is on the fifth column.
