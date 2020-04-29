
from functools import partial
from random import choice, randint
from ShipsException import *
from Interface import *


class MyButton(Button):

    def __init__(self, identity, player_identity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ID = identity
        self.state = 0
        self.player_ID = player_identity
        self.configure(height=2, width=5)
        self.configure(command=partial(button_press_handler, self.ID, self.player_ID))
        self.configure(bg="grey")


class MyGameBoard:

    def __init__(self, MyWindow):

        self.rows = []
        self.columns = []
        self.buttons_tab_players = [[], []]
        self.myFrames = [MyFrame(MyWindow) for i in range(2)]

        self.start_button = Button(MyWindow, text="START", command=start, relief="raised",
                                   font="Times 20", bd=10, bg="red").place(x=1050, y=200)
        self.reset_button = Button(MyWindow, text="RESET", command=reset, relief="raised",
                                   font="Times 20", bd=10, bg="red").place(x=1050, y=300)

    def create_buttons_table(self, player_ID):

        self.buttons_tab_players[player_ID] = [MyButton(i, player_ID, self.myFrames[player_ID]) for i in range(100)]

    def set_buttons_table(self, player_ID):

        j = 0
        for a in range(10):
            for b in range(10):
                self.buttons_tab_players[player_ID][j].grid(column=a, row=b)
                j = j + 1

    def set_rows_and_columns(self):

        self.columns = [[10 * i + x for x in range(10)] for i in range(10)]
        self.rows = [[10 * x + i for x in range(0, 10)] for i in range(10)]

    def initliazation(self):

        self.create_buttons_table(0)
        self.create_buttons_table(1)
        self.set_buttons_table(0)
        self.set_buttons_table(1)
        self.set_rows_and_columns()
        self.myFrames[0].grid(column=0, row=0, padx=20, pady=80)
        self.myFrames[1].grid(column=1, row=0, padx=20)

    def reset(self, start=False):

        if start == False:

            for i in range(100):
                self.buttons_tab_players[0][i].configure(bg='grey')
                self.buttons_tab_players[1][i].configure(bg='grey')
                self.buttons_tab_players[0][i].state = 0
                self.buttons_tab_players[1][i].state = 0

        else:

            for i in range(100):
                self.buttons_tab_players[1][i].state = 0
                self.buttons_tab_players[1][i].configure(bg='grey')

                if self.buttons_tab_players[0][i].state == 2:
                    self.buttons_tab_players[0][i].configure(bg='grey')
                    self.buttons_tab_players[0][i].state = 0

                if self.buttons_tab_players[0][i].state == 3:
                    self.buttons_tab_players[0][i].configure(bg='green')
                    self.buttons_tab_players[0][i].state = 1


class Ships:

    def __init__(self):

        self.ship_tmp_length = [0 for i in range(4)]
        self.ships_number_tmp = [0 for i in range(4)]

        self.ship_flags = [0 for i in range(4)]
        self.ship_board_access = [0 for i in range(2)]

        self.ship_length = (1, 2, 3, 4)
        self.ships_number = (4, 3, 2, 1)

        self.last_pressed_buttons_ID = []

        self.ships = [[[], [], [], []], [[], [], [], []]]

        self.stage = 0
        self.counter = 0
        self.start_pressed = False

    def find_neighbours(self, button_ID, GameBoard):

        neighbours = []

        for x in [10, 1, 11, 9]:

            if x == 10:
                neighbours.append(button_ID - x)
                neighbours.append(button_ID + x)

            if button_ID - x not in GameBoard.rows[9] and x == 1 and x != 10:
                neighbours.append(button_ID - x)

            if button_ID - x not in GameBoard.rows[9] and x == 11 and x != 10:
                neighbours.append(button_ID - x)

            if button_ID + x not in GameBoard.rows[0] and x == 11 and x != 10:
                neighbours.append(button_ID + x)

            if button_ID + x not in GameBoard.rows[0] and x == 1 and x != 10:
                neighbours.append(button_ID + x)

            if button_ID - x not in GameBoard.rows[0] and x == 9 and x != 10:
                neighbours.append(button_ID - x)

            if button_ID + x not in GameBoard.rows[9] and x == 9 and x != 10:
                neighbours.append(button_ID + x)

        remove = [a for a in neighbours if a < 0 or a >= 100]

        for i in remove:
            neighbours.remove(i)

        return neighbours

    def check_neighbour(self, button_ID, GameBoard):

        neighbours = self.find_neighbours(button_ID, GameBoard)

        for neighbour in neighbours:

            if neighbour in self.last_pressed_buttons_ID:
                return 1
        else:
            return 0

    def check_environment(self, GameBoard, button_ID, player_ID):

        environment = self.find_neighbours(button_ID, GameBoard)

        for y in self.last_pressed_buttons_ID:
            if y in environment:
                environment.remove(y)

        for env in environment:
            if GameBoard.buttons_tab_players[player_ID][env].state != 0:
                return 0
        else:
            return 1

    def place_ship(self, GameBoard, button_ID, player_ID):

        if button_ID == -1:
            return 1

        board_access = self.ship_board_access[player_ID]
        flags = self.ship_flags
        tmp_len = self.ship_tmp_length
        check_env = self.check_environment(GameBoard, button_ID, player_ID)
        button_state = GameBoard.buttons_tab_players[player_ID][button_ID].state
        check_neighbour = self.check_neighbour(button_ID, GameBoard)

        if board_access == 1:

            if button_state == 0:

                for flag in flags:
                    if flag == 1:

                        index = self.ship_flags.index(flag)

                        if tmp_len[index] == 0:

                            if check_env:
                                GameBoard.buttons_tab_players[player_ID][button_ID].configure(bg="green")
                                GameBoard.buttons_tab_players[player_ID][button_ID].state = 1
                                self.ship_tmp_length[index] += 1
                                self.last_pressed_buttons_ID.append(button_ID)
                                self.ships[player_ID][index].append(button_ID)
                            else:
                                return -1

                        elif tmp_len[index] < self.ship_length[index]:

                            if check_env:

                                if check_neighbour and button_state == 0:
                                    GameBoard.buttons_tab_players[player_ID][button_ID].configure(bg="green")
                                    GameBoard.buttons_tab_players[player_ID][button_ID].state = 1
                                    self.ship_tmp_length[index] += 1
                                    self.last_pressed_buttons_ID.append(button_ID)
                                    self.ships[player_ID][index].append(button_ID)
                                else:
                                    return -4

                            else:
                                return -1

                        if tmp_len[index] == self.ship_length[index]:
                            self.ship_flags[index] = 0
                            self.ship_tmp_length[index] = 0
                            self.last_pressed_buttons_ID.clear()
                            return 1
                else:
                    return 0

            else:
                return -2

        else:
            return -3

    def split_ships(self, player_ID):

        split = lambda A, n: [A[i:i + n] for i in range(0, len(A), n)]

        i = 1
        for ship in self.ships[player_ID]:
            self.ships[player_ID][self.ships[player_ID].index(ship)] = split(ship, i)
            i += 1

    def shoot_down_ship(self, button_ID, player_ID, gameboard, Graphics, AI=False):

        button_state = gameboard.buttons_tab_players[player_ID][button_ID].state
        board_acces = self.ship_board_access[player_ID]

        if board_acces == 1:

            if (button_state == 0 or button_state == 1):

                flatten_list = [item for s_type in self.ships[player_ID] for ship in s_type for item in ship]
                ships_list = [item for s_type in self.ships[player_ID] for item in s_type]

                if button_ID in flatten_list:



                    if AI == False:
                        gameboard.buttons_tab_players[player_ID][button_ID].configure(bg='red')


                    else:
                        myWindow.after(1000 + self.counter * 1000,
                                       lambda: gameboard.buttons_tab_players[player_ID][button_ID].configure(bg='red'))
                        myWindow.after(1000 + self.counter * 1000,
                                       lambda: myGraphics.message_text.set("Przeciwnik trafia!"))
                        self.counter += 1

                    gameboard.buttons_tab_players[player_ID][button_ID].state = 3

                    for element in ships_list:
                        if button_ID in element:
                            for ID in element:
                                if gameboard.buttons_tab_players[player_ID][ID].state == 1:
                                    return 1
                            else:

                                for ID in element:
                                    neighbours = self.find_neighbours(ID, gameboard)

                                    for env in neighbours:
                                        if gameboard.buttons_tab_players[player_ID][env].state == 3:
                                            continue
                                        else:
                                            gameboard.buttons_tab_players[player_ID][env].configure(bg='blue')
                                            gameboard.buttons_tab_players[player_ID][env].state = 2
                                else:
                                    return 2

                elif gameboard.buttons_tab_players[player_ID][button_ID].state != 3:



                    if AI == False:
                        gameboard.buttons_tab_players[player_ID][button_ID].configure(bg='blue')

                    if AI == True:
                        myWindow.after(1000 + self.counter * 1000,
                                       lambda: gameboard.buttons_tab_players[player_ID][button_ID].configure(bg='blue'))
                        myWindow.after(1000 + self.counter * 1000,
                                       lambda: myGraphics.message_text.set("Przeciwnik pudłuje! \n Twoja kolej!"))
                        self.counter = 0

                    gameboard.buttons_tab_players[player_ID][button_ID].state = 2
                    return 0
            else:
                return -1

        else:
            return -2

    def game_place_ships_player(self, player_ID, button_ID, Graphics, GameBoard):

        place_ship = self.place_ship(GameBoard, button_ID, player_ID)

        self.ship_board_access[0] = 1

        if place_ship == 1:

            for i in range(len(self.ship_length)):

                if self.ships_number_tmp[0] < self.ships_number[0]:
                    Graphics.message_text.set("Ustaw " + Graphics.ship_prefix[0] + "masztowce!")
                    self.ship_flags[0] = 1
                    self.ships_number_tmp[0] += 1
                    break

                if self.ships_number_tmp[i] < self.ships_number[i] and self.ships_number_tmp[i - 1] == \
                        self.ships_number[
                            i - 1]:
                    if Graphics.ship_prefix[i] == 'cztero':
                        Graphics.message_text.set("Ustaw " + Graphics.ship_prefix[i] + "masztowiec!")
                        Graphics.previous_text = Graphics.message_text.get()
                    else:
                        Graphics.message_text.set("Ustaw " + Graphics.ship_prefix[i] + "masztowce!")
                        Graphics.previous_text = Graphics.message_text.get()

                    self.ship_flags[i] = 1
                    self.ships_number_tmp[i] += 1
                    break

                if self.ships_number_tmp[3] == self.ships_number[3]:
                    self.ship_board_access[player_ID] = 0
                    self.ship_tmp_length = [0, 0, 0, 0]
                    self.ship_flags = [0, 0, 0, 0]
                    self.ship_board_access[player_ID] = 0
                    self.ships_number_tmp = [0, 0, 0, 0]
                    Graphics.message_text.set("Okręty rozstawione. Naciśnij START")
                    return 1

        if place_ship == 0:
            Graphics.message_text.set(Graphics.previous_text)

        try:

            if place_ship == -1:
                raise ShipsTouching

            if place_ship == -2:
                raise PlacingAlreadyPlaced

            if place_ship == -3:
                raise PlacingOnOponentBoard

            if place_ship == -4:
                raise PlacingElementNotConnectedWithShip



        except ShipsTouching:
            Graphics.message_text.set('Statek styka się z innym! \n Spróbuj jeszcze raz! \n')
            raise

        except PlacingAlreadyPlaced:
            Graphics.message_text.set('Pole już zajęte! \n Spróbuj jeszcze raz! \n')
            raise

        except PlacingOnOponentBoard:
            Graphics.message_text.set('To nie twoja plansza! \n Spróbuj jeszcze raz! \n')
            raise

        except PlacingElementNotConnectedWithShip:
            Graphics.message_text.set('Pole nie styka się ze swoim okrętem! \n Spróbuj jeszcze raz! \n')
            raise

    def game_shoot_down_ships_player(self, Graphics, GameBoard, button_ID, player_ID, AI=True):

        if button_ID == -1:
            first_turn = randint(0, 1)
            self.ship_board_access[first_turn] = 1

        if self.ship_board_access[1] == 1:

            Graphics.message_text.set('Strzel do przeciwnika!')
            if button_ID == -1:
                return 0

            shoot = self.shoot_down_ship(button_ID, player_ID, GameBoard, Graphics)

            if shoot == 0:
                Graphics.message_text.set('Pudło!')
                self.ship_board_access[1] = 0
                self.ship_board_access[0] = 1

            if shoot == 1:
                Graphics.message_text.set('Przeciwnik trafiony! \n Strzelaj dalej!')

            if shoot == 2:
                Graphics.message_text.set('Przeciwnik trafiony,zatopiony!\n Strzelaj dalej!')

            try:

                if shoot == -1:
                    raise ShootingInAlreadyShooted

                if shoot == -2:
                    raise ShootingOwnBoard

            except ShootingInAlreadyShooted:
                myGraphics.message_text.set('Już tu strzelałeś!! \n Strzel jeszcze raz!')
                raise

            except ShootingOwnBoard:
                myGraphics.message_text.set('Nie ta plansza! \n Strzel jeszcze raz!')
                raise

        if self.ship_board_access[0] == 1 and AI == True:
            self.shoot_down_ship_AI(myGameBoard, Graphics)

        self.end_game(Graphics, GameBoard)

    def end_game(self, Graphics, gameboard):

        for player in gameboard.buttons_tab_players:

            if self.ship_board_access[0] == 1 or self.ship_board_access[1] == 1:

                for button in player:
                    if button.state == 1:
                        break
                else:
                    if gameboard.buttons_tab_players.index(player) == 0:

                        myWindow.after(3000,
                                       lambda: myGraphics.message_text.set("Wygrał gracz 1 \nNaciśnij start lub reset"))

                    if gameboard.buttons_tab_players.index(player) == 1:

                        Graphics.message_text.set(
                            'Wygrał gracz 0 \nNaciśnij start lub reset')



                    self.ship_board_access[0] = 0
                    self.ship_board_access[1] = 0
                    return 1






    def shoot_down_ship_AI(self, myGameBoard, myGraphics):

        if self.ship_board_access[0] == 1:

            while True:

                remaining = [x.ID for x in myGameBoard.buttons_tab_players[0] if x.state != 3 and x.state != 2]

                if not self.last_pressed_buttons_ID:
                    button = choice(remaining)

                if self.last_pressed_buttons_ID:

                    for i in range(1, 8):

                        flag = 0
                        neighbour = self.find_neighbours(self.last_pressed_buttons_ID[-i], myGameBoard)

                        for x in neighbour:
                            if myGameBoard.buttons_tab_players[0][x].state not in [2, 3]:
                                button = x
                                flag = 1

                        if flag == 1:
                            break

                shot = self.shoot_down_ship(button, 0, myGameBoard, myGraphics, AI=True)

                if shot == 0:
                    break

                if shot == 1:
                    self.last_pressed_buttons_ID.append(button)

                if shot == 2:
                    self.last_pressed_buttons_ID.clear()

                if self.end_game(myGraphics,myGameBoard):
                    return 0


            self.ship_board_access[0] = 0
            self.ship_board_access[1] = 1

    def game_place_ships_AI(self, gameboard, AI=False):

        stop = 0

        self.ship_board_access[1] = 1

        tmp_len = self.ship_tmp_length
        check_env = self.check_environment
        board = gameboard.buttons_tab_players[1]
        find_neighbours = self.find_neighbours

        free_ships = [i for i in range(100)]

        j = 3

        numbers = reversed(self.ships_number)

        for number in numbers:
            i = 0
            while i < number:
                self.ship_flags[j] = 1
                if tmp_len[j] == 0:
                    while True:

                        button = choice(free_ships)
                        if board[button].state == 0 and check_env(gameboard, button, 1):
                            gameboard.buttons_tab_players[1][button].state = 1
                            self.ship_tmp_length[j] += 1
                            self.last_pressed_buttons_ID.append(button)
                            self.ships[1][j].append(button)
                            if AI == True:
                                gameboard.buttons_tab_players[1][button].configure(bg="green")
                            free_ships.remove(button)
                            break

                elif tmp_len[j] < self.ship_length[j]:

                    neighbours = find_neighbours(button, gameboard)
                    tmp = 0

                    while True:

                        stop += 1

                        if stop > 1000:
                            return -1

                        if neighbours:
                            neighbour = choice(neighbours)
                        if board[neighbour].state == 0 and check_env(gameboard, neighbour, 1):
                            button = neighbour
                            gameboard.buttons_tab_players[1][button].state = 1
                            self.ship_tmp_length[j] += 1
                            self.last_pressed_buttons_ID.append(button)
                            self.ships[1][j].append(button)
                            if AI == True:
                                gameboard.buttons_tab_players[1][button].configure(bg="green")
                            free_ships.remove(button)
                            break

                        if neighbour in neighbours:
                            neighbours.remove(neighbour)
                        tmp += 1

                        if tmp == len(neighbours):

                            if len(self.last_pressed_buttons_ID) >= 2:
                                neighbours = find_neighbours(self.last_pressed_buttons_ID[-2], gameboard)
                            else:
                                neighbours = find_neighbours(self.last_pressed_buttons_ID[0], gameboard)

                            tmp = 0

                if tmp_len[j] == self.ship_length[j]:
                    self.ship_flags[j] = 0
                    self.ship_tmp_length[j] = 0
                    self.last_pressed_buttons_ID.clear()
                    i += 1
            j -= 1

        self.ship_board_access[1] = 0

    def main_game_one_player(self, Graphics, GameBoard, button_ID, player_ID):

        if self.stage == 0:
            if self.game_place_ships_player(player_ID, button_ID, Graphics, GameBoard):
                self.split_ships(0)
                self.stage += 1
                return 0

        if self.stage == 1 and button_ID == -1:
            self.game_place_ships_AI(myGameBoard, AI=False)
            self.split_ships(1)
            self.stage += 1

        if self.stage == 2:
            self.game_shoot_down_ships_player(Graphics, GameBoard, button_ID, player_ID)

    def reset(self, start=False):

        if start == False:
            self.ship_tmp_length = [0, 0, 0, 0]
            self.ship_flags = [0, 0, 0, 0]
            self.ship_board_access = [0, 0]
            self.last_pressed_buttons_ID.clear()
            self.ships_number_tmp = [0, 0, 0, 0]
            self.ships = [[[], [], [], []], [[], [], [], []]]
            self.ships_players = [[[], [], [], []], [[], [], [], []]]
            self.mode = 1
            self.stage = 0
            self.start_pressed = False

        if start == True:
            self.ship_tmp_length = [0, 0, 0, 0]
            self.ship_flags = [0, 0, 0, 0]
            self.ship_board_access = [0, 0]
            self.last_pressed_buttons_ID.clear()
            self.ships_number_tmp = [0, 0, 0, 0]
            self.ships[1] = [[], [], [], []]
            self.stage = 1
            self.start_pressed = True


def button_press_handler(button_ID, player_ID):
    myShips.main_game_one_player(myGraphics, myGameBoard, button_ID, player_ID)


def start():
    if myShips.start_pressed == False:

        myShips.start_pressed = True
        myShips.main_game_one_player(myGraphics, myGameBoard, -1, 0)

    else:
        myShips.reset(start=True)
        myGameBoard.reset(start=True)
        myGraphics.reset(start=True)
        myShips.stage = 1
        myShips.main_game_one_player(myGraphics, myGameBoard, -1, 0)


def reset():
    myShips.reset()
    myGameBoard.reset()
    myGraphics.reset()


if __name__ == "__main__":
    myWindow = MyWindow()
    myGameBoard = MyGameBoard(myWindow)
    myGameBoard.initliazation()
    myShips = Ships()
    myGraphics = Graphics(myWindow)
    myWindow.mainloop()




