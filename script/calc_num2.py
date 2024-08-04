def calculate_next_two_elements_from_string(input_str, oneval=0):
    # 将输入字符串按空格分割，并转换为浮点数列表
    numbers_str = input_str.split()
    numbers = [float(num) for num in numbers_str]

    # 检查列表是否至少有两个元素
    if len(numbers) < 2:
        raise ValueError("输入字符串至少需要包含两个数字，用空格分隔")

    # 计算公差
    common_difference = numbers[1] - numbers[0]

    # 计算后两个元素
    next_element1 = numbers[-1] + common_difference
    next_element2 = next_element1 + common_difference

    # 确定输出的小数位数
    max_decimal_places = max(len(num.split('.')[1]) if '.' in num else 0 for num in numbers_str)

    if oneval == 0:
        # 格式化输出，保持与输入相同的小数位数
        formatted_numbers = []
        for num in numbers + [next_element1, next_element2]:
            if '.' in str(num):
                # 如果数字是小数，保留与输入相同的小数位数
                formatted_num = '{:.{prec}f}'.format(num, prec=max_decimal_places)
            else:
                # 如果数字是整数，不保留小数点
                formatted_num = str(int(num))
            formatted_numbers.append(formatted_num)

        common_difference = f'{common_difference:.{max_decimal_places}f}'

        # 将所有数字转换为字符串，用空格分隔
        return ' '.join(formatted_numbers), common_difference

    else:
        # 格式化输出，保持与输入相同的小数位数
        formatted_numbers = []
        for num in numbers + [next_element1]:
            if '.' in str(num):
                # 如果数字是小数，保留与输入相同的小数位数
                formatted_num = '{:.{prec}f}'.format(num, prec=max_decimal_places)
            else:
                # 如果数字是整数，不保留小数点
                formatted_num = str(int(num))
            formatted_numbers.append(formatted_num)

        common_difference = f'{common_difference:.{max_decimal_places}f}'

        # 将所有数字转换为字符串，用空格分隔
        return ' '.join(formatted_numbers), common_difference


if __name__ == '__main__':
    # 示例使用
    input_str = "1 1.5 2 2.5"
    output_str = calculate_next_two_elements_from_string(input_str, 0)
    print(output_str)
