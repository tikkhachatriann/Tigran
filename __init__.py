
dict_nums = {
        0: "",
        "0": "զրո",
        1: "",
        "1": "մեկ",
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
        50: "հիտսուն",
        60: "վատսուն",
        70: "յոթանասուն",
        80: "ութսուն",
        90: "իննսուն",
        100: "հարյուր",
        1000: "հազար"

}


# changing length of the number
def checking(num):
    list_of_digits = [int(x) for x in str(num)]
    if len(list_of_digits) > 1:
        list_of_digits[-2] = int(str(num)[-2] + "0")
    return list_of_digits


# def unique(digit):
#     if digit == 1000:
#         print(dict_[1000])
#     elif digit == 100:
#         print(dict_[100])
#     elif digit == 10:
#         print(dict_[10])
#     elif digit == 0:
#         print("zro")


# changing number to text
def changing(list_of_digits):

    final_list = []
    if len(list_of_digits) == 4:

        if list_of_digits[-1] == 1:
            final_list.append(f"{dict_nums[list_of_digits[0]]} "
                              f"{dict_nums[1000]} "
                              f"{dict_nums[list_of_digits[1]]} {dict_nums[100]}" 
                              f" {dict_nums[list_of_digits[2]]}{dict_nums['1']}"
                              )
        else:
            final_list.append(f"{dict_nums[list_of_digits[0]]} "
                              f"{dict_nums[1000]} "
                              f"{dict_nums[list_of_digits[1]]} {dict_nums[100]}"
                              f" {dict_nums[list_of_digits[2]]}"
                              f"{dict_nums[list_of_digits[3]]}"
                              )

    elif len(list_of_digits) == 3:

        if list_of_digits[-1] == 1:
            final_list.append(f"{dict_nums[list_of_digits[0]]} {dict_nums[100]}"
                              f" {dict_nums[list_of_digits[1]]}{dict_nums['1']}"
                              )
        else:
            final_list.append(f"{dict_nums[list_of_digits[0]]} {dict_nums[100]}"
                              f" {dict_nums[list_of_digits[1]]}" 
                              f"{dict_nums[list_of_digits[2]]}"
                              )

    elif len(list_of_digits) == 2:
        if list_of_digits[-1] == 1:
            final_list.append(f"{dict_nums[list_of_digits[0]]}{dict_nums['1']}")
        else:
            final_list.append(f"{dict_nums[list_of_digits[0]]}"
                              f"{dict_nums[list_of_digits[1]]}"
                              )

    elif len(list_of_digits) == 1:
        if dict_nums[list_of_digits[0]] == 1:
            final_list.append(dict_nums["1"])
        else:
            final_list.append(dict_nums[list_of_digits[0]])

    return final_list


def checking_ten(list_final):
    text = "".join(list_final)
    if "տաս" in text:
        new_text = text.replace("տաս", "տասն")
        return new_text
    return text


if __name__ == "__main__":
    number = input("input number")
    try:
        number = int(number)
        if number == 1000:
            print(dict_nums[1000])
        elif number == 100:
            print(dict_nums[100])
        elif number == 10:
            print(dict_nums[10])
        elif number == 0:
            print(dict_nums["0"])
        else:
            print(checking_ten(changing(checking(number))))

    except ValueError:
        print("You have to text number")

