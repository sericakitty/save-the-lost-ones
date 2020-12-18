
import pygame as pg
import random
import os
import time


# Class Robot
class Robot:
    def __init__(self,screen, image, x: float, y: float, screen_width: int, screen_height: int):
        self.__screen = screen
        self.__image = image
        self.__x = x
        self.__y = y
        self.__screen_width = screen_width
        self.__screen_height = screen_height

    def set_image(self, image):
        self.__image = image

    def image(self):
        return self.__image

    def draw(self):
        self.__screen.blit(self.__image, (self.__x, self.__y))

    def left_side(self):
        return self.__x + int(self.image().get_width()*0.20)

    def right_side(self):
        return self.__x + int(self.image().get_width()*0.80)

    def top_side(self):
        return self.__y + int(self.image().get_height()*0.20)

    def bottom_side(self):
        return self.__y + int(self.image().get_height()*0.80)

    def to_right(self):
        if (self.__x + self.__image.get_width()) < self.__screen_width:
            self.__x += 0.5
        
    def to_left(self):
        if 0 < self.__x:    
            self.__x -= 0.5
        
    def to_up(self):
        if 0 < self.__y:
            self.__y -= 0.5
    
    def to_down(self):
        if (self.__y + self.__image.get_height()) < self.__screen_height:
            self.__y += 0.5
    
    def collide(self, toinen):
        if self.right_side() >= toinen.left_side() and \
            self.left_side() <= toinen.right_side() and \
            self.top_side() <= toinen.bottom_side() and \
            self.bottom_side() >= toinen.top_side():
                return True
        return False


# Class monster
class Monster:
    def __init__(self, screen, image, x: float, y: float):
        self.__screen = screen
        self.__image = image
        self.__x = x
        self.__y = y
        self.__speed_x = random.choice([-2, -1, 1, 2])
        self.__speed_y = random.choice([-2, -1, 1, 2])

    def image(self):
        return self.__image

    def draw(self):
        self.__screen.blit(self.__image, (self.__x, self.__y))

    def left_side(self):
        return self.__x + int(self.image().get_width()*0.20)

    def right_side(self):
        return self.__x + int(self.image().get_width()*0.80)

    def top_side(self):
        return self.__y + int(self.image().get_height()*0.20)

    def bottom_side(self):
        return self.__y + int(self.image().get_height()*0.80)

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def speed_up_x(self):
        self.__x += self.__speed_x
    
    def speed_up_y(self):
        self.__y += self.__speed_y

    def change_direction_y(self, direction:str):
        if direction == "to_up":
            self.__speed_y = -(self.__speed_y)
        if direction == "to_down":
            self.__speed_y = -(self.__speed_y)

    def change_direction_x(self, direction:str):
        if direction == "to_right":
            self.__speed_x = -(self.__speed_x)
        if direction == "to_left":
            self.__speed_x = -(self.__speed_x)

    def collide(self, toinen):
        if self.right_side() >= toinen.left_side() and \
            self.left_side() <= toinen.right_side() and \
            self.top_side() <= toinen.bottom_side() and \
            self.bottom_side() >= toinen.top_side():
                return True
        return False

    def speed_up(self):
        if self.__speed_x < 0:
            self.__speed_x -= random.choice([0.5, 0.75, 1, 1.25, 1.5])
        else:
            self.__speed_x += random.choice([0.5, 0.75, 1, 1.25, 1.5])
            
        
        if self.__speed_y < 0:
            self.__speed_y -= random.choice([0.5, 0.75, 1, 1.25, 1.5])
        else:
            self.__speed_y += random.choice([0.5, 0.75, 1, 1.25, 1.5])
    

# Class Coin
class Coin:
    def __init__(self, screen, image, x: int, y: int):
        self.__screen = screen
        self.__image = image
        self.__x = x
        self.__y = y
        
    def image(self):
        return self.__image

    def draw(self):
        self.__screen.blit(self.__image, (self.__x, self.__y))

    def left_side(self):
        return self.__x + int(self.image().get_width()*0.20)

    def right_side(self):
        return self.__x + int(self.image().get_width()*0.80)

    def top_side(self):
        return self.__y + int(self.image().get_height()*0.20)

    def bottom_side(self):
        return self.__y + int(self.image().get_height()*0.80)

# Class Door
class Door:
    def __init__(self, screen, image, x: int, y: int):
        self.__screen = screen
        self.__image = image
        self.__x = x
        self.__y = y

    def image(self):
        return self.__image

    def draw(self):
        self.__screen.blit(self.__image, (self.__x, self.__y))

    def left_side(self):
        return self.__x + int(self.image().get_width()*0.50)

    def right_side(self):
        return self.__x + int(self.image().get_width()*0.50)

    def top_side(self):
        return self.__y + int(self.image().get_height()*0.50)

    def bottom_side(self):
        return self.__y + int(self.image().get_height()*0.50)

# Main game class
class SaveTheLostOnes:
    def __init__(self):
        pg.init()

        self.run = False
        self.main_menu = True
        self.win = False
        self.lose = False

        self.n_lost_games = 0
        self.n_won_games = 0

        self.start_time = pg.time.get_ticks()

        while self.main_menu:

            self.load_pics()
            self.new_game()

            self.width = len(self.game_map[0])
            self.height = len(self.game_map)
            self.scale = self.images[1].get_width()
            
            
            self.screen_width = self.width * self.scale
            self.screen_height = self.height * self.scale
        
            self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

            self.yellow = (255,255,0)
            self.red = (255, 0, 0)

            pg.display.set_caption("Save the Lost Ones")

            self.find_robot()
            self.find_morsters()
            self.find_coins()
            self.find_doors()
            self.liiku()

            self.draw_main_menu()
            
            self.main_menu_events()

            if self.run:
                self.loop()

    # function for drawing text
    def draw_text(self, text:str, size:int, color:int, width:float, height:float):
        font = pg.font.SysFont("Arial", size)
        text = font.render(f"{text}", True, (color))
        center_text = text.get_rect(center=(self.screen_width*width, self.screen_height*height))

        self.screen.blit(text, center_text)
    
    # Draw the main menu
    def draw_main_menu(self):
        self.screen.fill((5, 5, 5))

        caption_text = "Save the Lost Ones"
        self.draw_text(caption_text, 48, self.red, 0.50, 0.25)

        description_text = "''Collect the coin and save the lost ones, but be careful not to fall into darkness''"
        self.draw_text(description_text, 25, self.red, 0.50, 0.40)

        moving_description = "Move robot with the arrow keys"
        self.draw_text(moving_description, 20, self.red, 0.50, 0.50)
        
        self.screen.blit(self.images[0], (self.screen_width*0.15, self.screen_height*0.60))
        pg.draw.polygon(self.screen, (self.red), ((self.screen_width*0.25, self.screen_height*0.65), (self.screen_width*0.25, self.screen_height*0.67), (self.screen_width*0.275, self.screen_height*0.67), (self.screen_width*0.275, self.screen_height*0.68), (self.screen_width*0.30, self.screen_height*0.66), (self.screen_width*0.275, self.screen_height*0.64), (self.screen_width*0.275, self.screen_height*0.65)))
        self.screen.blit(self.images[1], (self.screen_width*0.35, self.screen_height*0.63))
        pg.draw.polygon(self.screen, (self.red), ((self.screen_width*0.475, self.screen_height*0.65), (self.screen_width*0.475, self.screen_height*0.67), (self.screen_width*0.5, self.screen_height*0.67), (self.screen_width*0.5, self.screen_height*0.68), (self.screen_width*0.525, self.screen_height*0.66), (self.screen_width*0.5, self.screen_height*0.64), (self.screen_width*0.5, self.screen_height*0.65)))
        self.screen.blit(self.images[2], (self.screen_width*0.60, self.screen_height*0.60))
        pg.draw.polygon(self.screen, (self.red), ((self.screen_width*0.70, self.screen_height*0.65), (self.screen_width*0.70, self.screen_height*0.67), (self.screen_width*0.725, self.screen_height*0.67), (self.screen_width*0.725, self.screen_height*0.68), (self.screen_width*0.75, self.screen_height*0.66), (self.screen_width*0.725, self.screen_height*0.64), (self.screen_width*0.725, self.screen_height*0.65)))
        self.screen.blit(self.images[3], (self.screen_width*0.80, self.screen_height*0.60))

        start_game_description = "Start the game? ( y / n )"
        self.draw_text(start_game_description, 20, self.red, 0.50, 0.80)
        
        pg.display.flip()

    # Main menu events
    def main_menu_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                self.main_menu = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.main_menu = False
                    
                if event.key == pg.K_y:
                    self.run = True

                if event.key == pg.K_n:
                    self.main_menu = False

    # Load foder pics into game 
    def load_pics(self):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, "img")

        self.images = []
        for nimi in ["robo", "coin", "soul", "door"]:
            self.images.append(pg.image.load(os.path.join(img_folder, nimi + ".png")))

    # Create new game and load map
    def new_game(self):
        self.game_map = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
                        [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Find location of robot, x and y, and create object
    def find_robot(self):
        robot_x = 0
        robot_y = 0 
        for y in range(self.height):
            for x in range(self.width):
                if self.game_map[y][x] == 1:
                    robot_x = x * self.scale
                    robot_y = y * self.scale

        self.robot = Robot(self.screen, self.images[0], robot_x, robot_y, self.screen_width, self.screen_height)

    # Find all coins and add them to list and create object
    def find_coins(self):
        self.coinlist = []
        self.coins = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.game_map[y][x] == 2:
                    self.coinlist.append(Coin(self.screen, self.images[1], x * self.scale, y * self.scale))

        random.shuffle(self.coinlist)
        self.n_coins = len(self.coins)
        self.collected_coins = 0
        self.remove_collected_coin = -1

        n = 1
        for i in self.coinlist:
            if n <= self.total_monsters+1:
                self.coins.append(i)
            n+=1
        random.shuffle(self.coins)

    # Find all monster from map and add them to list and create object
    def find_morsters(self):
        self.monsters = []

        for y in range(self.height):
            for x in range(self.width):
                if self.game_map[y][x] == 3:
                    self.monsters.append(Monster(self.screen, self.images[2], x * self.scale, y * self.scale))

        self.n_mosters = len(self.monsters)
        self.total_monsters = self.n_mosters
        self.saved_monsters = 0
        self.remove_saved_monster = -1
    
    # Find all doors from map and add them to list and create object
    def find_doors(self):
        self.doors = []

        for y in range(self.height):
            for x in range(self.width):
                if self.game_map[y][x] == 4:
                    self.doors.append(Door(self.screen, self.images[3], x * self.scale, y * self.scale))

        random.shuffle(self.doors)
        self.door_is_open = False

    # Check if robot moves statement are True
    def liiku(self):
        self.to_up = False
        self.to_down = False
        self.to_right = False
        self.to_left = False
    
    # If arrow keys are pressed, move robot
    def move_robot(self):
        if self.to_up:
            self.robot.to_up()
        if self.to_down:
            self.robot.to_down()
        if self.to_right:
            self.robot.to_right()
        if self.to_left:
            self.robot.to_left()

    # Display collected coin
    def display_collected_coin(self):
        text = f"Collected coin: {self.collected_coins}/1"
        self.draw_text(text, 20, self.yellow, 0.10, 0.025)
    
    # Display saved monsters
    def display_saved_monsters(self):
        text = f"Saved monsters: {self.saved_monsters}/{self.total_monsters}"
        self.draw_text(text, 20, self.yellow, 0.30, 0.025)

    # Display timer
    def display_timer(self):
        timer = f"{int(pg.time.get_ticks() - self.start_time)/1000}"
        self.draw_text(timer, 20, self.yellow, 0.50, 0.025)

        time = f"Timer:               seconds"
        self.draw_text(time, 20, self.yellow, 0.505, 0.025)

    # Display number of losed games
    def display_lost_games(self):
        text = f"Lost games: {self.n_lost_games}"
        self.draw_text(text, 20, self.yellow, 0.75, 0.025)

    # Display number of won games
    def display_won_games(self):
        text = f"Won games {self.n_won_games}"
        self.draw_text(text, 20, self.yellow, 0.90, 0.025)
    
    # Display win text at the end
    def show_win_text(self):
        text = "The salvation of the lost ones required a great sacrifice..."
        self.draw_text(text, 30, self.red, 0.50, 0.50)
        pg.display.flip()

    # Display lose text at the end
    def display_lose_text(self):
        text = f"The Lost ones got you..."
        self.draw_text(text, 30, self.red, 0.50, 0.50)
        pg.display.flip()

    # Remove coin from list
    def remove_coin(self, remove:int):
        if remove != -1:
            self.coins.pop(remove)
            self.collected_coins += 1
            self.remove_collected_coin = -1
            for i in self.monsters:
                i.speed_up()

    # Remove monster from list
    def remove_monster(self, remove:int):
        if remove != -1:
            self.n_mosters -= 1
            self.monsters.pop(remove)
            self.saved_monsters += 1
            self.remove_saved_monster = -1
            self.collected_coins = 0
            for i in self.monsters:
                i.speed_up()

    # Move monster
    def move_monsters(self, i):
        if self.monsters[i].get_speed_x() > 0 and self.monsters[i].right_side() >= self.screen_width:
            self.monsters[i].change_direction_x("to_left")
        if self.monsters[i].get_speed_y() > 0 and self.monsters[i].bottom_side() >= self.screen_height:
            self.monsters[i].change_direction_y("to_up")
        if self.monsters[i].get_speed_x() < 0 and self.monsters[i].left_side() <= 0:
            self.monsters[i].change_direction_x("to_right")
        if self.monsters[i].get_speed_y() < 0 and self.monsters[i].top_side() <= 0:
            self.monsters[i].change_direction_y("to_down")

    # Game events
    def game_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.run = False
                self.main_menu = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.to_left = True    
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.to_right = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.to_up = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.to_down = True

            elif event.type == pg.KEYUP and event.key == pg.K_LEFT:
                self.to_left = False
            elif event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                self.to_right = False
            elif event.type == pg.KEYUP and event.key == pg.K_UP:
                self.to_up = False
            elif event.type == pg.KEYUP and event.key == pg.K_DOWN:
                self.to_down = False

    # Create game loop
    def loop(self):
        while self.run:
            self.game_events()
            self.draw_game()
        
        # If lose, display lose text
        if self.lose:
            self.display_lose_text()
            pg.time.wait(1000)
            self.n_lost_games += 1
            self.lose = False
        
        # if win, display win text
        elif self.win:
            self.show_win_text()
            pg.time.wait(2500)
            self.n_won_games += 1
            self.win = False
        
        self.start_time = pg.time.get_ticks()
            
    # Draw the game loop
    def draw_game(self):
        
        self.screen.fill((2, 2, 2))

        # If all monster are saved, open the door
        if self.saved_monsters == self.total_monsters:
            self.door_is_open = True
            self.doors[0].draw()

            # If door is open and robot hits the door -> win the game
            if self.door_is_open and self.robot.collide(self.doors[0]):
                self.robot.set_image(self.images[2])
                self.win = True
                self.run = False
        
        # If collected coin are zero and not all monsters are saved, create coin
        if self.collected_coins == 0 and not self.saved_monsters == self.total_monsters:
            
            # If robot hits the coin and collected coins are zero, collect the coin
            if self.robot.collide(self.coins[0]) and self.collected_coins == 0:
                self.remove_collected_coin = 0
            
            # Diplay coin
            self.coins[0].draw()

        # Remove collected coin from game
        self.remove_coin(self.remove_collected_coin)
            
        # Move robot
        self.move_robot()

        # Piirretään robotti peliin
        self.robot.draw()

        # Create monster to game if more than zero
        if len(self.monsters) > 0:
            for i in range(self.n_mosters):
                
                # If collected coins are zero and monster hits to robot, lose the game
                if self.collected_coins == 0 and self.monsters[i].collide(self.robot):
                    self.lose = True
                    self.run = False
                    self.main_menu = True
                    
                
                # Move the monster
                self.monsters[i].speed_up_x()
                self.monsters[i].speed_up_y()

                self.move_monsters(i)

                # If collected coins are more than zero and monster hits to robot, monster is saved
                if self.collected_coins == 1 and self.monsters[i].collide(self.robot):
                    self.remove_saved_monster = i

                # Display the monster
                self.monsters[i].draw()

        # Remove saved monster from game and from list
        self.remove_monster(self.remove_saved_monster)
        
        # Display collected coin
        self.display_collected_coin()

        # Display saved monsters
        self.display_saved_monsters()

        # Display timer
        self.display_timer()
        
        # Display lost games
        self.display_lost_games()

        # Display won games
        self.display_won_games()
        
        pg.display.flip()
        
if __name__ == '__main__':

    SaveTheLostOnes()
    
