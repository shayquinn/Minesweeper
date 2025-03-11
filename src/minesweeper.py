from kivy.app import App

from kivy.graphics.texture import TextureRegion
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionView, ActionLabel, ActionButton, ActionPrevious
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.properties import ListProperty

import os
import random

grid_layout = None
sprite_sheet_path = None
sprite_size = None  # Replace with your sprite size
num_rows, num_cols = None, None
map = None
selected_map = None
game_over = None
you_win = None

dropdown = None

sound1, sound2, sound3, sound4 = None, None, None, None
font1_path = None
flag_label = None
flaged_cells = 0
value_map = {
    0: 12,
    1: 13,
    2: 14,
    3: 15,
    4: 8,
    5: 9,
    6: 10,
    7: 11,
    8: 4,
    9: 2
}

class FastActionButton(ActionButton):
    pressed_color = ListProperty([1, 0, 0, 1])  # Red color when pressed

    def on_press(self):
        self.background_color = self.pressed_color

    def on_release(self):
        self.background_color = self.color

class SingleSprite(Widget):
    def __init__(self, sprite_sheet_path, sprite_index, **kwargs):
        super(SingleSprite, self).__init__(**kwargs)
        self.sprite_sheet = CoreImage(sprite_sheet_path).texture
        self.sprite_index = sprite_index
        self.update_texture()
    
    def update_texture(self):
        sprite_size = self.sprite_sheet.width // 4  # Assuming a 4x4 grid
        i = self.sprite_index % 4
        j = self.sprite_index // 4
        region = TextureRegion(i * sprite_size, j * sprite_size, sprite_size, sprite_size, self.sprite_sheet)
        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=region, pos=self.pos, size=self.size)

    def change_sprite(self, new_index):
        self.sprite_index = new_index
        self.update_texture()

class SpriteGrid(Widget):
    def __init__(self, **kwargs):
        super(SpriteGrid, self).__init__(**kwargs)

        global game_over
        game_over = False
        global you_win
        you_win = False

        self.size = (num_cols * sprite_size, num_rows * sprite_size)  # Set the size of the widget
        self.sprites = []  # Initialize an empty list to keep track of sprite widgets
        
        self.mine_count = (num_cols * num_rows) // 6
        self.not_mine_count = (num_cols * num_rows) - self.mine_count

        global flaged_cells
        flaged_cells = self.mine_count
        flag_label.text = 'Flags: {}'.format(flaged_cells) 

        global map
        map = create_map(num_cols, num_rows, self.mine_count)
        for row in reversed(map):
            #print(' '.join(str(cell) for cell in row))
            pass
        global selected_map
        selected_map = [[1 for _ in range(num_cols)] for _ in range(num_rows)]

        # Create a grid of sprites
        for y in range(num_rows):
            for x in range(num_cols):
                # Determine the appropriate sprite index or type; using '5' as a placeholder
                sprite_index = 5
                single_sprite = SingleSprite(sprite_sheet_path, sprite_index, pos=(x * sprite_size, y * sprite_size), size=(sprite_size, sprite_size))
                self.add_widget(single_sprite)
                self.sprites.append(single_sprite)  # Track the sprite

    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(max(0, row - 1), min(row + 2, len(map))):
            for j in range(max(0, col - 1), min(col + 2, len(map[0]))):
                if (i, j) != (row, col):
                    selected_map[i][j] = 0
                    if map[i][j] == 0:
                        neighbours.append((i, j))
        return neighbours

    def find_zero_cells(self, row, col):
        neighbour_zeros = self.get_neighbours(row, col)
        checked_cells = set((row, col))
        while neighbour_zeros:
            # Iterate over a copy of the list
            for (i, j) in neighbour_zeros.copy():
                neighbour_zeros.remove((i, j))
                # Only add the neighbours that haven't been checked yet
                new_neighbours = [(x, y) for (x, y) in self.get_neighbours(i, j) if (x, y) not in checked_cells]
                neighbour_zeros += new_neighbours
                checked_cells.update(new_neighbours)

    
    def on_touch_down(self, touch):     
        
        if self.x <= touch.x <= self.x + self.width and self.y <= touch.y <= self.y + self.height:
            print("on_touch_down") 

            
            array_x = int(touch.x // sprite_size)
            array_y = int(touch.y // sprite_size)
            global game_over
            if game_over != True:
                print(f"selected_map: {selected_map[array_y][array_x]}")  
                global sound1             
                if touch.button == 'left':
                    if(selected_map[array_y][array_x] == 1):
                        if sound1.state != 'play':
                            sound1.play()
                        else:
                            sound1.stop()
                            sound1.play() 
                        if(map[array_y][array_x] == 9):      
                            game_over = True
                            selected_map[array_y][array_x] = 4
                            self.update_screen()
                            #print("Game Over")
                        elif map[array_y][array_x] == 0:
                            selected_map[array_y][array_x] = 0
                            self.find_zero_cells(array_y, array_x)
                            self.update_screen()
                            sound3.play()
                            #print("Find zeros")
                        else:
                            selected_map[array_y][array_x] = 0
                            self.update_screen()
                            #print(f"Touch down on sprite at array position {array_x}, {array_y}")  
                    # check not_mine_count
                    count = 0
                    for row in selected_map:
                        for i in row:
                            if i == 0:
                                count += 1
                    if count == self.not_mine_count:
                        game_over = True
                        global you_win
                        you_win = True
                        sound4.play()
                    self.update_screen()
                    #print(f"not_mine_count: {self.not_mine_count} count: {count}")

                elif touch.button == 'right':           
                    if(selected_map[array_y][array_x] != 0):
                        if sound1.state != 'play':
                            sound1.play()
                        else:
                            sound1.stop()
                            sound1.play() 
                        if(selected_map[array_y][array_x] == 1):
                            selected_map[array_y][array_x] = 2
                            #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                        elif(selected_map[array_y][array_x] == 2):
                            selected_map[array_y][array_x] = 3      
                            #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                        elif(selected_map[array_y][array_x] == 3):
                            selected_map[array_y][array_x] = 1
                            #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                        
                    self.update_screen()           
                    # check flaged_cells   
                    flaged = 0
                    for row in selected_map:
                        for i in row:
                            if i == 2:
                                flaged += 1
                    global flaged_cells
                    flaged_cells = self.mine_count - flaged
                    #print(f"flaged_cells: {flaged_cells}")
                    flag_label.text = 'Flags: {}'.format(flaged_cells) 
                
            return True

        
        return super(SpriteGrid, self).on_touch_down(touch)

    
    
    def update_screen(self):
        sprite_counter = 0  # Assuming a flat structure for simplicity
       
        for y in range(num_rows):
            row = map[y]
            for x in range(num_cols):
                cell = row[x]
                if game_over:
                    if(selected_map[y][x] == 1):
                        if(cell == 9):
                            new_value = 2
                        else:
                            new_value = 5
                    elif(selected_map[y][x] == 2):
                        if(cell == 9):
                            new_value = 7
                        else:
                            new_value = 0
                    elif(selected_map[y][x] == 3):
                        if(cell == 9):
                            new_value = 2
                        else:
                            new_value = 5
                    elif(selected_map[y][x] == 4):
                        new_value = 6
                    elif(selected_map[y][x] == 0):
                        new_value = value_map[cell]
                else:
                    # Get the new value for the cell            
                    if(selected_map[y][x] == 1):
                        new_value = 5
                    elif(selected_map[y][x] == 2):
                        new_value = 7
                    elif(selected_map[y][x] == 3):
                        new_value = 1
                    elif(selected_map[y][x] == 4):
                        new_value = 6
                    elif(selected_map[y][x] == 0):
                        new_value = value_map[cell]   



                # Add new sprites
                self.sprites[sprite_counter].change_sprite(new_value)
                sprite_counter += 1

                #single_sprite = SingleSprite(sprite_sheet_path, new_value, pos=(x * sprite_size, y * sprite_size), size=(sprite_size, sprite_size))
                #self.add_widget(single_sprite)
        if game_over:
            if you_win:
                label = Label(
                    text='**** You Win! ****',
                    size_hint=(.3, .1),
                    pos_hint={'x':.35, 'y':.50},
                    font_name=font1_path,
                    font_size=Window.width * 0.07,
                    color=(0, 0.5, 1, 1),
                    text_size=self.size,
                    halign='center',
                    valign='middle',
                    outline_color=[0, 0, 0, 1],
                    outline_width=3
                    )
                grid_layout.add_widget(label)
                
            else:
                label = Label(
                    text='**** You Lose! ****',
                    size_hint=(.3, .1),
                    pos_hint={'x':.35,'y':.50},
                    font_name=font1_path,
                    font_size=Window.width * 0.07,
                    color=(1, 0.5, 0, 1),
                    text_size=self.size,
                    halign='center',
                    valign='middle',
                    outline_color=[0, 0, 0, 1],
                    outline_width=3
                    )
                grid_layout.add_widget(label)
                global sound2
                sound2.play()




def create_map(width, height, num_mines):
    # Initialize the map with zeros
    map = [[0 for _ in range(width)] for _ in range(height)]

    # Place the mines
    for _ in range(num_mines):
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if map[y][x] == 0:  # Make sure we don't place a mine on top of another mine
                map[y][x] = 9
                break

    # Calculate the numbers
    for y in range(height):
        for x in range(width):
            if map[y][x] == 9:
                continue  # Skip the mines
            # Check the 8 neighboring cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and map[ny][nx] == 9:
                        map[y][x] += 1
    return map


class App(App):
    def build(self):
       
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        # Remove window title
        Window.title = ''
        global sprite_size
        sprite_size = 25
        global num_rows
        num_rows = 20
        global num_cols
        num_cols = 30


        # Get the path to the images directory (assuming this file is in 'src')
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # sounds directory
        sounds_dir = os.path.join(current_dir, '..', 'sounds')
        
        sound1_path = os.path.join(sounds_dir, 'click-button-140881.mp3')
        global sound1
        sound1 = SoundLoader.load(sound1_path)
        sound1.volume = 1.0  # Maximum volume

        sound2_path = os.path.join(sounds_dir, 'low-impactwav-14905.mp3')
        global sound2
        sound2 = SoundLoader.load(sound2_path)
        sound2.volume = 1.0  # Maximum volume

        sound3_path = os.path.join(sounds_dir, 'punch-a-rock-161647.mp3')
        global sound3
        sound3 = SoundLoader.load(sound3_path)
        sound3.volume = 0.3  # Half volume

        sound4_path = os.path.join(sounds_dir, 'you-win-sequence-1-183948.mp3')
        global sound4
        sound4 = SoundLoader.load(sound4_path)
        sound4.volume = 1.0  # Half volume

        # images directory
        images_dir = os.path.join(current_dir, '..', 'images')
        global sprite_sheet_path
        sprite_sheet_path = os.path.join(images_dir, 'gaming_SpriteSheet.png')

        # font directory
        fonts_dir = os.path.join(current_dir, '..', 'fonts')
        global font1_path
        font1_path = os.path.join(fonts_dir, 'Ultra-Regular.ttf')

        global root, action_bar, flag_label
        root = BoxLayout(orientation='vertical')
        action_bar = ActionBar(pos_hint={'top':1}, size_hint_y=None, height=50)
        av = ActionView()
        av.add_widget(ActionPrevious(title='Minesweeper', with_previous=False))

        flag_label = ActionLabel(text='Flags: {}'.format(flaged_cells))
        av.add_widget(flag_label)
        av.add_widget(FastActionButton(text='Restart', on_press=self.option1))
        av.add_widget(FastActionButton(text='Level', on_press=self.option2))

        # create a dropdown
        global dropdown
        dropdown = DropDown()
        # list of elements to add to the dropdown
        elements = ['Easy', 'Medium', 'Hard', 'Expert']
        # add items to the dropdown
        for element in elements:
            btn = Button(text=element, size_hint_y=None, height=44)
            # bind the button to set the text and close the dropdown
            btn.bind(on_release=lambda btn: self.on_dropdown_select(btn, dropdown))
            # then add the button inside the dropdown
            dropdown.add_widget(btn)

        action_bar.add_widget(av)
        root.add_widget(action_bar)
        self.init_sprite_grid()
        
        return root 
    
    def init_sprite_grid(self):
        global root, grid_layout

        # Remove grid_layout from its current parent
        if grid_layout is not None and grid_layout.parent is not None:
            grid_layout.parent.remove_widget(grid_layout)
        grid_layout = FloatLayout(size=(sprite_size*num_cols, sprite_size*num_rows), size_hint_y=0.9)

        sprite_grid = SpriteGrid(pos=(0, 0), size=grid_layout.size)
        grid_layout.add_widget(sprite_grid)
        root.add_widget(grid_layout)

        # Set the size of the window to match the size of the sprite grid
        Window.size = (grid_layout.width, grid_layout.height + action_bar.height)
        Window.resizable = False
 

    def option1(self, instance):
        self.init_sprite_grid()
        print('Restart')

    def option2(self, instance):
        global dropdown
        instance.bind(on_release=dropdown.open)

    def on_dropdown_select(self, btn, dropdown):
        # update the main button text to the selected value and close the dropdown
        dropdown.select(btn.text)
        global num_rows
        global num_cols
        if btn.text == 'Easy':  
            num_rows = 9   
            num_cols = 16
            self.init_sprite_grid()
            print('Resize')
        elif btn.text == 'Medium':  
            num_rows = 16
            num_cols = 16
            self.init_sprite_grid()
            print('Resize')
        elif btn.text == 'Hard':
            num_rows = 20
            num_cols = 30
            self.init_sprite_grid()
            print('Resize')
        elif btn.text == 'Expert':
            num_rows = 33
            num_cols = 40
            self.init_sprite_grid()
            print('Resize')
        
       

if __name__ == '__main__':
    App().run()
