class Player:
    """
    在Table类里面模拟玩家行为的类
    只是用来存储数据的
    """

    def __init__(self):
        self.hand_tiles = []
        self.discard_tiles = []
        self.melds = []
        self.self_wind = None  # should in (0, 1, 2, 3)
        self.point_bar = None  # should be integer number
