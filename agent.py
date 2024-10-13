import random


class Agent:
    def __init__(self, y, x):
        self.y, self.x = y+1, x+1
        self.__agent = random.choice([0, 1, 2, 3])
        self.cam_0 = None
        self.cam_left = None
        self.cam_center = None
        self.cam_right = None
        self.rotations = {0: "▲",
                          1: "►",
                          2: "▼",
                          3: "◄"}

    def set_matrix(self, matrix):
        self.matrix = matrix

    def get_position(self):
        return self.y, self.x

    def get_model(self):
        return self.rotations.get(self.__agent)

    def get_model_str(self):
        return str(self.__agent)

    def get_action(self):
        return self.action

    def advance(self, data=dict):
        cl = data.get('cam_left')
        cc = data.get('cam_center')
        cr = data.get('cam_right')

        if (cl == 0 or cl == 2) and (cc == 0 or cc == 2) and (cr == 0 or cr == 2):
            self.rule = 1
            if self.__agent % 2 == 0:
                self.__agent = random.choice([1, 3])
                self.action = 'girar -90' if self.__agent == 1 else 'girar +90'
                return
            self.__agent = random.choice([0, 2])
            self.action = 'girar -90' if self.__agent == 0 else 'girar +90'
            return

        if cl == 1 and (cc == 0 or cc == 1) and (cr == 0 or cr == 2):
            self.rule = 2
            self.__step()
            if self.__agent == 0:
                self.__agent = 3
            elif self.__agent == 1:
                self.__agent = 0
            elif self.__agent == 2:
                self.__agent = 1
            elif self.__agent == 3:
                self.__agent = 2
            self.action = 'avanzar y girar -90'
            return
        if (cl == 0 or cl == 2) and (cc == 0 or cc == 1) and cr == 1:
            self.rule = 3
            self.__step()
            if self.__agent == 0:
                self.__agent = 1
            elif self.__agent == 1:
                self.__agent = 2
            elif self.__agent == 2:
                self.__agent = 3
            elif self.__agent == 3:
                self.__agent = 0
            self.action = 'avanzar y girar +90'
            return

        if cl == 1 and (cc == 0 or cc == 1) and cr == 1:
            self.rule = 4
            self.__step()
            if self.__agent % 2 == 0:
                self.__agent = random.choice([1, 3])
                self.action = 'avanzar y girar -90' if self.__agent == 1 else 'girar +90'
                return
            self.__agent = random.choice([0, 2])
            self.action = 'avanzar y girar -90' if self.__agent == 0 else 'girar +90'
            return

        if (cl == 0 or cl == 2) and cc == 1 and (cr == 0 or cr == 2):
            self.rule = 5
            self.__step()
            self.action = 'avanzar'
            return

        if (cl == 0 or cl == 2) and cc == 2 and cr == 1:
            self.rule = 6
            if self.__agent == 0:
                self.__agent = 1
            elif self.__agent == 1:
                self.__agent = 2
            elif self.__agent == 2:
                self.__agent = 3
            elif self.__agent == 3:
                self.__agent = 0
            self.action = 'girar +90'
            return

        if cl == 1 and cc == 2 and (cr == 0 or cr == 2):
            self.rule = 7
            if self.__agent == 0:
                self.__agent = 3
            elif self.__agent == 1:
                self.__agent = 0
            elif self.__agent == 2:
                self.__agent = 1
            elif self.__agent == 3:
                self.__agent = 2
            self.action = 'girar -90'
            return

        if cl == 1 and cc == 2 and cr == 1:
            self.rule = 8
            if self.__agent % 2 == 0:
                self.__agent = random.choice([1, 3])
                self.action = 'girar -90' if self.__agent == 1 else 'girar +90'
                return
            self.__agent = random.choice([0, 2])
            self.action = 'girar -90' if self.__agent == 0 else 'girar +90'
            return

    def __step(self):
        if self.__agent == 0:  # ▲
            self.y = self.y - 1
        elif self.__agent == 1:  # ►
            self.x = self.x + 1
        elif self.__agent == 2:  # ▼
            self.y = self.y + 1
        elif self.__agent == 3:  # ◄
            self.x = self.x - 1

    def load_data_sensors(self) -> dict:
        data = {
            "cam_0": 1 if self.matrix[self.y][self.x] == 1 else 0,
            "cam_left": 'n',
            "cam_center": 'n',
            "cam_right": 'n'}
        if self.__agent == 0:  # ▲
            value = self.matrix[self.y-1][self.x-1]
            data['cam_left'] = value

            value = self.matrix[self.y-1][self.x]
            data['cam_center'] = value

            value = self.matrix[self.y-1][self.x+1]
            data['cam_right'] = value

        elif self.__agent == 1:  # ►
            value = self.matrix[self.y-1][self.x+1]
            data['cam_left'] = value

            value = self.matrix[self.y][self.x+1]
            data['cam_center'] = value

            value = self.matrix[self.y+1][self.x+1]
            data['cam_right'] = value

        elif self.__agent == 2:  # ▼
            value = self.matrix[self.y+1][self.x+1]
            data['cam_left'] = value

            value = self.matrix[self.y+1][self.x]
            data['cam_center'] = value

            value = self.matrix[self.y+1][self.x-1]
            data['cam_right'] = value

        elif self.__agent == 3:  # ◄
            value = self.matrix[self.y+1][self.x-1]
            data['cam_left'] = value

            value = self.matrix[self.y][self.x-1]
            data['cam_center'] = value

            value = self.matrix[self.y-1][self.x-1]
            data['cam_right'] = value

        return data
