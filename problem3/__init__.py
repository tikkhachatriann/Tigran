
arm_special_num = "զրո", "մեկ",

arm_nums = {
    '0': "",
    '1': "",
    '2': "երկու",
    '3': "երեք",
    '4': "չորս",
    '5': "հինգ",
    '6': "վեց",
    '7': "յոթ",
    '8': "ութ",
    '9': "ինն",
    '10': "տաս",
    '20': "քսան",
    '30': "երեսուն",
    '40': "քառասուն",
    '50': "հիթսուն",
    '60': "վաթսուն",
    '70': "յոթանասուն",
    '80': "ութսուն",
    '90': "իննսուն",
    '100': "հարյուր",
    '1000': "հազար",
    '1000000': "միլիոն"
}


def get_last_char(last_digit: str) -> str:
    """
    Get last char

    Parameters
    ----------
    last_digit : str

    Returns
    -------
    str

    """
    return arm_special_num[1] if last_digit == "1" else arm_nums[last_digit]


def check_teen_nums(digits_list: list) -> str:
    """
    Check teen nums

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    if digits_list[0] == "0":
        return f"{get_last_char(digits_list[1])}"

    separator = "ն" if digits_list[0] == "1" and digits_list[1] != "0" else ""

    return f"{arm_nums[digits_list[0] + '0']}{separator}" \
           f"{get_last_char(digits_list[1])}"


def check_hundred_nums(digits_list: list) -> str:
    """
    Check hundred nums

    Parameters
    ----------
    digits_list : str

    Returns
    -------
    str

    """
    if digits_list[-3] == "0":
        return f"{check_teen_nums(digits_list[-2:])}"

    separator = "" if digits_list[-3] == "1" else f"{arm_nums[digits_list[0]]} "

    return f"{separator}{arm_nums['100']} " \
           f"{check_teen_nums(digits_list[-2:])}"


def check_thousand(digits_list: list) -> str:
    """
    Check thousand

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    digit_number = "" if (digits_list[-4] == "0" or len(digits_list) > 4) \
        else f"{arm_nums[digits_list[0]]}"

    return f"{digit_number} {arm_nums['1000']} " \
           f"{check_hundred_nums(digits_list[-3:])}"


def get_ten_thousand(digits_list: list) -> str:
    """
    Get ten thousand

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    return f"{check_teen_nums(digits_list[-5:-3])} " \
           f"{check_thousand(digits_list)}"


def get_hundred_thousand(digits_list: list) -> str:
    """
    Check hundred nums

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    return f"{check_hundred_nums(digits_list[-6:-3])} " \
           f"{check_thousand(digits_list)}"


def check_million(digits_list: list) -> str:
    """
    Check million

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    start_million = f"{get_last_char(digits_list[0])} {arm_nums['1000000']} " \
        if len(digits_list) < 7 else f"{arm_nums['1000000']} "

    if check_hundred_nums(digits_list[-6:-3]) == "":
        return f"{start_million} {check_hundred_nums(digits_list[-3:])}"

    return f"{start_million}{get_hundred_thousand(digits_list)}"


def get_ten_million(digits_list: list) -> str:
    """
    Check ten million

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    return f"{check_teen_nums(digits_list[-8:-6])} " \
           f"{check_million(digits_list)}" \



def get_hundred_million(digits_list: list) -> str:
    """
    Check hundred million

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    return f"{check_hundred_nums(digits_list[:3])} " \
           f"{check_million(digits_list)}"


def get_final_result(digits_list: list) -> str:
    """
    Get final result

    Parameters
    ----------
    digits_list : list

    Returns
    -------
    str

    """
    match len(digits_list):
        case 1:
            return get_last_char(digits_list[-1])
        case 2:
            return check_teen_nums(digits_list)
        case 3:
            return check_hundred_nums(digits_list)
        case 4:
            return check_thousand(digits_list)
        case 5:
            return get_ten_thousand(digits_list)
        case 6:
            return get_hundred_thousand(digits_list)
        case 7:
            return check_million(digits_list)
        case 8:
            return get_ten_million(digits_list)
        case 9:
            return get_hundred_million(digits_list)


if __name__ == "__main__":
    print("Press 0 if you want finish")
    while True:
        input_number = input("input number ".strip())
        number = [x for x in input_number]

        if not input_number.isdigit():
            print("Invalid input ")
        elif number == ["0"]:
            print(arm_special_num[0])
            print("The loop was ended")
            break
        else:
            print(get_final_result(number))
