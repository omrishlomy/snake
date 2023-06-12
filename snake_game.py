import argparse
from typing import Optional
from game_display import GameDisplay
import game_utils
from argparse import Namespace
import argparse
from the_walls import Wall
import math

class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
        self.__x = args.height//2
        self.__y = args.width//2
        self.__width = args.width
        self.__height = args.height
        self.__num_apples, self.__num_walls = args.apples, args.walls
        self.__key_clicked = None
        self.__snake_coordinates = [(self.__x, self.__y - 2), (self.__x, self.__y - 1), (self.__x, self.__y)]
        self.__head_direction = 'Up'
        self.__walls = []
        self.__apples = []
        self.__lengthenning = 0
        self.score = 0




    def read_key(self, key_clicked: Optional[str])-> None:
        self.__key_clicked = key_clicked


    def change_direction(self):
        """this function get the key fron GameDisplay and change the direction of the snake's head
            according to the key. it also checks if the direction and key are'nt at opposite directions"""
        if self.__key_clicked == "Up" and self.__head_direction != "Down":
            self.__head_direction = "Up"
        if self.__key_clicked == "Right" and self.__head_direction != "Left":
            self.__head_direction = "Right"
        if self.__key_clicked == "Down" and self.__head_direction != "Up":
            self.__head_direction = "Down"
        if self.__key_clicked == "Left" and self.__head_direction != "Right":
            self.__head_direction = "Left"
        else:
            self.__head_direction = self.__head_direction



    def snake_eat_apple(self):
        wnt_to_go = (self.__x,self.__y)
        if wnt_to_go in self.__apples:
            self.__apples.remove(wnt_to_go)
            return True

    def wall_smash_snake(self):
        head = (self.__x,self.__y)
        for wall in self.__walls:
            if head in wall.coordinates:
                return True




    def eat_snake(self):
        """ this method checks if the snake is going to eat its tail, in another words,
            it will check it the location we want to add to the snake coordinates is already
                in the list"""
        if self.__head_direction != None:
            head = (self.__x, self.__y)
            if self.__snake_coordinates.count(head) > 1:
               return True
            else:
                return False


    def update_snake(self):
        if (self.__head_direction == 'Left') and (self.__x > 0):
            self.__x -= 1
        elif (self.__head_direction == 'Right') and (self.__x < self.__width):
            self.__x += 1
        elif (self.__head_direction == 'Up') and (self.__x < self.__height):
            self.__y += 1
        elif (self.__head_direction == 'Down') and (self.__x > 0):
            self.__y -= 1
        wnt_to_go = (self.__x, self.__y)
        if self.eat_snake():
            return False
        if self.__head_direction != None:
            if self.snake_eat_apple():
                self.score += int(math.sqrt((len(self.__snake_coordinates))))
                self.__lengthenning +=3
            if self.__lengthenning !=0:
                self.__snake_coordinates.append(wnt_to_go)
                self.__lengthenning -= 1
            else:
                self.__snake_coordinates.append(wnt_to_go)
                self.__snake_coordinates.pop(0)



    def draw_board(self, gd: GameDisplay) -> None:
        for apple in self.__apples:
            gd.draw_cell(apple[0],apple[1],"green")

        for cell in range(len(self.__snake_coordinates)):
                gd.draw_cell(self.__snake_coordinates[cell][0], self.__snake_coordinates[cell][1], "black")

        for wall in self.__walls:
            for (x,y) in wall.coordinates:
                gd.draw_cell(x, y, "blue")


    def update_objects(self, round)-> None:
        self.walls_updater(round)
        self.update_snake()
        self.las_manzanas(self.__apples)
        # if self.wall_smash_snake():
        #     self.__snake_coordinates.pop(-1)



    def check_in_board(self,gd:GameDisplay):
        """check if the snake is in the limits of the board, draw the relevant cell while 
            the snake reaches one of the board limits""" #need to chane width and height to args
        for cell in range(len(self.__snake_coordinates)):
            if (self.__snake_coordinates[cell][0] >= self.__width) or (
                    self.__snake_coordinates[cell][1] >= self.__height):
                    self.__snake_coordinates = self.__snake_coordinates[:-1]
                    self.draw_board(gd)
                    return True
            if self.__snake_coordinates[cell][0] <= 0 or self.__snake_coordinates[cell][1] <= 0:
                    self.__snake_coordinates = self.__snake_coordinates[:-1]
                    self.draw_board(gd)
                    return True


    def is_over(self,gd:GameDisplay,rounds, args: argparse.Namespace) -> bool:
        if self.check_in_board(gd) or rounds == args.rounds or self.eat_snake() or self.wall_smash_snake():
            # show_score #function that prints the score prerrylli
            return True

    def end_round(self) -> None:
        pass

#walls functions:

    #removes out of board walls coordinations
    def walls_coo_filter(self):
        wall_removed = False
        for wall in self.__walls:
            new_coo = list(wall.coordinates)
            for co_o in range(len(wall.coordinates)):
                x, y = wall.coordinates[co_o]
                if x < 0 or y < 0 or x >= self.__width or y >= self.__height:   #args.width or y >= args.height:
                    new_coo.remove(wall.coordinates[co_o])
            wall.coordinates = new_coo
            if len(wall.coordinates) == 0:
                self.__walls.remove(wall)
                wall_removed = True
        return wall_removed


    def walls_updater(self, round):
        if round % 2 == 0:
            new_coo = []
            for wall in self.__walls:
                new_coo.append(wall.move())
            hitted = self.wall_cut_things(new_coo)
            if hitted != None:
                self.__snake_coordinates = self.__snake_coordinates[hitted + 1:]
        if self.walls_coo_filter():
            self.wall_adder()
        self.wall_adder()



    def wall_adder(self):
        if len(self.__walls) < self.__num_walls:
            *center, direction = game_utils.get_random_wall_data()
            new_wall = Wall(direction, center)
            if self.new_wall_checker(new_wall.coordinates):
                self.__walls.append(new_wall)
                self.walls_coo_filter()




    def new_wall_checker(self, new_wall_coo):
        for co_o in new_wall_coo:
            if (co_o in self.__apples or co_o in self.__snake_coordinates):
                return False
        for co_o in new_wall_coo:
            for wall in self.__walls:
                if co_o in wall.coordinates:
                    return False
        return True


    def wall_cut_things(self, new_coo):
        for apple in self.__apples:
            if apple in new_coo:
                self.__apples.remove(apple)
        for co_o in range(len(self.__snake_coordinates)):
            if self.__snake_coordinates[co_o] in new_coo:
                return co_o




    #apples
    def las_manzanas(self, apples_lst):
        if len(apples_lst) < self.__num_apples:
            new_apple = game_utils.get_random_apple_data()
            if new_apple in self.__snake_coordinates: return

            for wall in self.__walls:
                if new_apple in wall.coordinates: return

            apples_lst.append(new_apple)






        # if self.eat_snake():
        #     return True



