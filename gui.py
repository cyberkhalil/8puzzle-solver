from PyQt5 import QtWidgets, uic
from copy import deepcopy


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('puzzle8.ui', self)  # Load the .ui file
        self.scrolResult = QtWidgets.QVBoxLayout(self.scrolWidget)
        self.show()  # Show the GUI


# Create an instance of QtWidgets.QApplication
app = QtWidgets.QApplication([])
window = Ui()  # Create an instance of our class


class puzzle:
    def __init__(self, initial, goal_state, up=None, result=None):
        self.initial = initial
        self.goal_state = goal_state
        self.up = up
        self.f = 0
        self.g = 0
        self.h = 0
        if result is None:
            self.result = ""
        else:
            self.result = result

    def move_function(self):
        curr = self.initial
        for i in range(3):
            for j in range(3):  # move function to move the tile
                if curr[i][j] == 0:
                    x, y = i, j
                    break
        q = []
        if x-1 >= 0:
            b = deepcopy(curr)
            b[x][y] = b[x-1][y]
            b[x-1][y] = 0
            succ = puzzle(initial=b, up=curr, goal_state=self.goal_state,
                          result=self.result+"U")
            q.append(succ)
        if x+1 < 3:
            b = deepcopy(curr)
            b[x][y] = b[x+1][y]
            b[x+1][y] = 0
            succ = puzzle(initial=b, up=curr, goal_state=self.goal_state,
                          result=self.result+"D")
            q.append(succ)
        if y-1 >= 0:
            b = deepcopy(curr)
            b[x][y] = b[x][y-1]
            b[x][y-1] = 0
            succ = puzzle(initial=b, up=curr, goal_state=self.goal_state,
                          result=self.result+"L")
            q.append(succ)
        if y+1 < 3:
            b = deepcopy(curr)
            b[x][y] = b[x][y+1]
            b[x][y+1] = 0
            succ = puzzle(initial=b, up=curr, goal_state=self.goal_state,
                          result=self.result+"R")
            q.append(succ)
        return q

    def manhattan_search(self):
        h = 0
        for i in range(3):  # Manhattan definition
            for j in range(3):
                # getting the remainder and quotient of the  current value
                x, y = divmod(self.initial[i][j], 3)
                g1, g2 = divmod(self.goal_state[i][j], 3)
                h += abs(x-g1) + abs(y-g2)  # calculating manhanttan distance
        return h

    def check_goal(self):
        # checking whether goal state is achieved

        for i in range(3):
            for j in range(3):
                if self.initial[i][j] != self.goal_state[i][j]:
                    return False
        return True

    def __eq__(self, other):
        return self.initial == other.initial


def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if(item.f < f):
            f = item.f
            index = i

    return openList[index], index


def plain(label):
    try:
        return int(label.text())
    except:
        return 0


def AStar():

    initalState = [
        [plain(window.P0), plain(window.P1), plain(window.P2)],
        [plain(window.P3), plain(window.P4), plain(window.P5)],
        [plain(window.P6), plain(window.P7), plain(window.P8)]
    ]
    # initalState = [[2, 3, 6], [0, 4, 5], [8, 1, 7]]
    goal_state = [
        [plain(window.R0), plain(window.R1), plain(window.R2)],
        [plain(window.R3), plain(window.R4), plain(window.R5)],
        [plain(window.R6), plain(window.R7), plain(window.R8)]
    ]
    # goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    start = puzzle(initalState, goal_state)
    openList = []
    closedList = []
    openList.append(start)

    while openList:
        current, index = best_fvalue(openList)
        if current.check_goal():
            window.scrolResult.addWidget(
                QtWidgets.QLabel(str(current.initial)))
            t = current.up
            noofMoves = 0
            while t:
                noofMoves += 1
                window.scrolResult.addWidget(QtWidgets.QLabel(str(t.initial)))
                t = t.up
            window.resultL1.setText("Puzzle Solved !!")
            window.resultL2.setText(
                "Open+Close Lists Nodes: "+str(len(openList)+len(closedList))+"\tMoves: "+str(noofMoves))
            window.scrolResult.addWidget(
                QtWidgets.QLabel("Result: "+str(current.result)))
            return 1

        openList.pop(index)
        closedList.append(current)

        X = current.move_function()
        for move in X:
            ok = False  # checking in closedList
            for item in closedList:
                if item == move:
                    ok = True
                    break
            if not ok:  # not in closed list
                newG = current.g + 1
                present = False

                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].up = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan_search()
                    move.f = move.g + move.h
                    move.up = current
                    openList.append(move)
    window.resultL1.setText("Puzzle Can't be solved !")
    return 0


window.resultBtn.clicked.connect(AStar)
app.exec_()  # Start the application
