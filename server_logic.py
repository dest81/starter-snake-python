import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""
def remove_moves(moves, move):
    if move in moves:
        moves.remove(move)
    return moves


def avoid_cells(my_head: Dict[str, int], cells: List[dict], possible_moves: List[str]) -> List[str]:

    for c in cells:
        x_c, y_c = c.values()
        if x_c + 1 == my_head["x"] and y_c == my_head["y"]:
            remove_moves(possible_moves, "left")
        if x_c - 1 == my_head["x"] and y_c == my_head["y"]:
            remove_moves(possible_moves, "right")

        if y_c + 1 == my_head["y"] and x_c == my_head["x"]:
            remove_moves(possible_moves, "down")
        if y_c -1 == my_head["y"] and x_c == my_head["x"]:
            remove_moves(possible_moves, "up")

        return possible_moves


def food_first(my_head: Dict[str, int], cells: List[dict], possible_moves: List[str]) -> List[str]:

    for c in cells:
        x_c, y_c = c.values()
        if x_c + 1 == my_head["x"] and y_c == my_head["y"]:
            possible_moves = ["left"]
        elif x_c - 1 == my_head["x"] and y_c == my_head["y"]:
            possible_moves = ["right"]
        elif y_c + 1 == my_head["y"] and x_c == my_head["x"]:
            possible_moves = ["down"]
        elif y_c -1 == my_head["y"] and x_c == my_head["x"]:
            possible_moves =  ["up"]

    return possible_moves


def avoid_board_edges(my_head: Dict[str, int], my_board: List[dict], possible_moves: List[str]) -> List[str]:
    height = my_board["height"]
    width = my_board["width"]

    if my_head["x"] == 0:
        remove_moves(possible_moves, "left")
    elif my_head["x"] == width-1:
        remove_moves(possible_moves, "right")

    if my_head["y"] == 0:
        remove_moves(possible_moves, "down")
    elif my_head["y"] == height-1:
        remove_moves(possible_moves, "up")

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]
    my_board = data["board"]

    possible_moves = ["up", "down", "left", "right"]

    # food first
    food = data["board"]["food"]
    possible_moves = food_first(my_head, food, possible_moves)
    if len(possible_moves) == 1:
        return possible_moves[0]

    # avoid board
    # print("avoid edges")
    possible_moves = avoid_board_edges(my_head, my_board, possible_moves)

    # avoid own body
    my_body = data["you"]["body"]
    possible_moves = avoid_cells(my_head, my_body, possible_moves)
    # print(possible_moves)

    # avoid own other snakes
    snakes = data["board"]["snakes"]
    for snake in snakes:
        snake_body = snake["body"]
        possible_moves = avoid_cells(my_head, snake_body, possible_moves)

    # avoid hazards
    hazards = data["board"]["hazards"]
    possible_moves = avoid_cells(my_head, hazards, possible_moves)
    print(possible_moves)

    print(my_head)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    print(possible_moves)
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
