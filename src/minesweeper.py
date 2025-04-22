from kivy.app import App

from kivy.graphics.texture import TextureRegion
from kivy.graphics import Rectangle, Color
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
from kivy.clock import Clock



from kivy.graphics.shader import Shader
from kivy.graphics import RenderContext

import os
import random
import time
import colorsys

grid_layout = None
sprite_sheet_path = None
sprite_size = None  # Replace with your sprite size
num_rows, num_cols = None, None
map = None
selected_map = None
game_over = None
you_win = None
flag_end = True
flag_stop = True

hue = 0.0

sprite_sheet_path_array = []
sprite_sheet_number = 0

dropdown1 = None

remove_zeros = False

sound1, sound2, sound3, sound4 = None, None, None, None
font1_path = None
flag_label = None
time_label = None
elapsed_time = 0
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
        # Get the sprite from the sprite sheet
        sprite_size = self.sprite_sheet.width // 4  # Assuming a 4x4 grid
        i = self.sprite_index % 4
        j = self.sprite_index // 4
        region = TextureRegion(i * sprite_size, j * sprite_size, sprite_size, sprite_size, self.sprite_sheet)
        
        # Clear previous drawing
        self.canvas.clear()
        
        # Add rectangle to the canvas with the texture region
        with self.canvas:     
            Rectangle(texture=region, pos=self.pos, size=self.size)

    def change_sprite(self, new_index):
        self.sprite_index = new_index
        self.update_texture()

class SpriteGrid(Widget):
    def __init__(self, **kwargs):
        super(SpriteGrid, self).__init__(**kwargs)

        global current_hue
        if 'current_hue' not in globals():
            current_hue = 0.0  # Default hue



         # Add this line to track if game has started
        self.game_started = False
        self.timer_event = None

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

    # Add this method to update the timer
    def update_timer(self, dt):
        global elapsed_time, time_label
        elapsed_time += 0.1
        
        # Extract tenths of a second
        tenths = int((elapsed_time * 10) % 10)
        
        # Convert to hours, minutes, seconds
        total_seconds = int(elapsed_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Format the time string with tenths of a second
        if hours > 0:
            time_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths}'
        else:
            time_string = f'{minutes:02d}:{seconds:02d}.{tenths}'
        
        time_label.text = f'Time: {time_string}'

    def reset_timer(self):
        global time_label
        tim_st = '00:00.0'
        time_label.text = 'Time: {}'.format(tim_st)

    #solver code --------------------------

    def solver_calls(self):
        if dropdown1.attach_to:
            dropdown1.dismiss()
            Clock.schedule_once(lambda dt: self.continue_solver(), 0.1)
        else:
            self.continue_solver()


    def continue_solver(self):
        self.strip_zeros()
        actions_taken = [False] * 4  # Initialize a list to track actions taken

        # Attempt each solving strategy in sequence, updating the actions_taken list accordingly
        actions_taken[0] = self.add_flag()
        if not actions_taken[0]:  # Only proceed to the next strategy if the previous didn't take action
            actions_taken[1] = self.remove_equal_mine_number()
        if not actions_taken[1]:  # Similarly, proceed to the next only if this didn't take action
            actions_taken[2] = self.find_subset(1)
        if not actions_taken[2]:  # Proceed to the final strategy only if the previous didn't take action
            actions_taken[3] = self.find_subset(2)

        self.update_screen()

        # If any action was taken, call the solver again with updated flags
        #if any(actions_taken):
            #self.calls_solver(*actions_taken)

    def calls_solver(self, a, b, c, d):
        #if self.update_screen():
        #self.update_screen()
        #print("add_flag: " + str(a) + " remove_equal_mine_number: " + str(b) + " find_subset1: " + str(c) + " find_subset1: " + str(d))
        time.sleep(1.5)
        self.solver_calls()



    def strip_zeros(self): 
        global map
        global selected_map
        global remove_zeros
        if not remove_zeros:
            for i in range(len(map)):
                for j in range(len(map[0])):
                    if map[i][j] == 0 and selected_map[i][j] == 1:  # if the cell in map is 0 and the corresponding cell in selected_map is 1
                       # self.find_zero_cells(i, j)  # open all connected 0 cells  in selected_map
                        remove_zeros = True

    def add_flag(self):
        global map
        global selected_map
        global flaged_cells
       
        return_vale = False

        
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] != 0 and map[i][j] != 9 and selected_map[i][j] == 0:
                    if map[i][j] == len(self.neighbor(False, "not_open", i, j)):
                        if len(self.neighbor(False, "not_open", i, j)) != len(self.neighbor(False, "mine", i, j)):
                            return_vale = True
                            for (x, y) in self.neighbor(False, "not_open", i, j):
                                selected_map[x][y] = 2

        # Update the flag count
        flaged = sum(row.count(2) for row in selected_map)
        flaged_cells = self.mine_count - flaged
        flag_label.text = 'Flags: {}'.format(flaged_cells)
        
        self.check_all_falgs()
        
        
        return return_vale
    
    def check_all_falgs(self): 
        global game_over
        global you_win
        # Check if all mines are correctly flagged
        all_mines_flagged = True
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 9 and selected_map[i][j] != 2:
                    all_mines_flagged = False
                    break
            if not all_mines_flagged:
                break 
        # If all mines are correctly flagged and no incorrect flags exist
        if all_mines_flagged:
            # Count total flags to ensure no incorrect flags
            total_flags = sum(row.count(2) for row in selected_map)
            total_mines = sum(row.count(9) for row in map)
            
            if total_flags == total_mines:
                self.game_over_call("win")
                self.update_screen()
    

    
    def remove_equal_mine_number(self):
        global map
        global selected_map
        return_vale = False
        for i in range(len(map)):
            for j in range(len(map[0])):
                n, mn = self.neighbor(False, "not_open", i, j), self.neighbor(False, "mine", i, j)
                if map[i][j] == len(mn):
                    if map[i][j] < len(n):
                        return_vale = True
                        for (x, y) in self.merge_lists_remove_duplicates(n, mn):
                            selected_map[x][y] = 0
        return return_vale
    
    def find_subset(self, type):
        global map, selected_map
        work_done = False

        while True:
            list_list = [[] for _ in range(8)]
            for i in range(len(map)):
                for j in range(len(map[0])):
                    if selected_map[i][j] == 0:
                        remaining_mines = map[i][j] - len(self.neighbor(False, "mine", i, j))
                        if 0 <= remaining_mines <= 7:
                            cell_list = self.neighbor(False, "cell", i, j)
                            list_list[remaining_mines].append(cell_list)  # Store cell lists directly

            # Simplify list_list by removing empty entries
            list_list = [group for group in list_list if group]

            if not any(list_list):  # Exit loop if list_list is empty or only contains empty sublists
                break

            # Alternate between uncovering and processing logic based on whether work was done
            if not work_done:  # Only switch methods if no work was done in the previous iteration
                if type == 1:
                    if self.uncover_common_cells(list_list):
                        work_done = True
                        continue
                if type == 2:
                    if self.process_groups(list_list):
                        work_done = True
                        continue

            break  # Exit while True loop if no further actions can be taken
        return work_done
    
  
    def find_subset(self, type):
        global map, selected_map
        work_done = False

        while True:
            list_list = [[] for _ in range(8)]
            for i in range(len(map)):
                for j in range(len(map[0])):
                    if selected_map[i][j] == 0:
                        remaining_mines = map[i][j] - len(self.neighbor(False, "mine", i, j))
                        if 0 <= remaining_mines <= 7:
                            cell_list = self.neighbor(False, "cell", i, j)
                            list_list[remaining_mines].append(cell_list)  # Store cell lists directly

            # Simplify list_list by removing empty entries
            list_list = [group for group in list_list if group]

            if not any(list_list):  # Exit loop if list_list is empty or only contains empty sublists
                break

            # Alternate between uncovering and processing logic based on whether work was done
            if not work_done:  # Only switch methods if no work was done in the previous iteration
                if type == 1:
                    if self.uncover_common_cells(list_list):
                        work_done = True
                        continue
                if type == 2:
                    if self.process_groups(list_list):
                        work_done = True
                        continue

            break  # Exit while True loop if no further actions can be taken
        return work_done
    
    def neighbor(self, clear, type, row, col):
        neighbors = []
        if clear:
            selected_map[row][col] = 0  
        for i in range(max(0, row - 1), min(row + 2, len(map))):
            for j in range(max(0, col - 1), min(col + 2, len(map[0]))):
                if (i, j) != (row, col):
                    if type == "zero":
                        if clear:
                            selected_map[i][j] = 0
                        if map[i][j] == 0:
                            neighbors.append((i, j))
                    elif type == "mine":
                        if selected_map[i][j] == 2:
                            neighbors.append((i, j))
                    elif type == "not_open":
                        if selected_map[i][j] == 1 or selected_map[i][j] == 2 or selected_map[i][j] == 3:
                            neighbors.append((i, j))
                    elif type == "cell":
                        if selected_map[i][j] == 1:
                            neighbors.append((i, j))       
        return neighbors  
    
    def merge_lists_remove_duplicates(self, list1, list2):
        return list(set(list1) ^ set(list2))  # ^ operator performs symmetric difference operation

    def list_contains_other(self, list1, list2):
        return set(list1).issubset(set(list2)) or set(list2).issubset(set(list1))

    def process_groups(self, list_list):
        global selected_map
        work_done = False

        # Preprocess to combine all groups into a dictionary with the key being the mine count
        # and the value being a set of all cells for that mine count.
        combined_groups = {}
        for mine_count, groups in enumerate(list_list):
            if mine_count == 0:  # Skip groups corresponding to 0 mines
                continue
            for group in groups:
                if mine_count not in combined_groups:
                    combined_groups[mine_count] = set(group)
                else:
                    combined_groups[mine_count].update(group)

        # Iterate over each mine count and its cells
        for mine_count, cells in combined_groups.items():
            # Compare with each subsequent mine count
            for higher_mine_count in range(mine_count + 1, len(list_list)):
                if higher_mine_count not in combined_groups:
                    continue  # Skip if no groups for this mine count

                higher_cells = combined_groups[higher_mine_count]
                # Calculate symmetric difference between current and higher mine count cells
                diff_cells = cells.symmetric_difference(higher_cells)

                # If the number of unique cells equals the difference in mine counts,
                # it suggests these cells have a distinct status (e.g., to be flagged).
                if len(diff_cells) == higher_mine_count - mine_count:
                    # Flag each cell in the difference as a mine
                    for x, y in diff_cells:
                        if selected_map[x][y] not in [0, 2]:  # Skip already uncovered or flagged cells
                            selected_map[x][y] = 2
                            work_done = True

        return work_done
    
    def uncover_common_cells(self, list_list):
        global selected_map
        work_done = False
        for sub_list in list_list:
            for i, el1 in enumerate(sub_list):
                for j, el2 in enumerate(sub_list) :
                    if i != j:
                        contains = self.list_contains_other(el1, el2)   
                        if contains:
                            duplicates = self.merge_lists_remove_duplicates(el1, el2)
                            if len(duplicates) > 0:
                                work_done = True
                                for el3 in duplicates:
                                    selected_map[el3[0]][el3[1]] = 0
        return work_done
    #--------------------------------------

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
            #print("on_touch_down") 

            array_x = int(touch.x // sprite_size)
            array_y = int(touch.y // sprite_size)

            # Add bounds checking to prevent index errors
            if array_x >= num_cols or array_y >= num_rows or array_x < 0 or array_y < 0:
                #print(f"Click outside valid grid area: {array_x}, {array_y}")
                return True

            global game_over
            if game_over != True:
                #print(f"selected_map: {selected_map[array_y][array_x]}")  
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
                            self.game_over_call("lose")
                            #print("Game Over")
                        elif map[array_y][array_x] == 0:
                            self.start_clock()
                            selected_map[array_y][array_x] = 0
                            self.find_zero_cells(array_y, array_x)
                            self.update_screen()
                            sound3.play()   
                            #print("Find zeros")
                        else:
                            self.start_clock()
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
                        self.game_over_call("win")
                        
                    #print(f"not_mine_count: {self.not_mine_count} count: {count}")

                elif touch.button == 'right':           
                    if(selected_map[array_y][array_x] != 0):
                        if sound1.state != 'play':
                            sound1.play()
                        else:
                            sound1.stop()
                            sound1.play()
                        if flag_stop:
                            if sum(row.count(2) for row in selected_map) < self.mine_count:
                                if(selected_map[array_y][array_x] == 1):
                                    selected_map[array_y][array_x] = 2
                                elif(selected_map[array_y][array_x] == 2):
                                    selected_map[array_y][array_x] = 3      
                                elif(selected_map[array_y][array_x] == 3):
                                    selected_map[array_y][array_x] = 1
                            else:      
                                if(selected_map[array_y][array_x] == 1):
                                    selected_map[array_y][array_x] = 3
                                elif(selected_map[array_y][array_x] == 2):
                                    selected_map[array_y][array_x] = 3      
                                elif(selected_map[array_y][array_x] == 3):
                                    selected_map[array_y][array_x] = 1
                        else:
                            if(selected_map[array_y][array_x] == 1):
                                selected_map[array_y][array_x] = 2
                                #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                            elif(selected_map[array_y][array_x] == 2):
                                selected_map[array_y][array_x] = 3      
                                #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                            elif(selected_map[array_y][array_x] == 3):
                                selected_map[array_y][array_x] = 1
                                #print(f"Touch down on sprite at array position {array_x}, {array_y}")
                    self.check_all_falgs()   
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
    
    def start_clock(self):
        if not self.game_started:
            self.game_started = True
            global elapsed_time
            elapsed_time = 0
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
    
    def game_over_call(self, type):
        global game_over
        global you_win
        global elapsed_time
        if type == "win":
            game_over = True
            you_win = True     
        elif type == "lose":   
            game_over = True
            you_win = False     
            elapsed_time = 0
            global time_label
            self.reset_timer()

        # Stop the timer when game ends
        if self.timer_event:
            #print("Stopping timer")
            Clock.unschedule(self.timer_event)       
            self.game_started = False
            self.timer_event = None
            

        self.update_screen()

    
    
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
                global sound4
                sound4.play()   
                
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
        return True




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
        #print("Sound1 path:", sound1_path)
        global sound1
        sound1 = SoundLoader.load(sound1_path)
        sound1.volume = 1.0  # Maximum volume

        sound2_path = os.path.join(sounds_dir, 'low-impactwav-14905.mp3')
        global sound2
        sound2 = SoundLoader.load(sound2_path)
        sound2.volume = 0.3  # Maximum volume

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
        global sprite_sheet_path_array, sprite_sheet_number

        sprite_sheet_number = 0
        sprite_sheet_path_array.append(os.path.join(images_dir, 'gaming_SpriteSheet.png'))
        sprite_sheet_path_array.append(os.path.join(images_dir, 'heart1.png'))
        sprite_sheet_path_array.append(os.path.join(images_dir, 'green2.png'))
        sprite_sheet_path_array.append(os.path.join(images_dir, 'shark1.png'))

        # Add this line to initialize sprite_sheet_path
        global sprite_sheet_path
        sprite_sheet_path = sprite_sheet_path_array[sprite_sheet_number]
        
        #sprite_sheet_path1 = os.path.join(images_dir, 'gaming_SpriteSheet.png')
        #sprite_sheet_path2 = os.path.join(images_dir, 'heart1.png')
        #sprite_sheet_path3 = os.path.join(images_dir, 'green2.png')

        # font directory
        fonts_dir = os.path.join(current_dir, '..', 'fonts')
        global font1_path
        font1_path = os.path.join(fonts_dir, 'Ultra-Regular.ttf')

        global root, action_bar, flag_label, time_label 
        root = BoxLayout(orientation='vertical')
        action_bar = ActionBar(pos_hint={'top':1}, size_hint_y=None, height=50)
        av = ActionView()
        av.add_widget(ActionPrevious(title='Minesweeper', with_previous=False))

        time_label = ActionLabel(text='Time: {}'.format(elapsed_time))
        av.add_widget(time_label)
        flag_label = ActionLabel(text='Flags: {}'.format(flaged_cells))
        av.add_widget(flag_label)
        av.add_widget(FastActionButton(text='Restart', on_press=self.option1))
        av.add_widget(FastActionButton(text='Level', on_press=self.option2))

        # create a dropdown
        global dropdown1
        dropdown1 = DropDown()
        # list of elements to add to the dropdown
        elements = ['Easy', 'Medium', 'Hard', 'Expert', "Solve", "Theme"]
        # add items to the dropdown
        for element in elements:
            btn = Button(text=element, size_hint_y=None, height=44)
            # bind the button to set the text and close the dropdown
            btn.bind(on_release=lambda btn: self.on_dropdown_select(btn, dropdown1))
            # then add the button inside the dropdown
            dropdown1.add_widget(btn)

        action_bar.add_widget(av)
        root.add_widget(action_bar)
        self.init_sprite_grid()
        
        return root 
    
    def on_start(self):
        # Remove window title
        Window.title = ''
    
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

        
        global time_label
        time_st = '00:00.0'
        time_label.text = 'Time: {}'.format(time_st)
 
    def change_theme(self):
        global sprite_sheet_path_array, sprite_sheet_number, sprite_sheet_path, grid_layout, sound1
        
        # Update theme number
        if sprite_sheet_number >= len(sprite_sheet_path_array) - 1:
            sprite_sheet_number = 0
        else:
            sprite_sheet_number += 1
        
        # Update global path variable
        sprite_sheet_path = sprite_sheet_path_array[sprite_sheet_number]     
        print(f"Changed theme to #{sprite_sheet_number+1}")
        
        # Find the SpriteGrid in the children
        sprite_grid = None
        if grid_layout and grid_layout.children:
            for child in grid_layout.children:
                if isinstance(child, SpriteGrid):
                    sprite_grid = child
                    break
        
        # Only update sprites if we found a valid SpriteGrid
        if sprite_grid:
            for sprite in sprite_grid.sprites:
                # Load the new texture and update each sprite
                sprite.sprite_sheet = CoreImage(sprite_sheet_path).texture
                sprite.update_texture()

    def option1(self, instance):
        self.init_sprite_grid()
        #print('Restart')

    def option2(self, instance):
        global dropdown1
        instance.bind(on_release=dropdown1.open)

    def on_dropdown_select(self, btn, dropdown1):
        # update the main button text to the selected value and close the dropdown
        dropdown1.select(btn.text)
        global num_rows
        global num_cols
        if btn.text == 'Easy':  
            num_rows = 9   
            num_cols = 16
            self.init_sprite_grid()
            #print('Resize')
        elif btn.text == 'Medium':  
            num_rows = 16
            num_cols = 16
            self.init_sprite_grid()
            #print('Resize')
        elif btn.text == 'Hard':
            num_rows = 20
            num_cols = 30
            self.init_sprite_grid()
            #print('Resize')
        elif btn.text == 'Expert':
            num_rows = 33
            num_cols = 40
            self.init_sprite_grid()
            #print('Resize')
        elif btn.text == 'Solve':
            grid_layout.children[0].solver_calls()
        elif btn.text == 'Theme':
            # Implement theme change logic here
            # For example, you could change the background color or sprite sheet
            self.change_theme()


        # Close the dropdown after processing
        dropdown1.dismiss()
        
       

if __name__ == '__main__':
    App().run()
