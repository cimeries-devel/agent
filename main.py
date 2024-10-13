from board import Board
from screen import Screen
from agent import Agent
from excel import Excel
import random


if __name__ == '__main__':
    board = Board(22, 22)
    screen = Screen(board.matrix,
                    board.height,
                    board.width,
                    1000)
    agent = Agent(5, 1)
    agent.set_matrix(board.matrix)
    screen.add_agent(agent)
    screen.draw_board()
