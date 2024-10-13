import curses
import random
from time import sleep
from agent import Agent
from excel import Excel


class Screen:
    def __init__(self, matrix, height, width, iteractions):
        self.iteractions = iteractions
        self.excel = Excel()
        self.height, self.width = height, width
        self.matrix = matrix

    def add_agent(self, agent: Agent):
        self.agent = agent

    def __board(self, win):
        for y in range(self.height):
            for x in range(self.width):
                value = self.matrix[y][x]
                if y == self.agent.y and x == self.agent.x:
                    self.agent.cam_0 = value
                    win.addstr(self.agent.y,
                               self.agent.x,
                               self.agent.get_model(),
                               curses.color_pair(4))
                    continue
                if value == 2:
                    color_pair = 3
                else:
                    color_pair = 2 if value == 0 else 1
                win.addstr(y,
                           x,
                           str(value),
                           curses.color_pair(color_pair))

    def __windows(self, stdscr: curses.initscr):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        pos_y = (height - self.height) // 2
        pos_x = (width - self.width) // 2

        win = curses.newwin(self.height+1, self.width+1, pos_y, pos_x)
        win.keypad(True)
        self.win_data = curses.newwin(8, 25, pos_y, pos_x-25)
        self.win_data.box()
        self.win_data.refresh()

        self.__board(win)
        data = self.agent.load_data_sensors()
        self.print_data(data)
        win.refresh()
        y, x = 0, 0
        i = 1
        win.getch()
        while True:
            try:
                if i <= self.iteractions:
                    sleep(0.5)
                    y, x = self.agent.get_position()
                    old_model = self.agent.get_model()
                    win.addstr(y,
                               x,
                               str(self.matrix[y][x]),
                               curses.color_pair(2 if self.matrix[y][x] == 0 else 1))
                    self.agent.advance(data)
                    data = self.agent.load_data_sensors()
                    win.addstr(self.agent.y,
                               self.agent.x,
                               self.agent.get_model(),
                               curses.color_pair(4))
                    self.print_data(data)
                    win.refresh()

                    self.excel.add_row(
                        '({},{})'.format(y, x),
                        old_model,
                        data.get('cam_0'),
                        data.get('cam_left'),
                        data.get('cam_center'),
                        data.get('cam_right'),
                        self.agent.rule,
                        self.agent.get_action(),
                        '({}, {})'.format(self.agent.y, self.agent.x),
                        self.agent.get_model())
                    i += 1
                else:
                    self.excel.to_excel('/home/cimeries/book.xlsx')
                    break
            except KeyboardInterrupt:
                self.excel.to_excel('/home/cimeries/book.xlsx')
                break

    def print_data(self, data: dict):
        self.win_data.addstr(
            1,
            1,
            'Position:({},{})'.format(self.agent.x, self.agent.y))
        self.win_data.addstr(
            2, 1, 'Cam: {}'.format(data.get('cam_0')))
        self.win_data.addstr(
            3, 1,
            'Cam left: {}'.format(data.get('cam_left')))
        self.win_data.addstr(
            4, 1, 'Cam center: {}'.format(data.get('cam_center')))
        self.win_data.addstr(
            5, 1, 'Cam right: {}'.format(data.get('cam_right')))
        self.win_data.addstr(
            6, 1, 'agent: {}'.format(self.agent.get_model_str()))
        self.win_data.refresh()

    def draw_board(self):
        curses.wrapper(self.__windows)
