def try_func(func):
    """
    :param func: 需要try运行的函数
    :return: 封装函数，报错会打印
    """
    def wrapper(*args):
        try:
            res = func(*args)
            return res
        except Exception as e:
            print(e)

    return wrapper


if __name__ == '__main__':
    @try_func
    def say_hi(a, b):
        print(f'say hi. {a}, {b}')


    say_hi(1, 2)
