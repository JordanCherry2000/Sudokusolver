import random
import tkinter as tk

newsudoku = [[0] * 9 for _ in range(9)]

# Solve the Sudoku
def sudokusolver(sudoku):
    for v in range(0, 9):
        for h in range(0, 9):
            if sudoku[v][h] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for i in numbers:
                    if linechecker(i, v, h, sudoku):
                        sudoku[v][h] = i
                        if sudokusolver(sudoku):
                            return True
                        sudoku[v][h] = 0
                return False  
    return True

# Check if a number can be placed in the current row, column, and block
def linechecker(tempnumber, vertical, horizontal, sudoku):
    for rowcol in range(0, 9):
        if sudoku[rowcol][horizontal] == tempnumber or sudoku[vertical][rowcol] == tempnumber:
            return False
    vertfloor = (vertical // 3) * 3
    horfloor = (horizontal // 3) * 3
    for vertrange in range(3):
        for horizrange in range(3):
            if sudoku[vertfloor + vertrange][horfloor + horizrange] == tempnumber:
                return False
    return True

# Remove a certain number of numbers from the grid based on difficulty
def newsudokuremover(sudoku, desirednum):
    i = 0
    while i < desirednum:
        randomnum1 = random.randint(0, 8)
        randomnum2 = random.randint(0, 8)
        if sudoku[randomnum1][randomnum2] != 0:
            sudoku[randomnum1][randomnum2] = 0
            i += 1
    return sudoku

# Create a new Sudoku with a selected difficulty
def createnewsudoku(newsudoku):
    sudokusolver(newsudoku)
    global completesudoku
    completesudoku = [row[:] for row in newsudoku]  # Copy the full solution
    # Adjust difficulty: fewer hidden cells for easier levels, more for harder
    if difficulty.get() == 1:  # Easy
        newsudokuremover(newsudoku, 35)
    elif difficulty.get() == 2:  # Medium
        newsudokuremover(newsudoku, 50)
    else:  # Hard
        newsudokuremover(newsudoku, 60)
    update_ui()

# Function to update the UI with the new Sudoku numbers
def update_ui():
    for i in range(9):
        for j in range(9):
            sudoku_cells[i][j].delete(0, tk.END)  # Clear the cell
            if newsudoku[i][j] != 0:
                sudoku_cells[i][j].insert(0, str(newsudoku[i][j]))  # Insert the new value
                sudoku_cells[i][j].config(state='readonly', fg="grey")
            else:
                sudoku_cells[i][j].config(state='normal', fg="white")

# Function to check if the user's solution matches the correct solution
def checksudoku():
    user_input = [[0] * 9 for _ in range(9)]  # Create a grid for user input

    # Get the values entered by the user in the grid
    for i in range(9):
        for j in range(9):
            value = sudoku_cells[i][j].get()
            if value.isdigit():  # Check if the entry is a number
                user_input[i][j] = int(value)
            else:
                user_input[i][j] = 0  # If the cell is empty or invalid, consider it as 0

    # Compare the user input grid with the complete solution
    if user_input == completesudoku:
        correctlabel.config(text="Correct")
    else:
        correctlabel.config(text="Incorrect")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Sudoku")
root.geometry("900x900")   

# Create a frame to hold the grid
frame = tk.Frame(root)
frame.pack()

# Create a Canvas widget for drawing the grid
canvas = tk.Canvas(frame, width=540, height=540)
canvas.grid(row=0, column=0, padx=5, pady=5)

# Draw the Sudoku grid
def draw_grid():
    cell_size = 60
    thick_line_width = 3
    thin_line_width = 1

    # Draw the 9x9 grid
    for i in range(10):
        # Draw horizontal lines
        if i % 3 == 0:
            canvas.create_line(0, i * cell_size, 9 * cell_size, i * cell_size, fill="black", width=thick_line_width)
        else:
            canvas.create_line(0, i * cell_size, 9 * cell_size, i * cell_size, fill="black", width=thin_line_width)

        # Draw vertical lines
        if i % 3 == 0:
            canvas.create_line(i * cell_size, 0, i * cell_size, 9 * cell_size, fill="black", width=thick_line_width)
        else:
            canvas.create_line(i * cell_size, 0, i * cell_size, 9 * cell_size, fill="black", width=thin_line_width)

# Draw the grid when the window is initialized
draw_grid()

# Create a 9x9 grid of Entry widgets for Sudoku cells
sudoku_cells = [[None for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entry = tk.Entry(frame, width=3, justify='center', font=('Arial', 18))
        entry.place(x=j * 60 + 5, y=i * 60 + 5, width=50, height=50)  # Position Entry widgets on top of the grid
        sudoku_cells[i][j] = entry

# Add a frame for difficulty level buttons
difficulty_frame = tk.Frame(root)
difficulty_frame.pack(pady=10)

# Difficulty level variable
difficulty = tk.IntVar()
difficulty.set(1)  # Default to "Easy"

# Add difficulty radio buttons
tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty, value=1).pack(side=tk.LEFT)
tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty, value=2).pack(side=tk.LEFT)
tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty, value=3).pack(side=tk.LEFT)

# Add a button to generate Sudoku
generate_button = tk.Button(root, text="Generate Sudoku", command=lambda: createnewsudoku(newsudoku))
generate_button.pack(pady=20)

# Add the Check Sudoku button
check_button = tk.Button(root, text="Check Sudoku", command=checksudoku)
check_button.pack(pady=20)

# Label to display the result of the check
correctlabel = tk.Label(root, text="")
correctlabel.pack(pady=10)  # Add the correct label to the window

# Start the Tkinter main loop
root.mainloop()
