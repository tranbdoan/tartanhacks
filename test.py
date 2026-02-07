project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
#5 [Check6-1] & #3 [Check6-2] & #3 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["cellSize"] = data["boardSize"] // data["rows"]
    data["numShips"] = 5
    data["userBoard"] = emptyGrid(data["rows"], data["cols"])
    data["computerBoard"] = emptyGrid(data["rows"], data["cols"])
    data["computerBoard"] = addShips(data["computerBoard"], data["numShips"])
    
    data["tempShip"] = []
    
    data["userShipsPlaced"] = 0
    data["gameStarted"] = False
    
    data["maxTurns"] = 50
    data["turnsMade"] = 0
    
    data["winner"] = None
    



'''
makeView(data, userCanvas, compCanvas)
#6 [Check6-1] & #2 [Check6-2] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userBoard"], showShips = True)
    drawGrid(data, compCanvas, data["computerBoard"], showShips = False)
    
    if data["userShipsPlaced"] < data["numShips"]:
        drawShip(data, userCanvas, data["tempShip"])
    
    drawGameOver(data, userCanvas)
    drawGameOver(data, compCanvas)
    
'''
keyPressed(data, events)
#5 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return" and data["winner"] is not None:
        makeModel(data)


'''
mousePressed(data, event, board)
#5 [Check6-2] & #1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; mouse event object ; str
Returns: None
'''
def mousePressed(data, event, board):
    if data.get("winner") is not None:
        return
    
    if board == "comp":
        board = "computer"
        
    cell = getClickedCell(data, event)
    if cell is None:
        return
    
    if board == "user":
        if data["userShipsPlaced"] < data["numShips"]:
            clickUserBoard(data, cell[0], cell[1])
            
            if data["userShipsPlaced"] == data["numShips"] and not data["gameStarted"]:
                data["gameStarted"] = True
                
    elif board == "computer":
        if data.get("gameStarted", False):
            runGameTurn(data, cell[0], cell[1])

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for r in range(rows):
        newRow = []
        for c in range(cols):
            newRow.append(EMPTY_UNCLICKED)
        grid.append(newRow)
    return grid


'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    shipRowCenter = random.randint(1, 8)
    shipColCenter = random.randint(1, 8)
    placement = random.randint(0, 1)
    ship = []
    if placement == 0:
        ship.append([shipRowCenter - 1, shipColCenter])
        ship.append([shipRowCenter, shipColCenter])
        ship.append([shipRowCenter + 1, shipColCenter])
    else:
        ship.append([shipRowCenter, shipColCenter - 1])
        ship.append([shipRowCenter, shipColCenter])
        ship.append([shipRowCenter, shipColCenter + 1])
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)):
        row = ship[i][0]
        col = ship[i][1]
        if grid[row][col] != EMPTY_UNCLICKED:
            return False
    return True

'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    addedShips = 0
    while addedShips < numShips:
        ship = createShip()
        if checkShip(grid, ship):
            for coordinate in ship:
                row = coordinate[0]
                col = coordinate[1]
                grid[row][col] = SHIP_UNCLICKED
            addedShips = addedShips + 1  
    return grid


'''
drawGrid(data, canvas, grid, showShips)
#6 [Check6-1] & #1 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    cellSize = data["cellSize"]
    rows = data["rows"]
    cols = data["cols"]
    
    for row in range(rows):
        for col in range(cols):
            x0 = col * cellSize
            y0 = row * cellSize
            x1 = x0 + cellSize
            y1 = y0 + cellSize
            
            if grid[row][col] == SHIP_UNCLICKED:
                if showShips:
                    color = "yellow"
                else:
                    color = "blue"
            elif grid[row][col] == SHIP_CLICKED:
                color = "red"
            elif grid[row][col] == EMPTY_CLICKED:
                color = "white"
            else:
                color = "blue"
            
                
            canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = "black")

### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    rows = [coordinate[0] for coordinate in ship]
    cols = [coordinate[1] for coordinate in ship]
    
    if not (cols[0] == cols[1] == cols[2]):
        return False
    
    rows.sort()
    
    return rows[1] == rows[0] + 1 and rows[2] == rows[1] + 1

'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    rows = [coordinate[0] for coordinate in ship]
    cols = [coordinate[1] for coordinate in ship]
    
    if not (rows[0] == rows[1] == rows[2]):
        return False
    
    cols.sort()
    
    return cols[1] == cols[0] + 1 and cols[2] == cols[1] + 1
    
'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            left = col * data["cellSize"]
            top = row * data["cellSize"]
            right = left + data["cellSize"]
            bottom = top + data["cellSize"]
            
            if left <= event.x < right and top <= event.y < bottom:
                return [row, col]
    return None


'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    cellSize = data["cellSize"]
    
    for coordinate in ship:
        row = coordinate[0]
        col = coordinate[1]
        x0 = col * cellSize
        y0 = row * cellSize
        x1 = x0 + cellSize
        y1 = y0 + cellSize
        canvas.create_rectangle(x0, y0, x1, y1, fill = "white", outline = "black")

'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) != 3:
        return False
    
    for coordinate in ship:
        if grid[coordinate[0]][coordinate[1]] != EMPTY_UNCLICKED:
            return False
        
    if not (isVertical(ship) or isHorizontal(ship)):
        return False
    
    if not checkShip(grid, ship):
        return False
    
    return True


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if data["userShipsPlaced"] >= 5:
        print("You already have 5 ships.")
        data["tempShip"] = []
        return 
    
    ship = data["tempShip"]
    
    if shipIsValid(data["userBoard"], ship):
        for coordinate in ship:
            data["userBoard"][coordinate[0]][coordinate[1]] = SHIP_UNCLICKED
            
        data["userShipsPlaced"] += 1
        
        if data["userShipsPlaced"] == 5:
            print("All 5 ships placed! You can start playing now.")
    else:
        print("Invalid ship placement. Try again.")
    
    data["tempShip"] = []
    


'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["userShipsPlaced"] >= 5:
        print("You already have 5 ships.")
        return 

    
    if [row, col] in data["tempShip"]:
        return 
    
    data["tempShip"].append([row, col])
    
    if len(data["tempShip"]) == 3:
        placeShip(data)


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
#1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
        
    if isGameOver(board):
        data["winner"] = player
    return board


'''
runGameTurn(data, row, col)
#1 [Hw6] & #2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["winner"] is not None:
        return
    
    cell = data["computerBoard"][row][col]
    
    if cell == EMPTY_CLICKED or cell == SHIP_CLICKED:
        return
    
    updateBoard(data, data["computerBoard"], row, col, "user")
    
    if isGameOver(data["computerBoard"]):
        data["winner"] = "user"
        return
    
    computerRow, computerCol = getComputerGuess(data["userBoard"])
    updateBoard(data, data["userBoard"], computerRow, computerCol, "computer")
    
    if isGameOver(data["userBoard"]):
        data["winner"] = "computer"
        return
    
    data["turnsMade"] += 1
    if data["turnsMade"] >= data["maxTurns"]:
        data["winner"] = "draw" 


'''
getComputerGuess(board)
#2 [Hw6]
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        
        if board[row][col] in [EMPTY_UNCLICKED, SHIP_UNCLICKED]:
            return [row, col]


'''
isGameOver(board)
#3 [Hw6]
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board:
        if SHIP_UNCLICKED in row:
            return False
    return True


'''
drawGameOver(data, canvas)
#3 [Hw6] & #4 [Hw6] & #5 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] is None:
        return
    
    if data["winner"] == "user":
        message = "Congratulations! You Won!"
    elif data["winner"] == "computer":
        message = "Sorry! You Lost."
    elif data["winner"] == "draw":
        message = "It's a draw!"
    
    canvas.create_text(data["boardSize"] // 2, data["boardSize"] // 2, text = message)
    
    canvas.create_text(data["boardSize"] // 2, data["boardSize"] // 2 + 20, text = "Press Enter to play again!")


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)

