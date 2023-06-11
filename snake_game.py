import argparse
from typing import Optional
from game_display import GameDisplay
import game_utils
from argparse import Namespace
import argparse
from the_walls import Wall

class SnakeGame:

    def __init__(self, args: argparse.Namespace) -> None:
        self.__x = args.height//2
        self.__y = args.width//2
        self.__width = args.width
        self.__height = args.height
        self.__key_clicked = None
        self.__snake_coordinates = [(self.__x, self.__y - 2), (self.__x, self.__y - 1), (self.__x, self.__y)]
        self.__head_direction = 'Up'
        self.__walls = []


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



    def update_objects(self, round)-> None:
        if (self.__head_direction == 'Left') and (self.__x > 0):
            self.__x -= 1
        elif (self.__head_direction == 'Right') and (self.__x < self.__width):
            self.__x += 1
        elif (self.__head_direction == 'Up') and (self.__x < self.__height):
            self.__y += 1
        elif (self.__head_direction == 'Down') and (self.__x > 0):
            self.__y -= 1
        self.walls_updater(round)



    def eat_snake(self):
        """ this method checks if the snake is going to eat its tail, in another words,
            it will check it the location we want to add to the snake coordinates is already
                in the list"""
        if self.__head_direction != None:
            wnt_to_go = (self.__x, self.__y)
            if wnt_to_go in self.__snake_coordinates:
               return True
            else:
                return False



    def draw_board(self, gd: GameDisplay) -> None:
        wnt_to_go = (self.__x,self.__y)
        if self.__head_direction !=None:
            self.__snake_coordinates.append(wnt_to_go)
            self.__snake_coordinates.pop(0)

        for cell in range(len(self.__snake_coordinates)):
                gd.draw_cell(self.__snake_coordinates[cell][0], self.__snake_coordinates[cell][1], "black")
                print("drew cell", self.__snake_coordinates[cell])

        for wall in self.__walls:
            for (x,y) in wall.coordinates:
                gd.draw_cell(x, y, "blue")





    def end_round(self) -> None:
        pass



    def check_in_board(self,gd:GameDisplay):
        """check if the snake is in the limits of the board, draw the relevant cell while 
            the snake reaches one of the board limits""" #need to chane width and height to args
        for cell in range(len(self.__snake_coordinates)):
            if (self.__snake_coordinates[cell][0] >= 40 and self.__head_direction == "Right") or (
                    self.__snake_coordinates[cell][1] >= 30 and self.__head_direction == "Up"):
                    self.__snake_coordinates = self.__snake_coordinates[:-1]
                    self.draw_board(gd)
                    return True
            if (self.__snake_coordinates[cell][0] < 0 and self.__head_direction == "Left") or (
                    self.__snake_coordinates[cell][1] < 0 and self.__head_direction == "Down"):
                    self.__snake_coordinates = self.__snake_coordinates[:-1]
                    self.draw_board(gd)
                    return True


    def walls_coo_filter(self):
        for wall in self.__walls:
            new_coo=list(wall.coordinates)
            for co_o in range(len(wall.coordinates)):
                x, y = wall.coordinates[co_o]
                if x < 0 or y < 0 or x >= self.__width or y >= self.__height:   #args.width or y >= args.height:
                    new_coo.remove(wall.coordinates[co_o])
            wall.coordinates=new_coo

            if len(wall.coordinates) == 0:
                self.__walls.remove(wall)

    def walls_updater(self, round):
        if round%2==0:
            for wall in self.__walls:
                wall.move()
        self.walls_coo_filter()

        if len(self.__walls) <3: #args.walls:
            *center, direction = game_utils.get_random_wall_data()
            new_wall = Wall(direction, center)
            self.__walls.append(new_wall)
        self.walls_coo_filter()

    def is_over(self,gd:GameDisplay) -> bool:
        if self.check_in_board(gd):
            return True
        # if self.eat_snake():
        #     return True



