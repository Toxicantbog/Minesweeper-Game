import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Minesweeper'
        self.x = 100
        self.y = 100
        self.width = 640
        self.height = 480

        # Variables
        self.map_size = 0
        self.num_bombs = 0
        self.hidden_map = []
        self.map = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        # Function to add a button
        self.add_button()

        self.show()

    def add_button(self):
        #Creates the grid that will be used for the options and for the actual game
        self.grid = QGridLayout()
        button1 = QPushButton('Easy', self)
        button2 = QPushButton('Intermediate', self)
        button3 = QPushButton('Hard', self)

        self.grid.addWidget(button1, 0, 0)
        self.grid.addWidget(button2, 0, 1)
        self.grid.addWidget(button3, 0, 2)

        button1.clicked.connect(lambda: self.maps_init(1))
        button2.clicked.connect(lambda: self.maps_init(2))
        button3.clicked.connect(lambda: self.maps_init(3))

        self.setLayout(self.grid)

    # Makes the map and hidden map array with the num of bombs and hides the difficulty buttons
    def maps_init(self, diff):
        if diff == 1:
            self.num_bombs = 5
            self.map_size = 7
        elif diff == 2:
            self.num_bombs = 10
            self.map_size = 7
        elif diff == 3:
            self.num_bombs = 15
            self.map_size = 10

        self.hidden_map = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.map = [['*' for _ in range(self.map_size)] for _ in range(self.map_size)]

        self.add_bombs()
        self.add_numbers()
        self.remove_current_layout()
        self.add_map()


    

    # Adds the num of bombs to the hidden map
    def add_bombs(self):
        for _ in range(self.num_bombs):
            bomb_x = random.randint(0, self.map_size - 1)
            bomb_y = random.randint(0, self.map_size - 1)

            while self.hidden_map[bomb_y][bomb_x] == 9:
                bomb_x = random.randint(0, self.map_size - 1)
                bomb_y = random.randint(0, self.map_size - 1)

            self.hidden_map[bomb_y][bomb_x] = 9

    #Adds the numbers that corrispond to the bombs to the hidden map
    def add_numbers(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                if self.hidden_map[y][x] == 9:
                    if y == 0:
                        if x == 0:
                            self.add_num(y + 1, x)
                            self.add_num(y + 1, x + 1)
                            self.add_num(y, x + 1)
                        elif x > 0 and x < self.map_size - 1:
                            self.add_num(y, x - 1)
                            self.add_num(y, x + 1)
                            self.add_num(y + 1, x - 1)
                            self.add_num(y + 1, x)
                            self.add_num(y + 1, x + 1)
                        elif x == self.map_size - 1:
                            self.add_num(y, x - 1)
                            self.add_num(y + 1, x - 1)
                            self.add_num(y + 1, x)
                    elif y > 0 and y < self.map_size - 1:
                        if x == 0:
                            self.add_num(y + 1, x)
                            self.add_num(y + 1, x + 1)
                            self.add_num(y, x + 1)
                            self.add_num(y - 1, x + 1)
                            self.add_num(y - 1, x)
                        elif x > 0 and x < self.map_size - 1:
                            self.add_num(y, x - 1)
                            self.add_num(y, x + 1)
                            self.add_num(y + 1, x - 1)
                            self.add_num(y + 1, x)
                            self.add_num(y + 1, x + 1)
                            self.add_num(y - 1, x - 1)
                            self.add_num(y - 1, x + 1)
                            self.add_num(y - 1, x)
                        elif x == self.map_size - 1:
                            self.add_num(y, x - 1)
                            self.add_num(y + 1, x - 1)
                            self.add_num(y + 1, x)
                            self.add_num(y - 1, x - 1)
                            self.add_num(y - 1, x)
                    elif y == self.map_size - 1:
                        if x == 0:
                            self.add_num(y, x + 1)
                            self.add_num(y - 1, x + 1)
                            self.add_num(y - 1, x)
                        elif x > 0 and x < self.map_size - 1:
                            self.add_num(y - 1, x - 1)
                            self.add_num(y - 1, x + 1)
                            self.add_num(y - 1, x)
                            self.add_num(y, x - 1)
                            self.add_num(y, x + 1)
                        elif x == self.map_size - 1:
                            self.add_num(y, x - 1)
                            self.add_num(y - 1, x - 1)
                            self.add_num(y - 1, x)

    #Checks if it can add the numbers to each slot in hidden map
    def add_num(self,cy,cx):
        if self.hidden_map[cy][cx] != 9:
            self.hidden_map[cy][cx] += 1
                            
    #Makes the buttons that will be used for the game
    def add_map(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                button = QPushButton(self.map[y][x],self)
                button.setFixedSize(50,50)
                self.grid.addWidget(button, y, x)
                button.clicked.connect(lambda _,y=y,x=x: self.game(y,x))
                button.customContextMenuRequested.connect(lambda _, y=y, x=x: self.set_flag(y, x))

    def game(self,cord_y,cord_x):
        if self.hidden_map[cord_y][cord_x] == 9:
            self.close()
        self.reveal(cord_y,cord_x)
        self.show_map()
        #self.color_num()

    def reveal(self, cord_y, cord_x):
        if self.hidden_map[cord_y][cord_x] != 9:
            if self.hidden_map[cord_y][cord_x] != 10:
                self.map[cord_y][cord_x] = str(self.hidden_map[cord_y][cord_x])
            if self.hidden_map[cord_y][cord_x] == 0:
                self.hidden_map[cord_y][cord_x] = 10
                if cord_y == 0:
                    if cord_x == 0:
                        self.reveal(cord_y, cord_x + 1)
                        self.reveal(cord_y + 1, cord_x)
                        self.reveal(cord_y + 1, cord_x + 1)
                    elif cord_x > 0 and cord_x < self.map_size - 1:
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y, cord_x + 1)
                        self.reveal(cord_y + 1, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x)
                        self.reveal(cord_y + 1, cord_x + 1)
                    elif cord_x == self.map_size - 1:
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x)
                elif cord_y > 0 and cord_y < self.map_size - 1:
                    if cord_x == 0:
                        self.reveal(cord_y + 1, cord_x)
                        self.reveal(cord_y + 1, cord_x + 1)
                        self.reveal(cord_y, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x)
                    elif cord_x > 0 and cord_x < self.map_size - 1:
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y, cord_x + 1)
                        self.reveal(cord_y + 1, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x)
                        self.reveal(cord_y + 1, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x - 1)
                        self.reveal(cord_y - 1, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x)
                    elif cord_x == self.map_size - 1:
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x - 1)
                        self.reveal(cord_y + 1, cord_x)
                        self.reveal(cord_y - 1, cord_x - 1)
                        self.reveal(cord_y - 1, cord_x)
                elif cord_y == self.map_size - 1:
                    if cord_x == 0:
                        self.reveal(cord_y, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x)
                    elif cord_x > 0 and cord_x < self.map_size - 1:
                        self.reveal(cord_y - 1, cord_x - 1)
                        self.reveal(cord_y - 1, cord_x + 1)
                        self.reveal(cord_y - 1, cord_x)
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y, cord_x + 1)
                    elif cord_x == self.map_size - 1:
                        self.reveal(cord_y, cord_x - 1)
                        self.reveal(cord_y - 1, cord_x - 1)
                        self.reveal(cord_y - 1, cord_x)

    def show_map(self):
        for y in range (self.map_size):
            for x in range (self.map_size):
                button = self.grid.itemAtPosition(y, x).widget()
                if button:
                    button.setText(self.map[y][x])
                    
    def color_num(self):
        for y in range (self.map_size):
            for x in range (self.map_size):
                button = self.grid.itemAtPosition(y, x).widget()
                if self.hidden_map[y][x] == 1:
                    button.setStyleSheet('red')

    def set_flag(self, y, x):
        print(f"Setting flag at ({y}, {x})")
        button = self.grid.itemAtPosition(y, x).widget()
        if button:
            button.setText('F')
        

    def you_lost(self):
        self.remove_current_layout()
        label = QLabel('You lost')
        self.grid.addWidget(label,0,0,1,1)
    



    #Just removes all the widgets from the layout
    def remove_current_layout(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def print_map(self):
        for x in range(self.map_size):
            print(self.map[x])

    def print_hidden_map(self):
        for x in range(self.map_size):
            print(self.hidden_map[x])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
