def lv_func(a: str, x: int) -> str:
    """
    :param a: 原字段
    :param x: "MaxLevel"   "x"
    :return: 原字段 + "MaxLevel"   "x"
    """
    mod = f'''_t1_"MaxLevel"                      "{x}"\n'''
    tab = a.split('"')[0]
    a2 = a + mod.replace('_t1_', tab)
    return a2


if __name__ == '__main__':
    t = '''		"SpellImmunityType"				"SPELL_IMMUNITY_ENEMIES_NO"'''
    print(lv_func(t, 6))
    print(lv_func(t, 4))
