import random
import tkinter
import tkinter as tk


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.size = 20      # must be i*20
        self.y_limit = 200  # must be i*self.size, minimum is 200
        self.start_worm = 5
        self.max_x = 620    # if self.start_worm is odd/even then self.max_x/self.size must be odd/even,
        # min is 620 or 640
        self.max_y = 600    # if self.y_limit/self.size is odd/even then self.max_y/self.size must be odd/even,
        # minimum is self.y_limit+4*self.size
        self.canvas = None
        self.speed = 200
        self.buttons_dict = {}
        self.numbers_dict = {}
        self.announcements = {}
        self.max_amount = self.elements_amount()
        self.game_options = ('start', 'stop', 'reset')
        self.create_background(self.max_x, self.max_y)
        self.create_table()
        self.create_starting_elements()
        self.create_announcements()
        self.bind_buttons()

    def create_starting_elements(self):
        self.pressed_b1 = None
        self.pressed_key = None
        self.game_state = None
        self.apples = []
        self.hunters = []
        self.blocks = []
        self.eaten_apples = []
        self.static_positions = []
        self.current_amount = self.start_worm - 1
        self.worm = self.create_worm()
        self.moving_elements = [self.hunters, self.apples]
        self.apples.append(self.create_apple())
        self.bind_worm()
        self.all_elements = [self.worm, self.apples, self.hunters, self.blocks, self.eaten_apples]
        numbers = [len(self.worm.elements_list) - 1, len(self.apples), len(self.hunters), len(self.blocks), '0']
        for i, value in enumerate(self.numbers_dict.values()):
            self.change_text_value(value, numbers[i])

    def bind_buttons(self):
        self.canvas.bind_all('<KeyPress-Return>', self.press_key)
        self.canvas.bind_all('<KeyRelease-Return>', self.release_key)
        self.canvas.bind_all('<KeyPress-space>', self.press_key)
        self.canvas.bind_all('<KeyRelease-space>', self.release_key)
        self.canvas.bind_all('<KeyPress-r>', self.press_key)
        self.canvas.bind_all('<KeyRelease-r>', self.release_key)
        for key, value in self.buttons_dict.items():
            for element in value:
                self.canvas.tag_bind(element, '<ButtonPress-1>', self.button1_press)
                self.canvas.tag_bind(element, '<ButtonRelease-1>', self.button1_release)

    def bind_worm(self):
        self.canvas.bind_all('<KeyPress-Right>', self.worm.keypress_right)
        self.canvas.bind_all('<KeyPress-Left>', self.worm.keypress_left)
        self.canvas.bind_all('<KeyPress-Up>', self.worm.keypress_up)
        self.canvas.bind_all('<KeyPress-Down>', self.worm.keypress_down)
        self.canvas.bind_all('<KeyPress-d>', self.worm.keypress_right)
        self.canvas.bind_all('<KeyPress-a>', self.worm.keypress_left)
        self.canvas.bind_all('<KeyPress-w>', self.worm.keypress_up)
        self.canvas.bind_all('<KeyPress-s>', self.worm.keypress_down)

    def create_background(self, x, y):
        self.canvas = tk.Canvas(width=x, height=y)
        self.canvas.pack()
        nx = x // self.size
        ny = (y - self.y_limit) // self.size
        for i in range(nx):
            for j in range(ny):
                if i == 0 or j == 0 or i == nx - 1 or j == ny - 1:
                    color_01 = 'DarkKhaki'
                    color_02 = 'White'
                else:
                    color_01 = 'Silver'
                    color_02 = 'White'
                self.canvas.create_rectangle(i * self.size, (j * self.size) + self.y_limit, (i + 1) * self.size,
                                             ((j + 1) * self.size) + self.y_limit, fill=color_01, outline=color_02)

    def create_table(self):
        self.canvas.create_rectangle(5, 5, self.max_x, self.y_limit, fill='LightSteelBlue', outline='DarkOrchid',
                                     width=5)
        button_size_x, button_size_y = self.max_x / 5, self.y_limit // 3
        button_space_x, button_space_y = button_size_x / 5, button_size_y / 3
        # create start/stop/rest buttons
        start_frame = self.canvas.create_rectangle(button_size_x + 2 * button_space_x, button_space_y,
                                                   2 * button_size_x + 2 * button_space_x,
                                                   button_size_y + button_space_y,
                                                   fill='LightSkyBlue', outline='Navy', width=5)
        stop_frame = self.canvas.create_rectangle(2 * button_size_x + 3 * button_space_x, button_space_y,
                                                  3 * button_size_x + 3 * button_space_x,
                                                  button_size_y + button_space_y,
                                                  fill='LightSkyBlue', outline='Navy', width=5)
        reset_frame = self.canvas.create_rectangle(1.5 * button_size_x + 2.5 * button_space_x,
                                                   2 * button_space_y + button_size_y,
                                                   2.5 * button_size_x + 2.5 * button_space_x,
                                                   2 * button_space_y + 2 * button_size_y,
                                                   fill='LightSkyBlue', outline='Navy', width=5)
        text_style = 'PalatineLinotype'
        text_size = button_size_y // 5
        form = (text_style, text_size, 'bold')
        start = self.canvas.create_text(1.5 * button_size_x + 2 * button_space_x, 0.5 * button_size_y + button_space_y,
                                        text='{:^18}\n(press enter)'.format('Start'), font=form, fill='ForestGreen')
        stop = self.canvas.create_text(2.5 * button_size_x + 3 * button_space_x, 0.5 * button_size_y + button_space_y,
                                       text='{:^18}\n(press space)'.format('Stop'), font=form, fill='ForestGreen')
        reset = self.canvas.create_text(2 * button_size_x + 2.5 * button_space_x,
                                        2 * button_space_y + 1.5 * button_size_y,
                                        text='{:^13}\n(press "r")'.format('Reset'), font=form, fill='ForestGreen')
        self.buttons_dict['start'] = [start_frame, start]
        self.buttons_dict['stop'] = [stop_frame, stop]
        self.buttons_dict['reset'] = [reset_frame, reset]
        # create start options
        self.canvas.create_text((button_size_x / 2) + button_space_x, button_space_y / 1.1, text='Start options',
                                font=form,
                                fill='DeepPink')
        sing_size = self.y_limit // 5
        sign_form = ('PalatineLinotype', int(button_space_y // 2.1), 'bold')
        text_dict = {'Worm': ['Lime', 'LimeGreen', 0],
                     'Apples': ['Red', 'Crimson', 0],
                     'Hunters': ['SteelBlue', 'MidnightBlue', 0],
                     'Blocks': ['DarkKhaki', 'White', 0]}
        x_dist = [0.8 * button_space_x, 2 * button_space_x + 0.5*sing_size, 3*button_space_x+(2*sing_size/3)]
        for i, (key, value) in enumerate(text_dict.items()):
            middle_y = ((i + 1) * sing_size) + sing_size*0.4
            self.canvas.create_rectangle(x_dist[0], middle_y - sing_size/4, x_dist[0] + sing_size/2,
                                         middle_y + sing_size/4,
                                         fill=value[0], outline=value[1])
            self.canvas.create_text(x_dist[1], middle_y, text=key, font=sign_form, fill='Purple')
            self.canvas.create_rectangle(x_dist[2], middle_y - sing_size/4, x_dist[2]+sing_size/2,
                                         middle_y + sing_size/4,
                                         fill='Silver', outline='DimGrey', width=3)
            num = self.canvas.create_text(x_dist[2] + sing_size/4, middle_y, text=value[2], font=sign_form,
                                          fill='Black')
            upper_points = [x_dist[2]+0.8*sing_size, middle_y - sing_size/20, x_dist[2] + 1.4*sing_size,
                            middle_y - sing_size/20, x_dist[2] + 1.1*sing_size, middle_y - (sing_size / 2.3)]
            lower_points = [x_dist[2]+0.8*sing_size, middle_y + sing_size/20, x_dist[2] + 1.4*sing_size,
                            middle_y + sing_size/20, x_dist[2] + 1.1*sing_size, middle_y + (sing_size / 2.3)]
            upper = self.canvas.create_polygon(upper_points, fill='DarkRed', outline='Black', width=1.5)
            lower = self.canvas.create_polygon(lower_points, fill='DarkRed', outline='Black', width=1.5)
            self.canvas.create_text(upper_points[2] + sing_size/8, ((upper_points[1] + upper_points[5]) / 2),
                                    text='+',
                                    font=sign_form, fill='Red')
            self.canvas.create_text(lower_points[2] + sing_size/8, ((lower_points[1] + lower_points[5]) / 2),
                                    text='−',
                                    font=sign_form, fill='Red')
            self.buttons_dict['{} increase'.format(key)] = ([upper])
            self.buttons_dict['{} decrease'.format(key)] = ([lower])
            self.numbers_dict[key] = num
        # create score
        score_table = [self.max_x - ((button_size_x / 2) + button_space_x), self.y_limit / 1.8, sing_size * 0.8,
                       self.y_limit / 4]
        self.canvas.create_text(self.max_x - ((button_size_x / 2) + button_space_x), score_table[3], text='Score:',
                                font=(text_style, int(text_size * 1.7), 'bold'), fill='DeepPink')
        self.canvas.create_rectangle(score_table[0] + score_table[2], score_table[1] + score_table[2],
                                     score_table[0] - score_table[2], score_table[1] - score_table[2],
                                     width=3, fill='Gray', outline='LightCyan')
        score = self.canvas.create_text(score_table[0], score_table[1], text='0',
                                        font=(text_style, int(score_table[2] // 1.3), 'bold'), fill='WhiteSmoke')
        self.numbers_dict['score'] = score

    def create_announcements(self):
        x = int(self.canvas.cget('width')) - 90
        y = self.y_limit - 28
        style = ('PalatineLinotype', 20, 'bold')
        message = ('PLAY!', 'PAUSE', 'GAME OVER')
        color = ('DarkOliveGreen', 'Chocolate', 'IndianRed')
        for i, option in enumerate(self.game_options):
            self.announcements[option] = self.canvas.create_text(x, y, text=message[i], font=style, fill=color[i],
                                                                 state=tkinter.HIDDEN)

    def elements_amount(self):
        x_lines = (self.max_x - 2 * self.size) // self.size
        y_lines = (self.max_y - 2 * self.size - self.y_limit) // self.size
        return (x_lines * y_lines) - 1

    def create_worm(self):
        return Worm(self.canvas, self.size, self.start_worm, self.y_limit, self.static_positions)

    def create_apple(self):
        self.current_amount += 1
        return Apple(self.canvas, self.size, 1, self.y_limit, self.worm, self.moving_elements, self.static_positions)

    def create_hunter(self):
        self.current_amount += 1
        return Hunter(self.canvas, self.size, 1, self.y_limit, self.worm, self.moving_elements, self.static_positions)

    def create_block(self):
        temp = Block(self.canvas, self.size, 1, self.y_limit, self.worm, self.moving_elements, self.static_positions)
        self.add_static_position(temp)
        self.current_amount += 1
        return temp

    @staticmethod
    def determine_pressed_key(event):
        if event.keysym == 'Return':
            return 'start'
        elif event.keysym == 'space':
            return 'stop'
        elif event.keysym == 'r':
            return 'reset'
        else:
            return None

    def button1_press(self, event):
        if not self.pressed_key:
            xc, yc = event.x, event.y
            for key, value in self.buttons_dict.items():
                # start/stop/reset buttons
                if key in self.game_options:
                    x1, y1, x2, y2 = self.canvas.coords(value[0])
                    if x1 <= xc <= x2 and y1 <= yc <= y2:
                        self.pressed_b1 = key
                        self.change_items(key)
                # +/- buttons
                else:
                    x1, y1, x2, y2, x3, y3 = self.canvas.coords(value)
                    # + button
                    if x1 <= xc <= x2 and y1 >= yc >= y3:
                        self.pressed_b1 = key
                        self.change_items(self.pressed_b1)
                    # - button
                    elif x1 <= xc <= x2 and y1 <= yc <= y3:
                        self.pressed_b1 = key
                        self.change_items(self.pressed_b1)

    def button1_release(self, event):
        if not self.pressed_key:
            for key, value in self.buttons_dict.items():
                if self.pressed_b1 == key:
                    self.pressed_b1 = None
                    self.change_items(key)

    def press_key(self, event):
        key_word = self.determine_pressed_key(event)
        if not self.pressed_b1 and not self.pressed_key:
            self.pressed_key = key_word
            self.change_items(key_word)

    def release_key(self, event):
        key_word = self.determine_pressed_key(event)
        if not self.pressed_b1 and self.pressed_key == key_word:
            self.pressed_key = None
            self.change_items(key_word)

    def change_items(self, key_word):
        # start/stop/reset buttons
        if key_word in self.game_options:
            [frame, text] = self.buttons_dict[key_word]
            # press
            if key_word in (self.pressed_b1, self.pressed_key):
                color_01 = 'Cyan'
                color_02 = 'SteelBlue'
                text_color = 'LimeGreen'
                expand = 1
            # release
            else:
                color_01 = 'LightSkyBlue'
                color_02 = 'Navy'
                text_color = 'ForestGreen'
                expand = -1
                # when button is released change game state
                if not (self.pressed_b1 == 'stop' and not self.game_state):
                    self.change_game_state(key_word)
            self.change_size(frame, expand)
            self.change_color(frame, color_01, color_02)
            self.change_text_graphic(text, text_color, expand)
        # +/- buttons
        elif not self.pressed_key and not self.game_state and key_word not in self.game_options:
            [number_key, position] = key_word.split()
            frame = self.buttons_dict[key_word]
            add = 0
            # press
            if self.pressed_b1 == key_word:
                color = 'Red'
            # release
            else:
                color = 'DarkRed'
                # + button
                if position == 'increase':
                    add = 1
                # - button
                elif position == 'decrease':
                    add = -1
                # check if the play-board is full
                if (self.current_amount < self.max_amount and add == 1) or add == -1:
                    self.change_objects_amount(number_key, add)
            self.change_color(frame, color)

    def change_color(self, item, fill_color, outline_color=None):
        if outline_color is not None:
            self.canvas.itemconfig(item, fill=fill_color, outline=outline_color)
        else:
            self.canvas.itemconfig(item, fill=fill_color)

    def change_size(self, item, expand):
        x1, y1, x2, y2 = self.canvas.coords(item)
        value = expand * 5
        self.canvas.coords(item, x1 + value, y1 + value, x2 - value, y2 - value)

    def change_text_graphic(self, text, color, expand):
        font = self.canvas.itemcget(text, 'font')
        font = font.split()
        font[1] = str(int(font[1]) - expand * 2)
        font = ' '.join(font)
        self.canvas.itemconfig(text, font=font, fill=color)

    def change_text_value(self, text, num):
        self.canvas.itemconfig(text, text=num)

    def change_objects_amount(self, key_word, add):
        number_idx = self.numbers_dict[key_word]
        num = 0
        if key_word == 'Worm':
            self.current_amount -= (len(self.worm.elements_list) - 1)
            static_apples = []
            if not self.game_state:
                for apple in self.apples:
                    static_apples.append((apple.x, apple.y))
            self.worm.add_body(condition=add, start_static_elements=static_apples)
            num = len(self.worm.elements_list) - 1
            self.current_amount += num
        elif key_word == 'Apples':
            if add == 1:
                self.apples.append(self.create_apple())
            elif add == -1 and len(self.apples) > 0:
                apple = self.apples.pop(-1)
                self.canvas.delete(apple.id)
                self.current_amount -= 1
            num = len(self.apples)
        elif key_word == 'Hunters':
            if add == 1 and self.check_hunter():
                self.hunters.append(self.create_hunter())
            elif add == -1 and len(self.hunters) > 0:
                hunter = self.hunters.pop(-1)
                self.canvas.delete(hunter.id)
                self.current_amount -= 1
            num = len(self.hunters)
        elif key_word == 'Blocks':
            if add == 1:
                self.blocks.append(self.create_block())
            elif add == -1 and len(self.blocks) > 0:
                block = self.blocks.pop(-1)
                self.canvas.delete(block.id)
                self.static_positions.pop(-1)
                self.current_amount -= 1
            num = len(self.blocks)
        self.change_text_value(number_idx, num)

    def change_game_state(self, key_word):
        if key_word == 'start' and self.game_state in ('hold', None):
            self.game_state = 'play'
            self.change_visibility('stop', 'HIDE')
            self.change_visibility('reset', 'HIDE')
            self.change_visibility('start', 'SHOW')
            self.canvas.after(self.speed, self.change_visibility, 'start', 'HIDE')
            self.canvas.after(self.speed, self.timer)
        elif key_word == 'stop' and self.game_state == 'play':
            self.game_state = 'hold'
            self.change_visibility('stop', 'SHOW')
            self.change_visibility('reset', 'HIDE')
        elif key_word == 'reset':
            self.game_state = None
            self.change_visibility('stop', 'HIDE')
            self.change_visibility('reset', 'HIDE')
            self.reset_game()

    def change_visibility(self, key_word, cond):
        if cond == 'HIDE':
            self.canvas.itemconfig(self.announcements[key_word], state=tkinter.HIDDEN)
        elif cond == 'SHOW':
            self.canvas.itemconfig(self.announcements[key_word], state=tkinter.NORMAL)

    def check_hunter(self):
        return (((self.max_y - 2 * self.size - self.y_limit) // self.size)-1) > len(self.hunters)

    def add_static_position(self, element):
        self.static_positions.append((element.x, element.y))

    def game_over(self):
        self.change_visibility('reset', 'SHOW')
        self.game_state = 'game_over'

    def reset_game(self):
        for element in self.all_elements[1:]:
            for i in element:
                i.destroy()
        self.worm.delete_body()
        self.create_starting_elements()

    def timer(self):
        # check game state
        if not self.game_state:
            return
        elif self.game_state != 'hold':
            self.worm.tik()
            # hunter movement and check if worm is caught
            if not self.worm.crashed:
                for hunter in self.hunters:
                    hunter.tik(self.worm, self.moving_elements, self.static_positions)
                    # additional check if worm is caught (case by the wall), first check inside of hunter movement
                    if (hunter.x, hunter.y) == (self.worm.head_x, self.worm.head_y):
                        self.worm.caught = True
            # check if worm head is on apple
            for apple in self.apples:
                self.worm.eat_apple(apple)
                # check if apple is eaten
                if apple.eaten:
                    self.canvas.itemconfig(apple.id, fill='', outline='Maroon', width=3)
                    self.eaten_apples.append(apple)
                    self.apples.remove(apple)
                    num = int(self.canvas.itemcget(self.numbers_dict['score'], 'text')) + 1
                    self.change_text_value(self.numbers_dict['score'], str(num))
            # if there is no apple create one
            if len(self.apples) == 0:
                self.apples.append(self.create_apple())
            # check if eaten apple is at the end of worm
            if len(self.eaten_apples) > 0 and self.worm.check_eaten_apple(self.eaten_apples[0]):
                apple = self.eaten_apples.pop(0)
                self.worm.add_body(apple)
                apple.destroy()
        # final check
        if self.worm.crashed or self.worm.caught:
            self.game_over()
        elif self.game_state == 'hold':
            pass
        else:
            self.canvas.after(self.speed, self.timer)


class BoardObject:
    def __init__(self, canvas, body_size, create_size, y_limit, static_positions):
        self.canvas = canvas
        self.canvas_height = int(self.canvas.cget('height'))
        self.canvas_width = int(self.canvas.cget('width'))
        self.body_size = body_size
        self.create_size = create_size
        self.elements_list = []
        self.static_elements = static_positions
        self.x = None
        self.y = None
        self.id = None
        self.y_limit = y_limit
        self.destroyed = False

    def create_lists(self, worm, moving_elements):
        worm_list = []
        moving_elements_list = []
        for i in worm.elements_list:
            xw, yw, _, _ = self.canvas.coords(i)
            xw += self.body_size / 2
            yw += self.body_size / 2
            worm_list.append((xw, yw))
        for element in moving_elements:
            for i in element:
                moving_elements_list.append((i.x, i.y))
        return worm_list, moving_elements_list

    def create_element(self, worm, moving_elements, color_01, color_02, hunter=False):
        # each line can have only 1 hunter, middle line no hunter
        check_lines = []
        if hunter:
            check_lines.append(worm.head_y)
            for element in moving_elements[0]:
                check_lines.append(element.y)
        worm_list, moving_elements_list = self.create_lists(worm, moving_elements)
        x = 0
        y = 0
        # check if cell is empty
        all_checks = moving_elements_list + self.static_elements + worm_list
        while (x, y) in all_checks or (x, y) == (0, 0) or y in check_lines:
            x = random.randrange(self.body_size, self.canvas_width - self.body_size,
                                 self.body_size) + self.body_size / 2
            y = random.randrange((self.body_size + self.y_limit), self.canvas_height - self.body_size, self.body_size) \
                + self.body_size / 2
        self.x = x
        self.y = y
        self.id = self.canvas.create_rectangle(x - self.body_size / 2, y - self.body_size / 2, x + self.body_size / 2,
                                               y + self.body_size / 2, fill=color_01, outline=color_02)

    def check_position(self, x, y):
        max_x = self.canvas_width - self.body_size
        max_y = self.canvas_height - self.body_size
        return self.body_size < x < max_x and (self.body_size + self.y_limit) < y < max_y

    def destroy(self):
        self.destroyed = True
        self.canvas.delete(self.id)


class Worm(BoardObject):
    def __init__(self, canvas, body_size, create_size, y_limit, static_positions):
        super().__init__(canvas, body_size, create_size, y_limit, static_positions)
        self.dx = self.body_size
        self.dy = 0
        self.head_x = self.canvas_width / 2 + (self.create_size // 2) * self.body_size
        self.head_y = (self.canvas_height + y_limit) / 2 + self.body_size / 2
        self.orientation = 'Horizontal'
        # for example: cannot press right when last time you pressed right or left
        self.check_orientation = None
        self.crashed = False
        self.caught = False
        self.tail_x = 0
        self.tail_y = 0
        self.tail_dx = 0
        self.tail_dy = 0
        self.create()

    def create(self):
        x = self.head_x
        y = self.head_y
        for i in range(self.create_size):
            if i == 0:
                color_01 = 'Yellow'
                color_02 = 'Gold'
            else:
                color_01 = 'Lime'
                color_02 = 'LimeGreen'
            idx = self.canvas.create_rectangle(x - self.body_size / 2, y - self.body_size / 2, x + self.body_size / 2,
                                               y + self.body_size / 2, fill=color_01, outline=color_02)
            if i == self.create_size - 1:
                self.tail_x = x
                self.tail_y = y
            self.elements_list.append(idx)
            x -= self.body_size

    def tik(self):
        self.move_object()

    def move_object(self):
        worm_length = len(self.elements_list)
        xp, yp = 0, 0
        for i, element in enumerate(self.elements_list):
            x, y, _, _ = self.canvas.coords(element)
            if i == 0:
                self.check_orientation = self.orientation
                temp_x = x + self.dx + self.body_size / 2
                temp_y = y + self.dy + self.body_size / 2
                if self.crash(temp_x, temp_y):
                    break
                self.head_x = temp_x
                self.head_y = temp_y
                self.canvas.move(element, self.dx, self.dy)
                xp, yp = x, y
            else:
                if i == worm_length - 1:
                    self.tail_x = xp + self.body_size / 2
                    self.tail_y = yp + self.body_size / 2
                    self.tail_dx = xp - x
                    self.tail_dy = yp - y
                self.canvas.coords(element, xp, yp, xp + self.body_size, yp + self.body_size)
                xp, yp = x, y

    def crash(self, x, y):
        for element in self.elements_list:
            xc, yc, _, _ = self.canvas.coords(element)
            xc += self.body_size / 2
            yc += self.body_size / 2
            if (xc == x and yc == y) or not self.check_position(x, y) or (x, y) in self.static_elements:
                self.crashed = True
                return True

    def eat_apple(self, apple):
        if (self.head_x, self.head_y) == (apple.x, apple.y):
            apple.eaten = True

    def check_eaten_apple(self, apple):
        if (apple.x, apple.y) == (self.tail_x - self.tail_dx, self.tail_y - self.tail_dy):
            return True

    def add_body(self, apple=None, condition=None, start_static_elements=None):
        # add before game started
        if apple is None:
            if condition == 1:
                x1, y1, _, _ = self.canvas.coords(self.elements_list[-1])
                x2, y2, _, _ = self.canvas.coords(self.elements_list[-2])
                temp_x = self.tail_x + (x1 - x2)
                temp_y = self.tail_y + (y1 - y2)
                start_static_elements += self.static_elements
                if self.check_position(temp_x, temp_y) and (temp_x, temp_y) not in start_static_elements:
                    self.tail_x = temp_x
                    self.tail_y = temp_y
                    idx = self.canvas.create_rectangle(self.tail_x - self.body_size / 2,
                                                       self.tail_y - self.body_size / 2,
                                                       self.tail_x + self.body_size / 2,
                                                       self.tail_y + self.body_size / 2,
                                                       fill='Lime', outline='LimeGreen')
                    self.elements_list.append(idx)
            elif condition == -1 and len(self.elements_list) > 2:
                idx = self.elements_list.pop(-1)
                self.canvas.delete(idx)
                x1, y1, _, _ = self.canvas.coords(self.elements_list[-1])
                x2, y2, _, _ = self.canvas.coords(self.elements_list[-2])
                self.tail_x = self.tail_x - (x1 - x2)
                self.tail_y = self.tail_y - (y1 - y2)
        # during the game, when apple is at the end of worm
        else:
            x = apple.x
            y = apple.y
            idx = self.canvas.create_rectangle(x - self.body_size / 2, y - self.body_size / 2, x + self.body_size / 2,
                                               y + self.body_size / 2, fill='Lime', outline='LimeGreen')
            self.elements_list.append(idx)

    def delete_body(self):
        for element in self.elements_list:
            self.canvas.delete(element)

    def keypress_right(self, event):
        if self.orientation == 'Vertical' and self.check_pressing_keys():
            self.orientation = 'Horizontal'
            self.dx = self.body_size
            self.dy = 0

    def keypress_left(self, event):
        if self.orientation == 'Vertical' and self.check_pressing_keys():
            self.orientation = 'Horizontal'
            self.dx = -self.body_size
            self.dy = 0

    def keypress_up(self, event):
        if self.orientation == 'Horizontal' and self.check_pressing_keys():
            self.orientation = 'Vertical'
            self.dx = 0
            self.dy = -self.body_size

    def keypress_down(self, event):
        if self.orientation == 'Horizontal' and self.check_pressing_keys():
            self.orientation = 'Vertical'
            self.dx = 0
            self.dy = self.body_size

    def check_pressing_keys(self):
        return self.check_orientation == self.orientation


class Apple(BoardObject):
    def __init__(self, canvas, body_size, create_size, y_limit, worm, moving_elements, static_positions):
        super().__init__(canvas, body_size, create_size, y_limit, static_positions)
        self.eaten = False
        self.create_element(worm, moving_elements, 'Red', 'Crimson')


class Hunter(BoardObject):
    def __init__(self, canvas, body_size, create_size, y_limit, worm, moving_elements, static_positions):
        super().__init__(canvas, body_size, create_size, y_limit, static_positions)
        self.create_element(worm, moving_elements, 'SteelBlue', 'MidnightBlue', hunter=True)
        self.dx = self.body_size
        self.dy = 0

    def tik(self, worm, moving_elements, static_positions):
        self.move_object(worm, moving_elements, static_positions)

    def move_object(self, worm, moving_elements, static_positions):
        worm_list, check_lists = self.create_lists(worm, moving_elements)
        temp_x = self.x + self.dx
        temp_y = self.y + self.dy
        counter = 0
        move = True
        # if worm head is on hunter spot before hunter movement
        if (self.x, self.y) == (worm.head_x, worm.head_y) and self.dx == -worm.dx:
            move = False
            worm.caught = True
        # change hunter movement direction
        while (temp_x, temp_y) in static_positions or not self.check_position(temp_x, temp_y) or \
                (temp_x, temp_y) in check_lists or (temp_x, temp_y) in worm_list[1:]:
            self.dx = -self.dx
            self.dy = -self.dy
            temp_x = self.x + self.dx
            temp_y = self.y + self.dy
            counter += 1
            # if hunter is between two elements and cannot move
            if counter > 1:
                move = False
                break
        # if worm head is on hunter spot after hunter movement
       # if (temp_x, temp_y) == (worm.head_x, worm.head_y):
            #worm.caught = True
        if move:
            self.canvas.move(self.id, self.dx, self.dy)
            self.x += self.dx
            self.y += self.dy


class Block(BoardObject):
    def __init__(self, canvas, body_size, create_size, y_limit, worm, moving_elements, static_positions):
        super().__init__(canvas, body_size, create_size, y_limit, static_positions)
        self.create_element(worm, moving_elements, 'DarkKhaki', 'White')


game = Game()

game.mainloop()
