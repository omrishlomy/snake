import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:

    # INIT OBJECTS
    game = SnakeGame(args)
    gd.show_score(0)
    round_num = 0
    # DRAW BOARD
    game.draw_board(gd)
    # END OF ROUND 0
    while not game.is_over(gd):
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        game.change_direction()
        if game.check_in_board(gd):
            continue
        # UPDATE OBJECTS
        game.update_objects(round_num)
        if game.eat_snake():
            return
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        round_num +=1
        game.end_round()
        gd.end_round()

if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")
