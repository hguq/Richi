class Agent:
    """
    All methods must be implemented
    每个函数都会有一个state编码当前player视角看到的桌面状态，这个状态是执行完操作之后的
    比如摸牌的response，在调用这个函数之前，摸的手牌已经加入到state中了
    """

    def draw_response(self, state, tile, lingshang=False):
        """
        摸牌之后的response
        :lingshang: 指示这张牌是否是岭上牌
        :return: 二元组，第一个指示操作，第二个指示操作对象
        """
        # 自摸? 暗杠? 立直? 流局? 切牌?
        raise NotImplementedError

    def discard_response(self, state, tile):
        """
        有人切牌之后的response
        :return: 二元组，第一个指示操作，第二个指示操作对象
        """
        # 荣? 副露? 不作任何反应?
        raise NotImplementedError

    def meld_response(self, state, meld):
        """
        有人杠牌之后是否抢杠？
        :return: True or False
        """
        raise NotImplementedError
