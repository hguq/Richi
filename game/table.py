import random
from copy import deepcopy
from typing import List

from agent import Agent
from game import Tile
from player import Player


class View:
    """
    玩家所能够看到的view
    """

    def __init__(self,
                 player_id,
                 action_id,
                 action,
                 action_tile,
                 hand_tiles,
                 all_player_melds,
                 all_player_discard_tiles,
                 all_player_point_bar,
                 east_or_south,
                 field_number,
                 n_pon,
                 field_wind,
                 banker,
                 dora_indicator,
                 n_wall_tiles,
                 discard_tiles,
                 n_richi_bar,
                 richi_flag,
                 yifa_flag,
                 lianglizhi_flag):
        self.player_id = player_id
        self.action_id = action_id
        self.action = action
        self.action_tile = action_tile
        self.hand_tiles = hand_tiles
        self.all_player_melds = all_player_melds
        self.all_player_discard_tiles = all_player_discard_tiles
        self.all_player_point_bar = all_player_point_bar
        self.east_or_south = east_or_south
        self.field_number = field_number
        self.n_pon = n_pon
        self.field_wind = field_wind
        self.banker = banker
        self.dora_indicator = dora_indicator
        self.n_wall_tiles = n_wall_tiles
        self.discard_Tiles = discard_tiles
        self.n_richi_bar = n_richi_bar
        self.richi_flag = richi_flag
        self.yifa_flag = yifa_flag
        self.lianglizhi_flag = lianglizhi_flag


class Table:
    """
    Table implementation
    桌子包含一个顺序。
    从12点钟方向开始，顺时针方向，依次是0,1,2,3
    Player和Agent放在哪个位置，就坐在哪个位置
    """

    def __init__(self):
        self.agents: List[Agent] = []  # bot主体，必须是Agent类的实例
        self.players: List[Player] = []  # 用于模拟对局的Player，必须是Player的实例

        self.east_or_south: str = "east"  # 指示是东风局或者南风局。用"east"标注东风局，用"south"标注南风局
        self.field_wind: str = "east"  # 场风
        self.field_number: int = 3  # 指示第几局，比如东风第三局，field_wind是"east"，field_number是3，从1开始
        self.n_pon: int = 0  # 本场数，起始应该是0
        self.banker: int = 0  # 当前局的庄家，对应的Player的wind应该是东风

        self.lingshang_tiles: List[Tile] = []  # 岭上牌，初始化的时候共四张
        self.lingshang_discard_tiles: List[Tile] = []  # 由于开杠，导致牌墙最后一张被移入王牌堆，无法被摸到的牌。初始化的时候是空列表

        self.dora_indicator: List[Tile] = []  # 宝牌指示牌，初始化的时候应当有5张
        self.inside_dora_indicator: List[Tile] = []  # 里宝牌指示牌，初始化的时候应该有5章
        self.dora_indicator_flag: List[bool] = []  # 宝牌指示牌是否被翻开

        self.wall_tiles: List[Tile] = []  # 用于摸牌的牌墙
        self.discard_tiles: List[Tile] = []  # 每一家弃掉的牌，应当是列表类型，一个列表中包含四个列表，依次排布
        self.n_richi_bar: int = 0  # 除了场上的立直棒，由于流局累积的立直棒数目
        self.richi_flag: List[bool] = []  # 标志每一家是否立直。
        self.yifa_flag: List[bool] = []  # 标记一发
        self.lianglizhi_flag: List[bool] = []  # 标记两立直，如果第一巡有人鸣牌或者超过了第一巡，将flag重置为False

    def player_view(self, player_id, action_id, action, action_tile):
        """
        从玩家角度看到的牌桌
        :player_id: 指示是从哪个player视角看到的
        :state: 指示当前的状态
            以下几种情况
            1. 自己摸了一张牌
            2. 自己副露了牌
            3. 有人打出了牌
            4. 有人加杠或者暗杠


            1. （自己id，摸牌，摸的牌）
            2. （自己id，吃或者碰或者杠，如果是杠那么岭上牌）
            3. （其他人id，打出牌，打出的牌）
            4. （其他人id，加杠或者暗杠，杠的牌）

        :return: encoded information
        """
        return View(
            player_id=player_id,
            hand_tiles=deepcopy(self.players[player_id].hand_tiles),
            action_id=action_id,
            action=action,
            action_tile=action_tile,
            all_player_melds=[player.melds for player in self.players],
            all_player_discard_tiles=[player.discard_tiles for player in self.players],
            all_player_point_bar=[player.point_bar for player in self.players],

            east_or_south=self.east_or_south,
            field_number=self.field_number,
            n_pon=self.n_pon,
            field_wind=self.field_wind,
            banker=self.banker,
            dora_indicator=[tile for tile, flag in zip(self.dora_indicator, self.dora_indicator_flag) if flag],
            n_wall_tiles=deepcopy(self.wall_tiles),
            discard_tiles=deepcopy(self.discard_tiles),
            n_richi_bar=self.n_richi_bar,
            richi_flag=deepcopy(self.richi_flag),
            yifa_flag=deepcopy(self.yifa_flag),
            lianglizhi_flag=deepcopy(self.lianglizhi_flag)
        )

    def single_round(self, agents: list):
        """
        简单的一局，需要完成每家配牌，摸打循环，返回赢家以及赢得点棒数
        需要在上一层中确定当前场风，当前场数，当前庄家，确定agent的座次
        :param agents: a list of agents
        """
        # TODO: Player需要在上一次层创建
        # 分发所有的牌，并且准备好所有人的手牌，初始化岭上牌
        self.dispence_tiles()
        # TODO: 点棒的分发需要在上一层完成
        # 进入摸打循环

    def settlement(self, result, player_id):
        raise NotImplementedError

    def play_loop(self, player_id, draw=True, lingshang=False):
        """
        一次摸打循环

        如果以一次摸牌开始，可能结果有:
        1. 自摸: 在可以胡牌的情况下直接自摸，结束
           这个可能符合岭上，因为岭上牌摸牌也会进入这个play_loop
        2. 流局: 第一次摸牌，九种九牌，结束
        3. 开暗杠: 摸到的牌可以开一次暗杠
        4. 立直: 打出立直棒宣布立直
        5. 切牌

        开暗杠会导致三种结果:
        1. 开杠成功，摸一张牌，再次进入play_loop
        2. 有人抢杠国士，荣胡，结束

        立直或者切牌会导致四种结果：
        1. 荣胡: 让其他一家胡牌，结束
        2. 流局: 结束
                四风连打，
                或者当前已经翻开了四张宝牌指示牌，打出之后无人胡牌，导致四杠散了
                或者打出了最后一张牌并且没有人胡牌，普通的荒牌，这种情况需要结算流局满贯
        3. 副露: 让其他一家副露，进入其他人的回合并且不摸牌，再次进入play_loop
        4. 无事发生，变更到下一个人的回合，再次进入play_loop

        如果有人荣胡或者流局，那么立直不成功，不需要放立直棒

        有人副露会导致以下可能:
        1. 变更到下一个玩家的回合，再次进入其他人的play_loop
        2. 杠牌摸一张岭上牌，变更到下一个玩家的回合，进入其他人的play_loop
        2. 有人抢杠和牌，结束

        所有的结束都会进入调用结算的函数。

        :param player_id: 当前的进行动作的agent的编号
        :param draw: 是否摸牌，因为如果是由于副露进入当前玩家回合，是不摸牌的。
                     一个例外是如果杠牌，那么在进入这个人的回合之前，先把岭上牌放进去
        :param lingshang: 指示摸牌是否是岭上牌
        """
        cur_player: Player = self.players[player_id]
        cur_agent: Agent = self.agents[player_id]
        if draw:
            # 如果摸牌，从牌山取出一张放入Player的手牌
            # 摸牌顺序是弹出最后一张，实现起来代价低
            draw_tile = self.wall_tiles.pop()
            cur_player.hand_tiles.append(draw_tile)
            response = cur_agent.draw_response(draw_tile, lingshang=lingshang)
            if response[0] == "zimo":
                if self.can_zimo(player_id):
                    # TODO: self.settlement()
                    return
                else:
                    raise ValueError(f"玩家{player_id}诈和自摸")
            elif response[0] == "liuju":
                # TODO: 检查是否可以九种九牌流局
                if ...:
                    # TODO: self.settlement()
                    return
                else:
                    raise ValueError(f"玩家{player_id}错误九种九牌流局")
            elif response[0] == "angang":
                # TODO: 检查是否可以暗杠
                if ...:
                    # TODO: self.settlement()
                    return
                else:
                    raise ValueError(f"玩家{player_id}非法开暗杠")
            elif response[0] == "lizhi":
                # TODO: 判断是否可以立直
                if ...:
                    # TODO: self.settlement()
                    return
                else:
                    raise ValueError(f"玩家{player_id}非法立直")
            elif response[0] == "qiepai":
                # TODO: 是不是response[1]
                cur_player.discard_tiles.append(response[1])

    def south_round(self):
        """
        南风局
        """
        raise NotImplementedError

    def can_zimo(self, player_id):
        """
        判断是否能够自摸
        :return: 能否自摸，如果可以，同时返回胡牌种类列表和各家需要支付的点数
        """
        raise NotImplementedError

    def tie(self):
        """
        流局
        判断每家是否听牌。
        如果庄家听牌，则本场数+1。
        如果有人流局满贯，优先结算流局满贯
        如果庄家没有听牌，闲家也没有听牌，则本场数加1，且进入下一轮。
        如果庄家没有听牌，闲家听牌，则本场数+1，进入下一轮，且罚符。
        进入下一轮的时候，如果场次到4，那么东风局直接结束，南风局判断是否进入南风。
        :return:
        """

    # 南风局的话，如果场数为4

    def set_seat(self):
        """
        随机设置agent的座次
        这个座次直接和Player绑定
        """
        random.shuffle(self.agents)

    def dispence_point_bars(self):
        """分发点棒"""
        for player in self.players:
            player.point_bar = 25000

    def next_banker(self):
        """一局结束之后，闲家胡牌或者流局情况下庄家未听牌，本场数+1，庄家轮换至下一家"""

    def dispence_tiles(self):
        """
        在一个单局的开始，准备好桌面上的所有的牌
        """
        self.wall_tiles = Tile.generate_all_136_tiles()
        random.shuffle(self.wall_tiles)
        for ind, player in enumerate(self.players):
            player.hand_tiles = self.wall_tiles[ind * 13:(ind + 1) * 13]  # draw 13 tiles
            player.melds = []

        self.wall_tiles = self.wall_tiles[13 * 4:]

        # 准备王牌堆
        self.lingshang_tiles, self.wall_tiles = self.wall_tiles[-4:], self.wall_tiles[:-4]
        self.lingshang_discard_tiles = []
        self.dora_indicator, self.wall_tiles = self.wall_tiles[-5:], self.wall_tiles[:-5]
        self.inside_dora_indicator, self.wall_tiles = self.wall_tiles[-5:], self.wall_tiles[:-5]
        self.dora_indicator_flag = [True, False, False, False, False]
        self.discard_tiles = []

    def init_richi_bar(self):
        """
        在一局的开始，重置立直棒
        """
        self.n_richi_bar = 0
        self.richi_flag = [False] * 4

    def collect_richi_bar(self):
        """
        流局时收集所有人的立直棒，重置所有人的立直标记位
        """
        self.n_richi_bar += sum(self.richi_flag)
        self.richi_flag = [False] * 4

    def open_new_dora_indicator(self):
        """
        打开新的宝牌指示牌，并且将河底牌移入王牌堆
        """
        if all(self.dora_indicator_flag):
            raise ValueError("All dora indicators have already opened!")
        self.dora_indicator_flag = [True] + self.dora_indicator_flag[:-1]

        # 将原本的河底牌移入王牌堆
        self.lingshang_discard_tiles.append(self.wall_tiles.pop(-1))
