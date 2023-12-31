from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_hex_from_color

import random
import copy


class KivySudokuApp(App):
    def build(self):
        return Sudoku()

    def close_application(self): 
        App.get_running_app().stop() 
        Window.close()


class MenuWidget(RelativeLayout):
    pass   


class MenuWidget2(RelativeLayout):
    pass   


class MenuWidget3(RelativeLayout):
    pass   


class SmallGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.buttons = []

        for i in range(9):
            obj = SudokuButton()
            self.add_widget(obj)  
            self.buttons.append(obj) 


class BigGrid(GridLayout):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.grids = []

        for i in range(9):
            obj = SmallGrid()
            self.add_widget(obj)  
            self.grids.append(obj)    


class SudokuButton(Button):
    last_key = ""
    locked = False
    number = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.background_normal = ""
        self.background_color = (0.2, 0.2, 0.2)
    
        
    def on_press(self):
        super().on_press()
        
        if not self.locked:
            self.text = self.last_key
        if not self.locked and self.last_key == "spacebar":
            self.text = self.number    
        
        
class Sudoku(BoxLayout):
    original_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    player_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    useable_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]  
    
    seconds_passed = 0
    minutes_passed = 0
    over = False
    
    last_key = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'vertical'
        
        self.layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), pos_hint = {'x':0, 'y':0})
        
        self.quitbtn = Button(text = "quit",
                           font_size = self.height * 0.5,
                           font_name = "label_font.ttf",
                           color = (0, 0.25, 0.3, 1),
                           bold = True,
                           size_hint = (0.5, 0.75))
        self.quitbtn.bind(on_press = self.quitback)
        
        self.clearbtn = Button(text = "clear",
                           font_size = self.height * 0.5,
                           font_name = "label_font.ttf",
                           color = (0, 0.25, 0.3, 1),
                           bold = True,
                           size_hint = (0.5, 0.75))
        self.clearbtn.bind(on_press = self.clearback)
        
        
        self.layout.add_widget(self.quitbtn)
        self.layout.add_widget(self.clearbtn)

        self.timer = Label(font_size = self.height * 0.2,
                           font_name = "label_font.ttf",
                           color = (0, 0.75, 0.3, 1),
                           bold = True,
                           size_hint = (1, 0.05))
        
        self.number = Label(font_size = self.height * 0.2,
                           font_name = "label_font.ttf",
                           color = (0, 0.75, 0.3, 1),
                           bold = True,
                           size_hint = (1, 0.05))
        
        self.grid = BigGrid(pos_hint = {"center_x": 0.5, "center_y:": 0.5})
        
        self.menu = MenuWidget()
        
        self.add_widget(self.menu)
        
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down = self.on_key_down)
        
        Clock.schedule_interval(self.update, 1/4)

    def quitback(self, event):       
        self.remove_widget(self.grid)
        self.remove_widget(self.layout)
        self.remove_widget(self.timer)
        self.remove_widget(self.number)
        self.add_widget(Sudoku())
        
        
    def clearback(self, event):
        for i in range(9):
            for j in range(9):
                if get_hex_from_color(self.grid.grids[i].buttons[j].background_color) == "#333333ff":
                    self.grid.grids[i].buttons[j].text = ''


    def on_key_down(self, keyboard, keycode, text, modifiers):
        for i in range(1, 10):
            if keycode[1] == str(i):
                self.last_key = str(i)
        if keycode[1] == "backspace":
            self.last_key = ""
        if keycode[1] == "spacebar":
            self.last_key = "spacebar"
        self.help()
        return True
    
    
    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.on_key_down)
        self._keyboard = None
    
    
    def original_board_init(self):
        count = 0
        for i in range(81):
            row = int(i/9)
            col = i%9        
            if self.original_board[row][col] == 0:
                random.shuffle(self.useable_values)      
                for value in self.useable_values:
                    if self.value_check(row, col, value, self.original_board):
                        self.original_board[row][col] = value
                        if self.is_full(self.original_board):
                            print("Count1: ",count)
                            return True
                if self.original_board[row][col] == 0:
                    self.original_board[row][col] = ""
                    count =+ 1
        print("Count2: ",count)


    def player_board_init(self, to_del):
        self.player_board = copy.deepcopy(self.original_board)
        to_remove = random.sample(range(81), to_del)
        
        for i in to_remove:
            row = int(i/9)
            col = i%9  
            self.player_board[row][col] = ""
    
        self.print_board(self.player_board)
        
            
    def print_board(self, board): 
        list1 = []
        list2 = []
                
        for i in range (0, 7, 3):
            for j in range(0, 7, 3):
                for k in range (3):
                    for l in range(3): 
                        list1.append(i + k)
                        list2.append(j + l)
                        
        for i in range(9):
            for j in range(9):
                grid = list1.pop(0)
                button = list2.pop(0)
                self.grid.grids[grid].buttons[button].text = str(board[i][j])
                self.grid.grids[grid].buttons[button].number = str(self.original_board[i][j])
                if self.grid.grids[grid].buttons[button].text != "":
                    self.grid.grids[grid].buttons[button].locked = True
                    self.grid.grids[grid].buttons[button].background_color = (0.15, 0.15, 0.15, 1)           


    def is_full(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0 or board[row][col] == "":
                    return False
        return True
                    
                    
    def value_check(self, row, col, value, board):
        R = int(row/3) * 3
        C = int(col/3) * 3
        
        for i in range(9):
            if board[i][col] == value:
                return False
            for j in range(9):
                if board[row][j] == value:
                    return False
        for i in range(R, R + 3):
            for j in range(C, C + 3):
                if value == board[i][j]:
                    return False
        return True

                
    def update(self, dt):
        if not self.over:
            self.seconds_passed += dt
            
            self.number.text = "Enter number: " + str(self.last_key)
            
            for i in range(9):
                for j in range(9):
                    self.grid.grids[i].buttons[j].last_key = self.last_key
                    self.player_board[i][j] = self.last_key
                    
            self.update_board() 
            self.update_time() 
                
            if self.is_over():
                self.game_over() 
        
    
    def help(self):
        for i in range(81):
            grid = int(i/9)
            button = i%9
            if self.last_key == "":
                if not self.grid.grids[grid].buttons[button].locked:
                    self.grid.grids[grid].buttons[button].background_color = (0.2, 0.2, 0.2)
                else:
                    self.grid.grids[grid].buttons[button].background_color = (0.15, 0.15, 0.15, 1)
            elif self.grid.grids[grid].buttons[button].text == self.last_key:
                self.grid.grids[grid].buttons[button].background_color = (0, 0.15, 0.2, 1)
            elif not self.grid.grids[grid].buttons[button].locked:
                self.grid.grids[grid].buttons[button].background_color = (0.2, 0.2, 0.2)
            else:
                self.grid.grids[grid].buttons[button].background_color = (0.15, 0.15, 0.15, 1)                


    def is_over(self):
        for i in range(81):
            row = int(i/9)
            col = i%9
            
            if self.player_board[row][col] == "":
                return False
        return True


    def check_smallgrid(self, prm, board):
        counts = [0,0,0,0,0,0,0,0,0]
        R = int(prm/3) * 3
        C = prm%3 * 3
        for i in range(9):
            row = int(i/3)
            col = i%3
            val = board[R+row][C+col]
            j = int(val) - 1
            counts[j]+=1
            if counts[j] == 2:
                return False
        return True

        
    def check_row(self, prm, board):
        counts = [0,0,0,0,0,0,0,0,0]
        for j in range(9):
            val = board[prm][j]
            k= int(val) - 1
            counts[k]+=1
            if counts[k] == 2:
                return False
        return True
        
        
    def check_col(self, prm, board):
        counts = [0,0,0,0,0,0,0,0,0]
        for j in range(9):
            val = board[j][prm]
            k= int(val) - 1
            counts[k]+=1
            if counts[k] == 2:
                return False
        return True

        
    def game_over(self):
        self.over = True
        self.correct = True
        
        self.remove_widget(self.grid)
        self.remove_widget(self.layout)
        self.remove_widget(self.timer)
        self.remove_widget(self.number)
        
        for i in range(9): 
            if self.check_smallgrid(i, self.player_board):
                self.correct = True
            else:
                self.correct = False
                break
                
        for i in range(9):
            if self.check_row(i, self.player_board):
                self.correct = True
            else:
                self.correct = False
                break 

        for i in range(9):
            if self.check_col(i, self.player_board):
                self.correct = True
            else:
                self.correct = False
                break
                            
        if self.correct:
            self.menu3 = MenuWidget3()
            self.add_widget(self.menu3)
        else:
            self.menu2 = MenuWidget2()
            self.add_widget(self.menu2)
        
    
    def new_game(self):
        self.remove_widget(self.menu3)
        self.add_widget(Sudoku())
        
        
    def new_game_incorrect(self):
        self.remove_widget(self.menu2)        
        self.add_widget(Sudoku())
        
                
    def update_time(self):
        if self.seconds_passed > 60:
            self.seconds_passed -= 60
            self.minutes_passed += 1
            
        seconds = str(format(int(self.seconds_passed), '02'))
        minutes = str(format(self.minutes_passed, '02'))
        
        self.timer.text = "Time: " + minutes + ":" + seconds
     
     
    def update_board(self):
        list1 = []
        list2 = []
         
        for i in range (0, 7, 3):
            for j in range(0, 7, 3):
                for k in range (3):
                    for l in range(3): 
                        list1.append(i + k)
                        list2.append(j + l)
                        
        for i in range(9):
            for j in range(9):
                grid = list1.pop(0)
                button = list2.pop(0)
                self.player_board[i][j] = self.grid.grids[grid].buttons[button].text
            
        
    def easy_button(self):
        self.switch_menu() 
        self.player_board_init(31)    
        
        
    def medium_button(self):
        self.switch_menu()
        self.player_board_init(51) 
        
        
    def hard_button(self):
        self.switch_menu()
        self.player_board_init(61) 
        
    
    def switch_menu(self):
        self.seconds_passed = 0
        self.minutes_passed = 0
        self.over = False
        
        self.original_board_init()
        
        self.remove_widget(self.menu)
        
        self.add_widget(self.layout)
        self.add_widget(self.timer)
        self.add_widget(self.number)
        self.add_widget(self.grid) 


KivySudokuApp().run()
