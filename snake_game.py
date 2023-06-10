from typing import Optional
from game_display import GameDisplay
import argparse

class SnakeGame:

    def __init__(self) -> None:
        self.__x = 40//2 #need to change to arg.height//2
        self.__y = 30//2  #need to change to arg.width//2
        self.__key_clicked = None
        self.__coordinates = [(self.__x, self.__y - 2), (self.__x, self.__y - 1), (self.__x, self.__y)]
        self.__head_direction = None

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
    def update_objects(self)-> None:
        if (self.__head_direction == 'Left') and (self.__x > 0):
            self.__x -= 1
        elif (self.__head_direction == 'Right') and (self.__x < 39): #need to change to args.width
            self.__x += 1
        elif (self.__head_direction == 'Up') and (self.__x < 29): #need to change to args.height
            self.__y += 1
        elif (self.__head_direction == 'Down') and (self.__x > 0):
            self.__y -= 1
    def eat_snake(self):
        """ this method checks if the snake is going to eat its tail, in another words,
            it will check it the location we want to add to the snake coordinates is alreadt
                in the list"""
        if self.__head_direction != None:
            wnt_to_go = (self.__x, self.__y)
            if wnt_to_go in self.__coordinates:
               return True
            else:
                return False
    def draw_board(self, gd: GameDisplay) -> None:
        print(("coordinates", self.__coordinates))
        wnt_to_go = (self.__x,self.__y)
        print("wnt_to_go", wnt_to_go)
        if self.__head_direction !=None:
            self.__coordinates.append(wnt_to_go)
            self.__coordinates.pop(0)
            print(self.__coordinates)
        for cell in range(len(self.__coordinates)):
                gd.draw_cell(self.__coordinates[cell][0],self.__coordinates[cell][1], "blue")
                print("drew cell", self.__coordinates[cell])


    def end_round(self) -> None:
        pass
    def check_in_board(self,gd:GameDisplay):
        """check if the snake is in the limits of the board, draw the relevant cell while 
            the snake reaches one of the board limits""" #need to chane width and height to args
        for cell in range(len(self.__coordinates)):
            if (self.__coordinates[cell][0] >= 40 and self.__head_direction == "Right") or (
                self.__coordinates[cell][1] >= 30 and self.__head_direction == "Up"):
                    self.__coordinates = self.__coordinates[:-1]
                    self.draw_board(gd)
                    return True
            if (self.__coordinates[cell][0] < 0 and self.__head_direction == "Left") or (
                self.__coordinates[cell][1] < 0 and self.__head_direction == "Down"):
                    self.__coordinates = self.__coordinates[:-1]
                    self.draw_board(gd)
                    return True

    def is_over(self,gd:GameDisplay) -> bool:
        if self.check_in_board(gd):
            return True
        # if self.eat_snake():
        #     return True



