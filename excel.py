import pandas as pd


class Excel:
    def __init__(self):
        self.n = 1
        self.data = {
            'n': [],
            'pos_before': [],
            'ori_before': [],
            'cam_0': [],
            'cam_left': [],
            'cam_center': [],
            'cam_right': [],
            'rule': [],
            'action': [],
            'pos_after': [],
            'ori_after': []}

    def to_excel(self, path: str = None):
        df = pd.DataFrame(self.data)
        df.to_excel(path, index=True)

    def add_row(self, *args: list):
        self.data.get('n').append(self.n)
        self.data.get('pos_before').append(args[0])
        self.data.get('ori_before').append(args[1])
        self.data.get('cam_0').append(args[2])
        self.data.get('cam_left').append(args[3])
        self.data.get('cam_center').append(args[4])
        self.data.get('cam_right').append(args[5])
        self.data.get('rule').append(args[6])
        self.data.get('action').append(args[7])
        self.data.get('pos_after').append(args[8])
        self.data.get('ori_after').append(args[9])
        self.n += 1
