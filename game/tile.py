import random

man = 0  # 万子
pin = 1  # 饼子
suo = 2  # 索子
wind = 3  # 风牌
honor = 4  # 三元牌

mo = 0  # 摸牌
qie = 1  # 切牌
chi = 2  # 吃牌
peng = 3  # 碰牌
minggang = 4  # 明杠
angang = 5  # 暗杠
jiagang = 6  # 加杠


class Tile:
    """
    (type, value ,red)
    type表示种类，0是万，1是饼，2是索，3是风，是三元
    value表示数牌大小，从1~9。如果是字牌，风牌从0~3是东南西北，三元牌是0~2是白发中
    red表示是否是红宝牌。
    """
    # 各种集合，存储类型使用元组，匹配的时候使用base匹配
    numbers = tuple((cate, value, red) for cate in (man, pin, suo) for value in range(1, 10) for red in
                    ((0, 0, 0, 1) if value == 5 else (0, 0, 0, 0)))  # 数牌
    chars = tuple((wind, value, red) for value in range(4) for red in (0,) * 4)  # 字牌
    chars += tuple((honor, value, red) for value in range(3) for red in (0,) * 4)  # 字牌

    all = numbers + chars

    number_graph = {
        man: {1: "🀇", 2: "🀈", 3: "🀉", 4: "🀊", 5: "🀋", 6: "🀌", 7: "🀍", 8: "🀎", 9: "🀏"},
        pin: {1: "🀙", 2: "🀚", 3: "🀛", 4: "🀜", 5: "🀝", 6: "🀞", 7: "🀟", 8: "🀠", 9: "🀡"},
        suo: {1: "🀐", 2: "🀑", 3: "🀒", 4: "🀓", 5: "🀔", 6: "🀕", 7: "🀖", 8: "🀗", 9: "🀘"},

        wind: {0: "🀀", 1: "🀁", 2: "🀂", 3: "🀃"},
        honor: {0: "🀆", 1: "🀅", 2: "🀄"}
    }

    def __init__(self, category, value, red):
        self.base = (category, value, red)

    @staticmethod
    def generate_all_136_tiles():
        """
        产生所有136章牌
        :return:
        """
        return list(map(lambda b: Tile(*b), Tile.all))

    @property
    def __category(self):
        return self.base[0]

    @property
    def __value(self):
        return self.base[1]

    @property
    def __red(self):
        return self.base[2]

    def is_man(self):
        return self.__category == man

    def is_pin(self):
        return self.__category == pin

    def is_suo(self):
        return self.__category == suo

    def is_wind(self):
        return self.__category == wind

    def is_east(self):
        return self.is_wind() and self.__value == 0

    def is_south(self):
        return self.is_wind() and self.__value == 1

    def is_west(self):
        return self.is_wind() and self.__value == 2

    def is_north(self):
        return self.is_wind() and self.__value == 3

    def is_honor(self):
        return self.__category == honor

    def is_blank(self):
        return self.is_honor and self.__value == 0

    def is_fortune(self):
        return self.is_honor and self.__value == 1

    def is_center(self):
        return self.is_honor() and self.__value == 2

    def is_number(self):
        return self.is_man() or self.is_pin() or self.is_suo()

    def is_character(self):
        return self.is_wind() or self.is_honor()

    def is_red(self):
        return self.__red == 1

    def is_one_nine(self):
        return self.is_number() and self.__value in (1, 9)

    def __lt__(self, other):
        assert isinstance(other, Tile)
        if self.__category != other.__category:
            return self.__category < other.__category
        elif self.__value != other.__value:
            return self.__value < other.__value
        else:
            return self.__red < other.__red

    def __gt__(self, other):
        return not (self < other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.is_red():
            return f'\033[1;31m{Tile.number_graph[self.__category][5]}\033[0m'
        else:
            return Tile.number_graph[self.__category][self.__value]

    def __add__(self, other: int):
        # This function is for meld calculation. Not dora calculation
        assert self.is_number()
        new_value = self.__value + other
        # assert 1 <= new_value <= 9
        if new_value < 1 or new_value > 9:
            raise ValueError("add exceed boundary")
        return Tile(self.__category, new_value, self.__red)

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        """红宝牌不纳入考虑"""
        return self.__category == other.__category and self.__value == other.__value

    def is_same_category(self, other):
        return self.__category == other.__category


if __name__ == "__main__":
    tiles = Tile.generate_all_136_tiles()
    random.shuffle(tiles)
    tiles.sort()
    print(tiles)
