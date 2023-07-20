
arm_special_num = {
        0: "զրո",
        1: "մեկ",
}
arm_nums = {
        0: "",
        1: "",
        2: "երկու",
        3: "երեք",
        4: "չորս",
        5: "հինգ",
        6: "վեց",
        7: "յոթ",
        8: "ութ",
        9: "ինն",
        10: "տաս",
        20: "քսան",
        30: "եռեսուն",
        40: "քառասուն",
        50: "հիթսուն",
        60: "վաթսուն",
        70: "յոթանասուն",
        80: "ութսուն",
        90: "իննսուն",
        100: "հարյուր",
        1000: "հազար"
}


# changing length of the number
def get_checked_list(num):
    list_of_digits = [int(x) for x in str(num)]
    if len(list_of_digits) > 1:
        list_of_digits[-2] = int(str(num)[-2] + "0")
    return list_of_digits


def get_text_for_ten(list_final):
    text = "".join(list_final)
    if "տաս" in text:
        new_text = text.replace("տաս", "տասն")
        return new_text
    return text


def checking_for_hundred(list_digits):
    if len(list_digits) == 4 and list_digits[1] == 0:
        return ""
    return arm_nums[100]


# checking last character
def checking_last_char(list_for_digits):
    if list_for_digits[-1] == 1:
        return arm_special_num[1]
    else:
        return arm_nums[list_for_digits[-1]]


# changing number to text
def get_final_result(list_of_digits):
    final_list = []

    if len(list_of_digits) == 4:
        final_list.append(
            f"{arm_nums[list_of_digits[0]]} {arm_nums[1000]} "
            f"{arm_nums[list_of_digits[1]]} "
            f"{checking_for_hundred(list_of_digits)} "
            f"{arm_nums[list_of_digits[2]]}"
            f"{checking_last_char(list_of_digits)}"
            )

    elif len(list_of_digits) == 3:
        final_list.append(
            f"{arm_nums[list_of_digits[0]]} {arm_nums[100]}"
            f" {arm_nums[list_of_digits[1]]}" 
            f"{checking_last_char(list_of_digits)}"
            )

    elif len(list_of_digits) == 2:
        final_list.append(
            f"{arm_nums[list_of_digits[0]]}"
            f"{checking_last_char(list_of_digits)}"
            )

    elif len(list_of_digits) == 1:
        final_list.append(f"{checking_last_char(list_of_digits)}")

    return final_list


if __name__ == "__main__":
    number = input("input number")

    try:
        number = int(number)
        if number == 1000:
            print(arm_nums[1000])
        elif number == 100:
            print(arm_nums[100])
        elif number == 10:
            print(arm_nums[10])
        elif number == 0:
            print(arm_special_num[1])
        else:
            print(get_text_for_ten(get_final_result(get_checked_list(number))))

    except ValueError:
        print("You have to text number")

