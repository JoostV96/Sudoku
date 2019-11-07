# Sudoku
GUI to play sudoku

Sudoku.py reads the sudoku from a .txt file where the sudoku is stored as a list of lists. 
After reading it, it is displayed on a GUI for the user to play it. The GUI is made with the Pygame package. 
To insert a number, use the keyboard to select a number and hit enter to finalize it. 
On the GUI, there is a "hint" button. When there is a hint available, the action of clicking the button will highlight the corresponding cell. If the user is done playing, press the "solve" button to see the solution. If the user has made an error, it is displayed on the window. 
In case one wants all pencil marks to appear when the hint button is clicked to make the sudoku easier to solve, uncomment line 65. 

Sudoku_reader.py displays an empty sudoku grid on which the user can input his/her own sudoku. After completing it, click on "done" and exist the window. Clicking on "done" will write the sudoku grid to the .txt file which can then be read in using the sudoku.py program.

Sudoku.txt contains the sudoku grid stored as a list of lists. This file is overwritten each time the "done" button is pressed in Sudoku_reader.py. 
