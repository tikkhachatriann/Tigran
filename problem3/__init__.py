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


# checking last character of number
def get_last_char(last_digit):
    return arm_special_num[1] if last_digit == "1" else arm_nums[last_digit]


# checking teen numbers from the end
def check_teen_nums(digits):

    if digits[0] == "0":
        return f"{get_last_char(digits[1])}"

    separator = "ն" if digits[0] == "1" and digits[1] != "0" else ""

    return f"{arm_nums[digits[0] + '0']}{separator}" \
           f"{get_last_char(digits[1])}"


# checking hundred numbers from the end
def check_hundred_nums(digits):

    if digits[-3] == "0":
        return f"{check_teen_nums(digits[-2:])}"

    separator = "" if digits[-3] == "1" else arm_nums[digits[0]]

    return f"{separator} {arm_nums['100']} " \
           f"{check_teen_nums(digits[-2:])}"


# checking thousand numbers
def check_thousand(digits_list):

    digit_number = "" if (digits_list[-4] == "0" or len(digits_list) > 4) \
        else arm_nums[digits_list[0]]

    return f"{digit_number} {arm_nums['1000']} " \
           f"{check_hundred_nums(digits_list[-3:])}"


# checking ten thousand numbers
def check_ten_thousand(digits_list):
    return f"{check_teen_nums(digits_list[-5:-3])} " \
           f"{check_thousand(digits_list)}"


# checking hundred thousand numbers
def check_hundred_thousand(digits_list):
    return f"{check_hundred_nums(digits_list[-6:-3])} " \
           f"{check_thousand(digits_list)}"


# checking million numbers
def check_million(digits_list):

    if check_hundred_nums(digits_list[-6:-3]) == "":
        return f"{get_last_char(digits_list[0])} {arm_nums['1000000']} " \
               f"{check_hundred_nums(digits_list[-3:])}"

    return f"{get_last_char(digits_list[0])} {arm_nums['1000000']} " \
           f"{check_hundred_thousand(digits_list)}"


# checking ten millions numbers
def check_ten_million(digits_list):
    return f"{check_teen_nums(digits_list[-8:-6])} {arm_nums['1000000']} " \
           f"{check_hundred_thousand(digits_list)}"


# getting result vor for a given number
def get_final_result(digits_list):
    final_list = []

    if len(digits_list) == 8:
        final_list.append(check_ten_million(digits_list))

    elif len(digits_list) == 7:
        final_list.append(check_million(digits_list))

    elif len(digits_list) == 6:
        final_list.append(check_hundred_thousand(digits_list))

    elif len(digits_list) == 5:
        final_list.append(check_ten_thousand(digits_list))

    elif len(digits_list) == 4:
        final_list.append(check_thousand(digits_list))

    elif len(digits_list) == 3:
        final_list.append(check_hundred_nums(digits_list))

    elif len(digits_list) == 2:
        final_list.append(check_teen_nums(digits_list))

    elif len(digits_list) == 1:
        final_list.append(get_last_char(digits_list[-1]))

    return final_list


if __name__ == "__main__":
    print("Press 0 if you want finish")
    while True:
        input_number = input("input number").strip()
        number = [x for x in input_number]
        if not input_number.isdigit():
            print("You must be give number")
        elif number == ["0"]:
            print(arm_special_num[0])
            print("The loop was ended")
            break
        else:
            print("".join(get_final_result(number)))



