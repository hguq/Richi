from copy import deepcopy
from typing import List, Dict

from game import View
from game.tile import *

yaojiu_list = (
    Tile(man, 1, 0),
    Tile(man, 9, 0),
    Tile(pin, 1, 0),
    Tile(pin, 9, 0),
    Tile(suo, 1, 0),
    Tile(suo, 9, 0),
    Tile(wind, 0, 0),
    Tile(wind, 1, 0),
    Tile(wind, 2, 0),
    Tile(wind, 3, 0),
    Tile(honor, 0, 0),
    Tile(honor, 1, 0),
    Tile(honor, 2, 0)
)


def list2dict(tiles):
    """
    将牌的列表转换成牌到数量的字典
    :return:
    """
    d = dict()
    for tile in tiles:
        if tile in d.keys():
            d[tile] += 1
        else:
            d[tile] = 1
    return d


def is_normal_form(tiles: List[Tile]):
    """
    判断是否满足麻将的普通牌型，四个面子，一个雀头
    副露的牌可以不传到这里面，因为副露直接作为面子即可
    只需要判断剩下的是否要么是面子，要么是刻子
    :param tiles: 手牌（不包含副露）
    :return: Bool 是否满足普通规则
    """
    return is_normal_form_helper(list2dict(tiles))


def is_seven_pair_form(tiles: List[Tile]):
    """
    判断是否可以满足七对子型，必须是14章牌
    :param tiles:
    :return:
    """
    if len(tiles) != 14:
        return False
    for i in range(7):
        if tiles[2 * i] != tiles[2 * i + 1]:
            return False
    return True


def normal_form_split(tiles: List[Tile]):
    """
    枚举所有可能的普通型的分组
    :param tiles:
    :return:
    """
    d = list2dict(tiles)
    return normal_form_split_helper(d, (), False)


def normal_form_split_helper(tiles: Dict[Tile, int], tile_packs, has_pair=False):
    """
    帮助函数
    :param tiles:
    :param tile_packs:
    :param has_pair
    :return:
    """
    if not tiles:
        yield tile_packs
        # 所有的牌都用光了，完全分割完毕

    # 尝试削减雀头:
    if not has_pair:
        for tile, n in tiles.items():
            if n >= 2:
                new_tiles = deepcopy(tiles)
                new_tiles[tile] -= 2
                if new_tiles[tile] == 0:
                    new_tiles.pop(tile)
                    for pack in normal_form_split_helper(new_tiles, tile_packs + ((tile, tile),), True):
                        yield pack

    # 尝试削减顺子
    for tile, n in tiles.items():
        try:
            tile_1 = tile + 1
            tile_2 = tile + 2
            if tile_1 in tiles.keys() and tile_2 in tiles.keys():
                new_tiles = deepcopy(tiles)
                for x in [tile, tile_1, tile_2]:
                    new_tiles[x] -= 1
                    if new_tiles[x] == 0:
                        new_tiles.pop(x)
                for pack in normal_form_split_helper(new_tiles, tile_packs + ((tile, tile_1, tile_2),), has_pair):
                    yield pack
        except ValueError:
            continue

    # 尝试消减刻子
    for tile, n in tiles.items():
        if n >= 3:
            new_tiles = deepcopy(tiles)
            new_tiles[tile] -= 3
            if new_tiles[tile] == 0:
                new_tiles.pop(tile)
            for pack in normal_form_split_helper(new_tiles, tile_packs + ((tile, tile, tile),), has_pair):
                yield pack


def is_normal_form_helper(tiles: Dict[Tile, int], has_pair=False):
    """
    使用字典格式判断，用于削减面子或者雀头
    由于这个函数是递归的，所以需要拿出来
    :param has_pair: 在递归过程中是否已经生成过雀头了
    :param tiles:
    :return:
    """
    if len(tiles) == 0:
        return True
    # 尝试削减雀头
    if not has_pair:
        for tile, n in tiles.items():
            if n >= 2:
                new_tiles = deepcopy(tiles)
                new_tiles[tile] -= 2
                if new_tiles[tile] == 0:
                    new_tiles.pop(tile)
                if is_normal_form_helper(new_tiles, has_pair=True):
                    return True

    # 尝试削减顺子
    for tile, n in tiles.items():
        try:
            tile_1 = tile + 1
            tile_2 = tile + 2
            if tile_1 in tiles.keys() and tile_2 in tiles.keys():
                new_tiles = deepcopy(tiles)
                for x in [tile, tile_1, tile_2]:
                    new_tiles[x] -= 1
                    if new_tiles[x] == 0:
                        new_tiles.pop(x)
                if is_normal_form_helper(new_tiles):
                    return True
        except ValueError:
            continue

    # 尝试消减刻子
    for tile, n in tiles.items():
        if n >= 3:
            new_tiles = deepcopy(tiles)
            new_tiles[tile] -= 3
            if new_tiles[tile] == 0:
                new_tiles.pop(tile)
            if is_normal_form_helper(new_tiles):
                return True

    return False


def is_guoshi_form(tiles: List[Tile]):
    """
    判断是否满足国士牌型，必须是14章牌
    :param tiles:
    :return:
    """
    d = list2dict(tiles)
    if len(tiles) != 14:
        return False

    for yaojiu in yaojiu_list:
        if yaojiu not in d.keys():
            return False


def normal_form_wait_list(tiles: List[Tile]):
    """
    判断普通牌型在13章牌的时候听哪些牌
    :param tiles: 手牌
    :return: 听牌
    """
    d = list2dict(tiles)
    return normal_form_wait_list_helper(d, has_pair=False)


def normal_form_wait_list_helper(tiles: Dict[Tile, int], has_pair=False):
    """
    用于递归计算的帮助函数
    :param has_pair: 在递归过程中是否已经生成过雀头了
    :param tiles: 从牌映射到牌的数量
    :return: 听牌列表
    """
    if len(tiles) == 1:
        # 有可能听雀头
        tile, _ = tiles.keys()
        if tiles[tile] == 1:
            assert has_pair
            return {tile}
    elif len(tiles) != 2:
        tile1, tile2, _ = sorted(tiles.keys())
        if tiles[tile1] == 1 and tiles[tile2] == 1:
            if tile1.is_same_category(tile2):
                # 剩下一个搭子
                if tile1 + 1 == tile2:
                    if tile1 in yaojiu_list:
                        return {tile2 + 1}
                    elif tile2 in yaojiu_list:
                        return {tile1 - 1}
                    else:
                        return {tile1 - 1, tile2 + 1}
                elif tile1 + 2 == tile2:
                    return {tile1 + 1}

    result = {}

    # 尝试削减雀头
    if not has_pair:
        for tile, n in tiles.items():
            if n >= 2:
                new_tiles = deepcopy(tiles)
                new_tiles[tile] -= 2
                if new_tiles[tile] == 0:
                    new_tiles.pop(tile)
                result |= normal_form_wait_list_helper(new_tiles, has_pair=True)

    # 尝试削减顺子
    for tile, n in tiles.items():
        try:
            tile_1 = tile + 1
            tile_2 = tile + 2
            if tile_1 in tiles.keys() and tile_2 in tiles.keys():
                new_tiles = deepcopy(tiles)
                for x in [tile, tile_1, tile_2]:
                    new_tiles[x] -= 1
                    if new_tiles[x] == 0:
                        new_tiles.pop(x)
                result |= normal_form_wait_list_helper(new_tiles)
        except ValueError:
            continue

    # 尝试消减刻子
    for tile, n in tiles.items():
        if n >= 3:
            new_tiles = deepcopy(tiles)
            new_tiles[tile] -= 3
            if new_tiles[tile] == 0:
                new_tiles.pop(tile)
            result |= normal_form_wait_list_helper(new_tiles)

    return result


def seven_pair_wait_list(tiles: List[Tile]):
    """
    判断七对子型听牌
    :param tiles: 手牌
    :return:
    """
    if len(tiles) != 13:
        # 如果不是门清，那么无法七对子听牌
        return {}

    d = list2dict(tiles)
    if len(d) == 7:
        # 有七种牌，则七对子听牌
        for k, v in d.items():
            if v == 1:
                return {k}

    return {}


def guoshi_wait_list(tiles: List[Tile]):
    """
    判断国士听牌
    :param tiles: 手牌
    :return: 国士听牌的种类
    """
    if len(tiles) != 13:
        # 如果不是门清，则无法国士
        return {}

    if any(x not in yaojiu_list for x in tiles):
        # 如果有任何一张牌不是幺九牌，则不是国士
        return {}

    d = list2dict(tiles)

    if len(d) == 13:
        # 国士十三面
        return set(yaojiu_list)
    elif len(d) == 12:
        # 国士
        for yaojiu in yaojiu_list:
            if yaojiu not in d.keys():
                return {yaojiu}
    else:
        return {}


"""
如何判断一个人胡牌？
1. 是否满足听牌牌型
    1.1 是否满足普通听牌牌型
    1.2 是否满足七对子听牌
    1.3 是否满足国士听牌

2. 将所有听牌合并到一起，供牌有几种情况
    2.1 自摸
        2.1.1 门前清自摸
        2.1.2 岭上开花
        2.1.3 海底捞月
        2.1.4 普通自摸
        
    2.2 荣胡
        2.2.1 河底捞鱼
        2.2.2 普通荣胡
        
    2.3 抢杠
        2.3.1 抢加杠
        2.3.2 国士抢暗杠

3. 判断是否满足胡牌牌型

4. 判断是否有役，将役累加计算番数，并且得到合理的划分

5. 在划分的基础上计算符数，重新分配点棒
        
    为了判断这些情况，而不是从参数列表中传入，牌桌的编码需要包含这些信息"""


# 下面通过玩家的视角判断是否满足胡牌条件，即有役
# 在调用下面这些函数之前，需要先判断是否满足听牌条件
def is_richi(view: View):
    """
    是否立直胡牌
    :param view: 牌桌的view
    :return:
    """
    player_id = view.player_id
    return view.richi_flag[player_id]


def is_duanyao(view: View):
    """
    :param view: 牌桌的view
    :return:
    """
    last_tile = view.action_tile
    if last_tile in yaojiu_list:
        return False
    for tile in view.hand_tiles:
        if tile in yaojiu_list:
            return False
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        for tile in meld.tiles:
            if tile in yaojiu_list:
                return False
    return True


def is_menqianqingzimo(view: View) -> object:
    """
    判断是否门前清自摸
    :param view:
    :return:
    """
    # 有两种情况
    # 1. 自己存在暗杠
    # 2. 自己没有副露
    melds = view.all_player_melds[view.player_id]
    if not (view.action_id == view.player_id and view.action == mo):
        return False
    return len(view.hand_tiles) == 13 or all(meld.meld_type == angang for meld in melds)


def is_yipai_zifeng(view: View):
    """
    判断是不是自风刻
    :param view:
    :return:
    """
    zifeng = Tile(wind, view.player_id, 0)
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if zifeng in meld.tiles:
            return True
    cnt = 0
    for tile in view.hand_tiles:
        if tile == zifeng:
            cnt += 1
    return cnt == 3


def is_yipai_changfeng(view: View):
    """
    判断是不是场风刻
    :param view:
    :return:
    """
    changfeng = Tile(wind, view.field_wind, 0)
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if changfeng in meld.tiles:
            return True
    cnt = 0
    for tile in view.hand_tiles:
        if tile == changfeng:
            cnt += 1
    return cnt == 3


def is_yipai_honor_white(view: View):
    """
    判断是不是三元刻白
    :param view:
    :return:
    """
    white = Tile(honor, 0, 0)
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if white in meld.tiles:
            return True
    cnt = 0
    for tile in view.hand_tiles:
        if tile == white:
            cnt += 1
    return cnt == 3


def is_yipai_honor_fortune(view: View):
    """
    判断是不是三元刻中
    :param view:
    :return:
    """
    fortune = Tile(honor, 0, 0)
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if fortune in meld.tiles:
            return True
    cnt = 0
    for tile in view.hand_tiles:
        if tile == fortune:
            cnt += 1
    return cnt == 3


def is_yipai_honor_center(view: View):
    """
    判断是不是三元刻中
    :param view:
    :return:
    """
    center = Tile(honor, 0, 0)
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if center in meld.tiles:
            return True
    cnt = 0
    for tile in view.hand_tiles:
        if tile == center:
            cnt += 1
    return cnt == 3


def pack_is_string(pack):
    """
    判断一个pack是不是顺子
    :param pack:
    :return:
    """
    return len(pack) == 3 and pack[0] + 2 == pack[1] + 1 == pack[2]


def pack_is_three(pack):
    """
    判断一个pack是不是刻子
    :param pack:
    :return:
    """
    return len(pack) == 3 and pack[0] == pack[1] == pack[2]


def pack_is_pair(pack):
    """
    判断一个pack是不是雀头
    :param pack:
    :return:
    """
    return len(pack) == 2 and pack[0] == pack[1]


def is_pinghu(view: View):
    """
    判断是不是平和
    :param view:
    :return:
    """
    melds = view.all_player_melds[view.player_id]
    if melds:
        return False  # 平和不能够有任何副露
    for split_form in normal_form_split(view.hand_tiles):
        flag = True
        for pack in split_form:
            if pack_is_three(pack):
                flag = False
                break
        if flag:
            return True
    return False


def is_yibeikou(view: View):
    """
    判断是不是一杯口
    :param view:
    :return:
    """
    if view.all_player_melds[view.player_id]:
        return False  # 一杯口不能有副露
    for split_form in normal_form_split(view.hand_tiles + [view.action_tile]):
        string_packs = (pack for pack in split_form if pack_is_string(pack))
        for pack1, index1 in enumerate(string_packs):
            for pack2, index2 in enumerate(string_packs):
                if index1 != index2 and pack1 == pack2:
                    return True
    return False


def is_qianggang(view: View):
    """
    判断是不是抢杠
    :param view:
    :return:
    """
    if view.action_id == view.player_id or view.action != jiagang:
        return False
    # 必须是别家杠牌
    # 国士的计算不放这里，所以没有暗杠
    return True


def is_lingshangkaihua(view: View):
    """
    判断是不是岭上开花
    :param view:
    :return:
    """
    if view.action_id != view.player_id or view.action not in (jiagang, angang, minggang):
        return False
    return True


def is_haidimoyue(view: View):
    """
    判断是不是海底摸月
    :param view:
    :return:
    """
    if view.action_id != view.player_id or view.action != mo:
        return False
    return view.n_wall_tiles == 0


def is_hedilaoyu(view: View):
    """
    判断是不是河底摸鱼
    :param view:
    :return:
    """
    if view.action_id == view.player_id or view.action != qie:
        return False
    return view.n_wall_tiles == 0


def is_yifa(view: View):
    """
    判断是不是一发
    :param view:
    :return:
    """
    return view.yifa_flag[view.player_id] and view.richi_flag[view.player_id]


def is_shuanglizhi(view: View):
    """
    判断是不是两立直
    :param view:
    :return:
    """
    return view.lianglizhi_flag[view.player_id]


def is_sansetongke(view: View):
    """
    判断是不是三色同刻
    :param view:
    :return:
    """
    # 将刻子的牌映射到数
    for split_form in normal_form_split(view.hand_tiles + [view.action_tile]):
        pack_flag_tile = []
        for pack in split_form:
            if pack_is_three(pack):
                pack_flag_tile.append(pack[0])
        # 从1到9，看是否存在三种数牌
        for i in range(1, 10):
            cnt = 0
            for tile in pack_flag_tile:
                if tile.is_number() and tile.__value == i:
                    cnt += 1
            if cnt == 3:
                return True
    return False


def is_sangangzi(view: View):
    """
    判断是不是三杠子
    :param view:
    :return:
    """
    melds = view.all_player_melds[view.player_id]
    if len(melds) < 3:
        return False
    cnt = 0
    for meld in melds:
        if meld.meld_type in (minggang, angang, jiagang):
            cnt += 1
    if cnt == 3:
        return True


def is_duidui(view: View):
    """
    判断是不是对对
    :param view:
    :return:
    """
    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type != peng:
            return False
    # 判断所有的手牌是不是可以划分成雀头和刻子
    all_tiles = view.hand_tiles + [view.action_tile]
    d = list2dict(all_tiles)
    # 去掉雀头之后，必定只剩下刻子
    pair_flag = False
    for tile, n in d.items():
        if n == 2:
            if pair_flag:
                return False
            else:
                pair_flag = True
        else:
            if tile != 3:
                return False
    return True


def is_sananke(view: View):
    """
    判断是不是三暗刻
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles[:]
    if view.action == mo and view.action_id == view.player_id:
        all_tiles.append(view.action_tile)

    # 判断手上的牌能不能组成三个暗刻
    for split_form in normal_form_split(all_tiles):
        cnt = 0
        for pack in split_form:
            if pack_is_three(pack):
                cnt += 1
        if cnt >= 3:
            return True


def is_xiaosanyuan(view: View):
    """
    判断是不是小三元
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    # 中，发，白，其中有一种是两张的雀头，另外两种都有刻子
    # 输出三元牌的对子和刻子的数目，分别应该是1和2
    meld_three_cnt = 0

    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type is peng and meld.tiles[0].is_honor():
            meld_three_cnt += 1

    for split_form in normal_form_split(all_tiles):
        hand_pair_cnt = 0
        hand_three_cnt = 0
        for pack in split_form:
            if pack_is_pair(pack) and pack[0].is_honor():
                hand_pair_cnt += 1
            elif pack_is_three(pack) and pack[0].is_honor():
                hand_three_cnt += 1
        if hand_pair_cnt == 1 and meld_three_cnt + hand_three_cnt == 2:
            return True
    return False


def is_hunlaotou(view: View):
    """
    判断是不是混老头
    :param view:
    :return:
    """
    # 必须全部划分为刻子和雀头，全部是幺九牌，并且必须要有19数牌和字牌
    # 由于一定符合和牌牌型，手牌只需要检查是否都是幺九牌就可以了
    char_flag = False
    one_nine_flag = False
    all_tiles = view.hand_tiles + [view.action_tile]
    for tile in all_tiles:
        if tile.is_number():
            if tile.__value in (1, 9):
                one_nine_flag = True
            else:
                return False
        elif tile.is_character():
            char_flag = True
    if not char_flag or not one_nine_flag:
        return False

    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type != peng:
            return False
        tile = melds.tiles[0]
        if tile.is_number():
            if not tile.is_one_nine():
                return False
            one_nine_flag = True
        else:
            char_flag = True
    return one_nine_flag and char_flag


def is_seven_pair(view: View):
    """
    判断是不是七对子
    :param view:
    :return:
    """
    # 二杯口优先级高于七对子
    if is_erbeikou(view):
        return False
    # 如果是自摸的话，14张牌判断字典大小就可以
    if view.action == mo and view.player_id == view.action_id:
        d = list2dict(view.hand_tiles)
        return len(d) == 7 and all(x == 2 for x in d.values())

    # 如果是荣胡的话，判断动作牌是否在七对wait_list里
    else:
        return len(view.hand_tiles) == 13 and view.action_tile in seven_pair_wait_list(view.hand_tiles)


def is_hunquandai(view: View):
    """
    判断是否混全带幺
    :param view:
    :return:
    """
    all_melds = view.all_player_melds[view.player_id]
    all_tiles = view.hand_tiles + [view.action_tile]

    # 至少分割出一组顺子，否则变成混老头
    string_flag = False

    for meld in all_melds:
        if meld.meld_type == chi:
            string_flag = True
            # 顺子必须是123或者789
            value = tuple(sorted(tile.__value for tile in meld.tiles))
            if value not in ((1, 2, 3), (7, 8, 9)):
                return False
        else:
            # 必须是幺九牌刻子
            if meld.tiles[0] not in yaojiu_list:
                return False

    for split_form in normal_form_split(all_tiles):
        for pack in split_form:
            if pack_is_pair(pack):
                if pack[0] not in yaojiu_list:
                    return False
            elif pack_is_string(pack):
                string_flag = True
                value = tuple(sorted(tile.__value for tile in pack))
                if value not in ((1, 2, 3), (7, 8, 9)):
                    return False
            elif pack_is_three(pack):
                if pack[0] not in yaojiu_list:
                    return False

    return string_flag


def is_yiqitongguan(view: View):
    """
    判断是否是一气通贯
    :param view:
    :return:
    """

    melds = view.all_player_melds[view.player_id]
    all_tiles = view.hand_tiles + [view.action_tile]
    for t in (man, pin, suo):
        flag123 = False
        flag456 = False
        flag789 = False

        for meld in melds:
            if meld.meld_type == chi and meld.tiles[0].__category == t:
                values = tuple(sorted(tile.__value for tile in meld.tiles))
                if values == (1, 2, 3):
                    flag123 = True
                elif values == (4, 5, 6):
                    flag456 = True
                elif values == (7, 8, 9):
                    flag789 = True

        for split_form in normal_form_split(all_tiles):
            for pack in split_form:
                if pack_is_string(pack) and pack[0].__category == t:
                    values = tuple(sorted(tile.__value for tile in pack))
                    if values == (1, 2, 3):
                        flag123 = True
                    elif values == (4, 5, 6):
                        flag456 = True
                    elif values == (7, 8, 9):
                        flag789 = True

        if flag123 and flag456 and flag789:
            return True
    return False


def is_sansetongshun(view: View):
    """
    判断是否三色同顺
    :param view:
    :return:
    """
    # 将顺子的牌映射到数
    for split_form in normal_form_split(view.hand_tiles + [view.action_tile]):
        pack_flag_tile = []
        for pack in split_form:
            if pack_is_string(pack):
                pack_flag_tile.append(tuple(sorted(pack))[0])
        # 从1到7，看是否存在三种数牌
        for i in range(1, 7):
            cnt = 0
            for tile in pack_flag_tile:
                if tile.is_number() and tile.__value == i:
                    cnt += 1
            if cnt == 3:
                return True
    return False


def is_erbeikou(view: View):
    """
    判断是不是二杯口
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    if len(all_tiles) != 14:
        return False
    for split_form in normal_form_split(all_tiles):
        faces = sorted(filter(lambda x: len(x) == 3, split_form))
        if faces[0] == faces[1] and faces[2] == faces[3]:
            return True

    return False


def is_chunquandai(view: View):
    """
    判断是不是纯全带
    :param viwe:
    :return:
    """
    all_melds = view.all_player_melds[view.player_id]
    all_tiles = view.hand_tiles + [view.action_tile]

    # 必须全部都是数牌
    for tile in all_tiles:
        if tile.is_character():
            return False

    for meld in all_melds:
        for tile in meld.tiles:
            if tile.is_character():
                return False

    # 至少分割出一组顺子，否则变成清老头
    string_flag = False

    for meld in all_melds:
        if meld.meld_type == chi:
            string_flag = True
            # 顺子必须是123或者789
            value = tuple(sorted(tile.__value for tile in meld.tiles))
            if value not in ((1, 2, 3), (7, 8, 9)):
                return False
        else:
            # 必须是19刻子
            if not meld.tiles[0].is_one_nine():
                return False

    for split_form in normal_form_split(all_tiles):
        for pack in split_form:
            if pack_is_pair(pack):
                if not pack[0].is_one_nine():
                    return False
            elif pack_is_string(pack):
                string_flag = True
                value = tuple(sorted(tile.__value for tile in pack))
                if value not in ((1, 2, 3), (7, 8, 9)):
                    return False
            elif pack_is_three(pack):
                if not pack[0].is_one_nine():
                    return False

    return string_flag


def is_hunyise(view: View):
    """
    判断是不是混一色
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    all_melds = view.all_player_melds[view.player_id]

    number_category = None
    char_flag = False

    for tile in all_tiles:
        if tile.is_number():
            if number_category is None:
                number_category = tile.__category
            elif tile.__category != number_category:
                return False
        else:
            char_flag = True

    for meld in all_melds:
        for tile in meld.tiles:
            if tile.is_number():
                if number_category is None:
                    number_category = tile.__category
                elif tile.__category != number_category:
                    return False
            else:
                char_flag = True

    return char_flag


def is_qingyise(view: View):
    """
    判断是不是清一色
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    all_melds = view.all_player_melds[view.player_id]

    number_category = None

    for tile in all_tiles:
        if tile.is_number():
            if number_category is None:
                number_category = tile.__category
            elif tile.__category != number_category:
                return False
        else:
            return False

    for meld in all_melds:
        for tile in meld.tiles:
            if tile.is_number():
                if number_category is None:
                    number_category = tile.__category
                elif tile.__category != number_category:
                    return False
            else:
                return False

    return True


def is_tianhu(view: View):
    """
    判断是否天胡
    :param view:
    :return:
    """
    return view.banker == view.player_id and view.player_id == view.action_id and view.action == mo and \
           all(len(melds) == 0 for melds in view.all_player_melds) and \
           len(view.all_player_discard_tiles[view.player_id]) == 0


def is_dihu(view: View):
    """
    判断是否地胡
    :param view:
    :return:
    """
    return view.banker != view.player_id and view.player_id == view.action_id and view.action == mo and \
           all(len(melds) == 0 for melds in view.all_player_melds) and \
           len(view.all_player_discard_tiles[view.player_id]) == 0


def is_dasanyan(view: View):
    """
    判断是否大三元
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    # 三元牌的刻子数目应该是
    meld_three_cnt = 0

    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type is peng and meld.tiles[0].is_honor():
            meld_three_cnt += 1

    for split_form in normal_form_split(all_tiles):
        hand_three_cnt = 0
        for pack in split_form:
            if pack_is_three(pack) and pack[0].is_honor():
                hand_three_cnt += 1
        if hand_three_cnt + meld_three_cnt == 3:
            return True
    return False


def is_sianke(view: View):
    """
    判断是否四暗刻
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action]
    all_melds = view.all_player_melds[view.player_id]
    # 先判断是否门清状态

    # 普通四暗刻必须自己自摸
    if view.action != mo:
        return False

    for meld in all_melds:
        if meld.meld_type != angang:
            return False

    flag = False

    for split_form in normal_form_split(all_tiles):
        for pack in split_form:
            if not pack_is_three(pack):
                return False
            if pack[0] == view.action_tile:
                flag = True
    return flag


def is_ziyise(view: View):
    """
    判断是否字一色
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action]
    all_melds = view.all_player_melds[view.player_id]

    for tile in all_tiles:
        if tile.is_number():
            return False

    for meld in all_melds:
        for tile in meld.tiles:
            if tile.is_number():
                return False

    return True


green_list = {
    Tile(suo, 2, 0),
    Tile(suo, 3, 0),
    Tile(suo, 4, 0),
    Tile(suo, 6, 0),
    Tile(honor, 1, 0)
}


def is_lvyise(view: View):
    """
    判断是否绿一色
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    all_melds = view.all_player_melds[view.player_id]

    for tile in all_tiles:
        if tile not in green_list:
            return False
    for meld in all_melds:
        for tile in meld.tiles:
            if tile not in green_list:
                return False


def is_qinglaotou(view: View):
    """
    判断是否青老头
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    all_melds = view.all_player_melds[view.player_id]

    for tile in all_tiles:
        if not tile.is_one_nine():
            return False
    for meld in all_melds:
        for tile in meld.tiles:
            if not tile.is_one_nine():
                return False
    return True


def is_guoshiwushuang(view: View):
    """
    判断是否国士无双
    :param view:
    :return:
    """
    # 首先需要门清状态
    if view.all_player_melds[view.player_id]:
        return False
    all_tiles = view.hand_tiles + [view.action_tile]
    for tile in all_tiles:
        if tile not in yaojiu_list:
            return False
    d = list2dict(all_tiles)
    if len(d) != 13:
        return False
    # 接下来是国士无双13面的判断

    d = list2dict(view.hand_tiles)
    if len(d) == 13:
        return False  # 应当是13面
    else:
        return True


def is_xiaosixi(view: View):
    """
    判断是否小四喜
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    # 东南西北，中有一种是两张的雀头，另外两种都有刻子
    # 输出风牌的对子和刻子的数目，分别应该是1和3
    meld_three_cnt = 0

    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type is peng and meld.tiles[0].is_wind():
            meld_three_cnt += 1

    for split_form in normal_form_split(all_tiles):
        hand_pair_cnt = 0
        hand_three_cnt = 0
        for pack in split_form:
            if pack_is_pair(pack) and pack[0].is_wind():
                hand_pair_cnt += 1
            elif pack_is_three(pack) and pack[0].is_wind():
                hand_three_cnt += 1
        if hand_pair_cnt == 1 and meld_three_cnt + hand_three_cnt == 3:
            return True
    return False


def is_sigangzi(view: View):
    """
    判断是否四杠子
    :param view:
    :return:
    """
    all_melds = view.all_player_melds[view.player_id]
    return all(meld.meld_type in (minggang, angang, jiagang) for meld in all_melds)


def is_jiulian(view: View):
    """
    判断是否九莲
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    if len(all_tiles) != 14:
        return False

    # 确定是清一色
    if not is_qingyise(view):
        return False

    cnt = list(range(10))
    # 统计所有牌，保证符合基本九莲格式
    for tile in all_tiles:
        cnt[tile.__value] += 1
    if cnt[1] < 3 or cnt[9] < 3 or not all(cnt[2:9]):
        return False
    # 统计手牌，保证不是纯九莲
    cnt = list(range(10))
    for tile in view.hand_tiles:
        cnt[tile.__value] += 1
    if cnt[1] == 3 and cnt[9] == 3 and all(cnt[2:9]):
        return False
    else:
        return True


def is_siankedanji(view: View):
    """
    判断是否四暗刻单骑
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action]
    all_melds = view.all_player_melds[view.player_id]
    # 先判断是否门清状态

    for meld in all_melds:
        if meld.meld_type != angang:
            return False

    for split_form in normal_form_split(all_tiles):
        for pack in split_form:
            if not pack_is_three(pack):
                return False

    return True


def is_guoshiwuhuangshisanmian(view: View):
    """
    判断是否十三面
    :param view:
    :return:
    """
    # 首先需要门清状态
    if view.all_player_melds[view.player_id]:
        return False
    all_tiles = view.hand_tiles + [view.action_tile]
    for tile in all_tiles:
        if tile not in yaojiu_list:
            return False
    d = list2dict(all_tiles)
    if len(d) != 13:
        return False
    # 接下来是国士无双13面的判断

    d = list2dict(view.hand_tiles)
    if len(d) == 13:
        return True  # 应当是13面
    else:
        return False


def is_chunzhengjiulian(view: View):
    """
    判断是否纯正九莲
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    if len(all_tiles) != 14:
        return False

    # 确定是清一色
    if not is_qingyise(view):
        return False

    cnt = list(range(10))
    # 统计所有牌，保证符合基本九莲格式
    for tile in all_tiles:
        cnt[tile.__value] += 1
    if cnt[1] < 3 or cnt[9] < 3 or not all(cnt[2:9]):
        return False
    # 统计手牌，保证不是纯九莲
    cnt = list(range(10))
    for tile in view.hand_tiles:
        cnt[tile.__value] += 1
    if cnt[1] == 3 and cnt[9] == 3 and all(cnt[2:9]):
        return True
    else:
        return False


def is_dasixi(view: View):
    """
    是否大四喜
    :param view:
    :return:
    """
    all_tiles = view.hand_tiles + [view.action_tile]
    # 东南西北，都是刻子
    meld_three_cnt = 0

    melds = view.all_player_melds[view.player_id]
    for meld in melds:
        if meld.meld_type is peng and meld.tiles[0].is_wind():
            meld_three_cnt += 1

    for split_form in normal_form_split(all_tiles):
        hand_three_cnt = 0
        for pack in split_form:
            if pack_is_three(pack) and pack[0].is_wind():
                hand_three_cnt += 1
        if meld_three_cnt + hand_three_cnt == 3:
            return True
    return False
