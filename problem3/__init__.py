
arm_special_num = "զրո", "մեկ",

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
        30: "երեսուն",
        40: "քառասուն",
        50: "հիթսուն",
        60: "վաթսուն",
        70: "յոթանասուն",
        80: "ութսուն",
        90: "իննսուն",
        100: "հարյուր",
        1000: "հազար",
        1000000: "միլիոն"
}


# changing length of the number
def get_checked_list(num):
    list_of_digits = [int(x) for x in str(num)]
    if len(list_of_digits) > 1:
        list_of_digits[-2] = int(str(num)[-2] + "0")
    if len(list_of_digits) == 5:
        list_of_digits[0] = int(str(num)[0] + "0")

    return list_of_digits


def get_text_for_ten(list_final):
    text = "".join(list_final)
    if "տաս" in text:
        new_text = text.replace("տաս", "տասն")
        return new_text
    return text


def checking_for_hundred(list_digits):
    if list_digits[-3] == 0:
        return ""
    elif list_digits[-3] == 1:
        return arm_nums[100]
    else:
        return f"{arm_nums[list_digits[-3]]} {arm_nums[100]}"


def checking_for_thousand(list_digits):
    if list_digits[-4] == 0:
        return arm_nums[1000]
    elif len(list_digits) > 4 and list_digits[-4] == 1:
        return f"{arm_special_num[1]} {arm_nums[1000]}"
    else:
        return f"{arm_nums[list_digits[-4]]} {arm_nums[1000]}"


def checking_thousand_hundred(list_digits):
    if list_digits[-6] == 1:
        return f"{arm_nums[100]} "\
                f"{arm_nums[int(str(list_digits[1]) + '0')]}" \
                f"{checking_for_thousand(list_digits)}"

    return f"{arm_nums[list_digits[-6]]}"\
           f"{checking_for_hundred(list_digits)} "\
           f"{arm_nums[int(str(list_digits[1]) + '0')]}" \
           f"{checking_for_thousand(list_digits)}"


def checking_million(list_digits):
    if list_digits[0] == 1:
        return f"{arm_nums[list_digits[0]]}" \
               f"{arm_nums[1000000]} " \
               f"{checking_for_hundred(list_digits[1:4])} " \
               f"{arm_nums[int(str(list_digits[2]) + '0')]}"\
               f"{checking_for_thousand(list_digits)}"
               #f"{checking_thousand_hundred(list_digits)}"


# checking last character
def checking_last_char(list_for_digits):
    if list_for_digits[-1] == 1:
        return arm_special_num[1]
    else:
        return arm_nums[list_for_digits[-1]]


# changing number to text
def get_final_result(list_of_digits):
    final_list = []

    if len(list_of_digits) == 7:
        final_list.append(
            f"{checking_million(list_of_digits)} " 
            f"{checking_for_hundred(list_of_digits)} "
            f"{arm_nums[list_of_digits[-2]]}"
            f"{checking_last_char(list_of_digits)}"
        )

    if len(list_of_digits) == 6:
        final_list.append(

            f"{checking_thousand_hundred(list_of_digits)} "
            f"{checking_for_hundred(list_of_digits)} "
            f"{arm_nums[list_of_digits[-2]]}"
            f"{checking_last_char(list_of_digits)}"
            )

    if len(list_of_digits) == 5:
        final_list.append(
            f"{arm_nums[list_of_digits[0]]}"
            f"{checking_for_thousand(list_of_digits)} "
            f"{checking_for_hundred(list_of_digits)} "
            f" {arm_nums[list_of_digits[3]]}"
            f"{checking_last_char(list_of_digits)}"
            )

    if len(list_of_digits) == 4:
        final_list.append(
            f"{arm_nums[list_of_digits[0]]} "
            f"{checking_for_thousand(list_of_digits)} "
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
        if number == 1000000:
            print(arm_nums[1000000])
        elif number == 100000:
            print(arm_nums[100] + arm_nums[1000])
        elif number == 10000:
            print(arm_nums[10] + arm_nums[1000])
        elif number == 1000:
            print(arm_nums[1000])
        elif number == 100:
            print(arm_nums[100])
        elif number == 10:
            print(arm_nums[10])
        elif number == 0:
            print(arm_special_num[0])
        else:
            print(get_text_for_ten(get_final_result(get_checked_list(number))))

    except ValueError:
        print("You have to text number")

