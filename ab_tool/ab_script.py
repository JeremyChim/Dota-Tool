def func1(ab: str):
    """
    :param ab: 技能信息
    :return: 技能名，技能值
    """
    ls = ab.split('"')
    abn, abv = ls[1], ls[3]
    return abn, abv


def func2(abv: str):
    """
    :param abv: 技能值<str>
    :return: 技能值<list[float]>
    """
    ls = abv.split(' ')
    ls2 = [float(i) for i in ls]
    return ls2


def func3(abl: list[float], x):
    """
    :param abl: 技能值<list[float]>
    :param x: 计算后x位
    :return: 技能值<list[float]>，魔晶值（公差）<float>，魔杖值<float>, 注释值（晶+杖总值）<float>
    """
    sa = abl[1] - abl[0]
    for i in range(x):
        abv = abl[-1] + sa
        abl.append(abv)
    sp = abl[-1]
    tip = abl[-1] * 2 + sa
    return abl, sa, sp, tip


def func3_2(abl: list[float], x):
    """
    冷却类计算
    :param abl: 技能值<list[float]>
    :param x: 计算后x位
    :return: 技能值<list[float]>，魔晶值（公差）<float>，魔杖值<float>, 注释值（晶+杖总值）<float>
    """
    sa = abl[1] - abl[0]
    for i in range(x):
        abv = abl[-1] + sa
        abl.append(abv)
    sp = 0 - (abl[-1] + sa) / 2
    tip = abl[-1] + sa + sp
    return abl, sa, sp, tip


def func3_3(abl: list[float]):
    """
    魔耗类计算
    :param abl: 技能值<list[float]>
    :return: 技能值<list[float]>，魔晶值（公差）<float>，魔杖值<float>, 注释值（晶+杖总值）<float>
    """
    sa = 0 - abl[0] * 0.25
    sp = 0 - abl[0] * 0.5
    tip = abl[0] + sa + sp
    return abl, sa, sp, tip


def func4(ab: str, x):
    """
    :param ab: 技能信息
    :param x: 1是带{}，0是“”，2是只有魔晶{}，3是只有魔杖{}，4是只有魔晶""，5是只有魔杖""，6是只有冷却""
    :return: 新模版（改了缩进）
    """
    mod1 = '''_t0_"ab_name"
_t0_{
_t1_"value"_t2_\t\t\t\t"ab_value"
_t1_"special_bonus_shard"_t2_"sa_value"
_t1_"special_bonus_scepter"_t2_"sp_value"
_t0_}
'''
    mod_ = '''_t0_"ab_name"_t2_\t\t\t\t\t"ab_value"
_t0_"special_bonus_shard"_t2_\t"sa_value"
_t0_"special_bonus_scepter"_t2_\t"sp_value"
'''
    mod_sa = '''_t0_"ab_name"
_t0_{
_t1_"value"_t2_\t\t\t\t"ab_value"
_t1_"special_bonus_shard"_t2_"sa_value"
_t0_}
'''
    mod_sp = '''_t0_"ab_name"
_t0_{
_t1_"value"_t2_\t\t\t\t"ab_value"
_t1_"special_bonus_scepter"_t2_"sp_value"
_t0_}
'''
    mod_sa2 = '''_t0_"ab_name"_t2_\t\t\t\t\t"ab_value"
_t0_"special_bonus_shard"_t2_\t"sa_value"
'''
    mod_sp2 = '''_t0_"ab_name"_t2_\t\t\t\t\t"ab_value"
_t0_"special_bonus_scepter"_t2_\t"sp_value"
'''
    mod_cd = '''_t0_"ab_name"_t2_\t\t\t\t\t"ab_value"
_t0_"special_bonus_shard"_t2_\t"-50%"
_t0_"special_bonus_scepter"_t2_\t"-50%"
'''

    ls = ab.split('"')
    t0 = ls[0]
    t1 = ls[0] + '\t'
    t2 = ls[2]

    match x:
        case 1:
            mod = mod1.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case 2:
            mod = mod_sa.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case 3:
            mod = mod_sp.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case 4:
            mod = mod_sa2.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case 5:
            mod = mod_sp2.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case 6:
            mod = mod_cd.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)
        case _:
            mod = mod_.replace('_t0_', t0).replace('_t1_', t1).replace('_t2_', t2)

    return mod


def func5(mod2, ab_name, ab_value, sa_value, sp_value, tip_value):
    """
    :param mod2: 新模版（改了缩进）
    :param ab_name: 技能名
    :param ab_value: 技能值
    :param sa_value: 魔晶值（公差）
    :param sp_value: 魔杖值
    :param tip_value: 注释值（晶+杖总值）
    :return: 技能信息（替换好的）
    """
    ab = mod2.replace('ab_name', ab_name).replace('ab_value', ab_value).replace('sa_value', sa_value).replace(
        'sp_value', sp_value).replace('tip_value', tip_value)
    return ab


def func6(ls: list[float]):
    """
    :param ls: 技能值<list[float]>
    :return: 小数位<int>
    """
    lp = []  # 小数位表，list_point
    for i in ls:
        i2 = str(i)
        ls2 = i2.split('.')

        if ls2[1] == '0':  # 小数位为0
            lp.append(0)  # 记0
        else:
            p = len(ls2[1])
            lp.append(p)  # 记小数位

    mp = max(lp)  # 算出小数位表里的最大，max_point
    return mp


def func7(mp: int, ab_value: list[float], sa_value: float, sp_value: float, tip_value: float):
    """
    :param mp: 小数位<int>
    :param ab_value: 技能值<list[float]>
    :param sa_value: 魔晶值（公差）
    :param sp_value: 魔杖值
    :param tip_value: 注释值（晶+杖总值）
    :return: 技能值，魔晶值，魔杖值，注释值（全str）
    """
    ab = ' '.join([f'{i:.{mp}f}' for i in ab_value])
    sa = f'{sa_value:.{mp}f}'
    sp = f'{sp_value:.{mp}f}'
    ti = f'{tip_value:.{mp}f}'
    return ab, sa, sp, ti


# def _ab_func(ab: str, x: int = 2, y=False):
#     """
#     :param ab: 技能信息
#     :param x: 计算后x位
#     :param y: 强制 "" mod模板 ，默认false
#     :return: 技能信息<魔改>
#     """
#     abn, abv = func1(ab)  # 技能名，技能值
#     if y:
#         n = 0
#     else:
#         n = 0 if abn == 'value' else 1  # 1带{}，0为""
#     mod = func4(ab, n)  # 新模版（改了缩进）
#     abl = func2(abv)  # 技能值<list[float]>
#
#     if len(abl) != 1 and abl[0] == abl[1] == abl[2]:
#         abl = [abl[0]]  # 相同数值合并
#
#     match abn:
#         case 'AbilityCooldown':
#             if len(abl) == 1:  # 只有一个技能值
#                 sa = 0 - abl[0] * 0.25
#                 sp = 0 - abl[0] * 0.5
#                 ti = abl[0] + sa + sp
#                 ab_str = func7(1, abl, sa, sp, ti)
#             else:
#                 ab_float = func3_2(abl, x)  # 算
#                 ab_str = func7(1, *ab_float)  # 转字符串
#
#         case 'AbilityCastPoint':
#             if len(abl) == 1:  # 只有一个技能值
#                 sa = 0 - abl[0] * 0.25
#                 sp = 0 - abl[0] * 0.5
#                 ti = abl[0] + sa + sp
#                 ab_str = func7(2, abl, sa, sp, ti)
#             else:
#                 ab_float = func3_2(abl, x)  # 算
#                 ab_str = func7(2, *ab_float)  # 转字符串
#
#         case 'AbilityManaCost':
#             if len(abl) == 1:  # 只有一个技能值
#                 sa = 0 - abl[0] * 0.25
#                 sp = 0 - abl[0] * 0.5
#                 ti = abl[0] + sa + sp
#                 ab_str = func7(0, abl, sa, sp, ti)
#             else:
#                 ab_float = func3_3(abl)  # 算
#                 ab_str = func7(0, *ab_float)  # 转字符串
#
#         case _:
#             if len(abl) == 1:  # 只有一个技能值
#                 mp = func6(abl)
#                 sa = abl[0] * 0.5
#                 sp = abl[0]
#                 ti = abl[0] * 2.5
#                 ab_str = func7(mp, abl, sa, sp, ti)
#
#             else:
#                 mp = func6(abl)  # 小数位
#                 ab_float = func3(abl, x)  # 算
#                 ab_str = func7(mp, *ab_float)  # 转字符串
#
#     ls = [*ab_str]  # ab_str是元组无法改，解包到list
#     ls[1] = '+' + ls[1] if '-' not in ls[1] else ls[1]  # sa
#     ls[2] = '+' + ls[2] if '-' not in ls[2] else ls[2]  # sp
#
#     ab2 = func5(mod, abn, *ls)  # 技能信息（替换好的）
#     return ab2


def ab_func(ab: str, x: int = 2, y: int = None):
    """
    :param ab: 技能信息
    :param x: 计算后x位
    :param y: 1是带{}，0是“”，2是只有魔晶{}，3是只有魔杖{}，4是只有魔晶""，5是只有魔杖""，不输入就自行判断
    :return: 技能信息<魔改>
    """
    abn, abv = func1(ab)  # 技能名，技能值

    match y:
        case None:
            n = 0 if abn == 'value' else 1  # 1带{}，0为""
        case 0:
            n = 0
        case 1:
            n = 1
        case 2:
            n = 4 if abn == 'value' else 2  # 2是只有魔晶{}，4是只有魔晶""
        case 3:
            n = 5 if abn == 'value' else 3  # 3是只有魔杖{}，5是只有魔杖""
        case _:
            n = y

    mod = func4(ab, n)  # 新模版（改了缩进）
    abl = func2(abv)  # 技能值<list[float]>
    mp = func6(abl)  # 小数位
    if len(abl) != 1 and abl[0] == abl[1] == abl[2]:
        abl = [abl[0]]  # 相同数值合并

    match abn:
        case 'AbilityCooldown' | 'AbilityCastPoint':
            if len(abl) == 1:  # 只有一个技能值
                abv = f'{abl[0]:.{mp}f}'
            else:
                ab_float = func3(abl, x)  # 算
                abv, *_ = func7(mp, *ab_float)  # 转字符串
            ab_str = [abv, '-50%', '-50%', '-75%']  # 技能值，魔晶值，魔杖值，注释值（全str）

        case 'AbilityManaCost':
            if len(abl) == 1:  # 只有一个技能值
                abv = f'{abl[0]:.{mp}f}'
            else:
                ab_float = func3_3(abl)  # 算
                abv, *_ = func7(mp, *ab_float)  # 转字符串
            ab_str = [abv, '-50%', '-50%', '---']  # 技能值，魔晶值，魔杖值，注释值（全str）

        case _:
            if len(abl) == 1:  # 只有一个技能值
                abv = f'{abl[0]:.{mp}f}'
            else:
                ab_float = func3(abl, x)  # 算
                abv, *_ = func7(mp, *ab_float)  # 转字符串
            ab_str = [abv, '+100%', '+100%', '---']  # 技能值，魔晶值，魔杖值，注释值（全str）

    ab2 = func5(mod, abn, *ab_str)  # 技能信息（替换好的）
    return ab2


if __name__ == '__main__':
    ex = '''\t\t"power"\t\t\t\t"175 250 325 400"'''
    # ex = '''\t\t"value"\t\t\t\t"1.75 2.5 3.25 4"'''
    # ex = '''\t\t"power"\t\t\t\t"1.75 2.50 3.25"'''
    # ex = '''\t\t"value"\t\t\t\t"10 9 8 7"'''
    # ex = '''\t\t"AbilityCooldown"\t\t\t\t"15 14 13 12"'''
    # ex = '''\t\t"AbilityCastPoint"\t\t\t\t"0.15"'''
    # ex = '''\t\t"AbilityManaCost"\t\t\t\t"50 60 70 80"'''
    # ex = '''\t\t"value"\t\t\t\t"0.3 0.3 0.3 0.3"'''
    # ex = '''\t\t"special_bonus_facet_windrunner_tailwind"\t\t\t\t"700"'''

    res = ab_func(ex, 0, 0)
    print(res)
