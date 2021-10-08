from tile import chi, peng, minggang, angang, jiagang


class Meld:
    """
    副露的实现
    """

    def __init__(self, tiles, meld_type, offer_flag, offer_player):
        """
        生成一个副露
        :param tiles: 用来组成这张副露的所有牌
        :param meld_type: 副露的种类
        :param offer_flag: 用来标记tiles中哪一张是鸣的牌，使用序号标记，第一张是0。
        :param offer_player: 提供牌的玩家的座次，使用当前局面的绝对编号，和东南西北对应
                            如果是吃，只能是上家；
                            如果是碰，可以是其他三家；
                            如果是杠，可以是其他三家；
                            如果是暗杠，只能是自己提供。
                            如果是加杠，offer_player代表碰牌来自哪一家
        """
        if meld_type == chi:
            if len(tiles) != 3:
                raise ValueError("吃生成的副露不是三张")
            tile1, tile2, tile3 = tiles
            if not (tile1 + 1 == tile2 and tile2 + 1 == tile3):
                raise ValueError("吃的牌无法组成顺子")

        if meld_type == peng:
            if len(tiles) != 3:
                raise ValueError("碰生成的副露不是三张")
            tile1, tile2, tile3 = tiles
            if not (tile1 == tile2 and tile2 == tile3):
                raise ValueError("碰的牌不相同")

        if meld_type in (minggang, angang):
            if len(tiles) != 3:
                raise ValueError("杠生成的副露不是三张")
            if not all(x == tiles[0] for x in tiles):
                raise ValueError("杠的牌不相同")

        if meld_type == jiagang:
            raise ValueError("不能直接生成加杠!")

        self.tiles = tiles[:]
        self.meld_type = meld_type
        self.offer_player = offer_player
        self.offer_flag = offer_flag

    def promote(self, tile):
        """
        将碰变成加杠
        """
        if self.meld_type != peng:
            raise ValueError("不是碰不能加杠")
        if tile != self.tiles[0]:
            raise ValueError("加杠的牌种类不对")
        self.tiles.append(tile)
        self.meld_type = jiagang
        # 加杠不会改变offer_flag也不会改变offer_player
