
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


def check_dig(number):
    return [x for x in number]


def checking_last_char(digits_list):
    if digits_list[-1] == "1":
        return arm_special_num[1]
    else:
        return arm_nums[digits_list[-1]]


def checking_second_char(digits_list):
    if digits_list[1] == "1":
        return arm_special_num[1]
    else:
        return arm_nums[digits_list[1]]


def check_teen_end(digits_list):
    if "10" < "".join(digits_list[-2:]) < "20":
        return f"{arm_nums[digits_list[-2] + '0']}ն" \
               f"{checking_last_char(digits_list)}"
    elif digits_list[-2] == "0":
        return f"{checking_last_char(digits_list)}"
    else:
        return f"{arm_nums[digits_list[-2] + '0']}" \
               f"{checking_last_char(digits_list)}"


def check_teen_start(digits_list):
    if "10" < "".join(digits_list[-5:-3]) < "20":
        return f"{arm_nums[digits_list[-5] + '0']}ն"\
               f"{checking_second_char(digits_list)}"

    elif digits_list[-5] == "0":
        return f"{arm_nums[digits_list[0]]}"
    else:
        return f"{arm_nums[digits_list[-5] + '0']}" \



def check_hundred_end(digits_list):
    if digits_list[-3] == "0":
        return f"{check_teen_end(digits_list)}"
    elif digits_list[-3] == "1":
        return f"{arm_nums['100']} {check_teen_end(digits_list)}"
    else:
        return f"{arm_nums[digits_list[-3]]} {arm_nums['100']}" \
               f" {check_teen_end(digits_list)}"


def check_hundred_start(digits_list):
    if digits_list[-6] == "0":
        return f"{check_teen_start(digits_list)}"
    elif digits_list[-6] == "1":
        return f"{arm_nums['100']}" \
               f" {check_teen_start(digits_list)}"
    else:
        return f"{arm_nums[digits_list[-6]]} {arm_nums['100']}" \
               f" {check_teen_start(digits_list)}"



def check_thousand(digits_list):
    if digits_list[-4] == "0":
        return f"{arm_nums['1000']} {check_hundred_end(digits_list)}"
    # elif digits_list[-4] == "1":
    #     return f"{arm_nums['1000']}" \
    #            f" {check_hundred_end(digits_list)}"
    else:
        return f"{arm_nums[digits_list[-4]]} {arm_nums['1000']}" \
               f" {check_hundred_end(digits_list)}"


def check_ten_thousand(digits_list):
    #if digits_list[-5] == "1":
    return f"{check_teen_start(digits_list)} {check_thousand(digits_list)}"
    # return f"{arm_nums[digits_list[0]]}" \
    #        f"{check_teen_start(digits_list)} {check_thousand(digits_list)}"


def check_hundred_thousand(digits_list):
    if digits_list[-4] == "1" and digits_list[-5] != "1":
        return f"{check_hundred_start(digits_list)}" \
               f"{arm_special_num[1]} " \
               f"{check_thousand(digits_list)}"

    return f"{check_hundred_start(digits_list)} " \
           f"{check_thousand(digits_list)}"


def check_million(digits_list):
    if digits_list[0] == "1":
        return f"{arm_special_num[1]} {arm_nums['1000000']} "\
               f"{check_hundred_start(digits_list) }"\
               f"{check_thousand(digits_list)}"
    return f"{arm_nums[digits_list[0]]} {arm_nums['1000000']} "\
           f"{check_hundred_start(digits_list)}"\
           f"{check_thousand(digits_list)}"


def get_final_result(digits_list):
    final_list = []

    if len(digits_list) == 7:
        final_list.append(check_million(digits_list))

    elif len(digits_list) == 6:
        final_list.append(check_hundred_thousand(digits_list))

    elif len(digits_list) == 5:
        final_list.append(check_ten_thousand(digits_list))

    elif len(digits_list) == 4:
        final_list.append(f"{check_thousand(digits_list)}")

    elif len(digits_list) == 3:
        final_list.append(check_hundred_end(digits_list))

    elif len(digits_list) == 2:
        final_list.append(check_teen_end(digits_list))

    elif len(digits_list) == 1:
        final_list.append(f"{checking_last_char(digits_list)}")

    return final_list


if __name__ == "__main__":
    number = input("input number")
    print(get_final_result(check_dig(number)))










