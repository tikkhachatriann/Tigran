import json


class AddressBook:

    def __init__(self):
        self.dict_address_book = {}

    # Creating AddressBook list
    def create_account(self, phone_number: str, name: str, surname: str):
        if phone_number not in self.dict_address_book.keys():
            self.dict_address_book[phone_number] = {name: surname}
        else:
            raise KeyError("The phoneNumbers must be unique")

    # updating json files after update numbers
    def update_user(self):
        with open("new_file.json", "w") as new_file:
            json.dump(self.dict_address_book, new_file, indent=3)

    # reading json file
    def address_book_reader(self):
        with open("new_file.json", "r") as new_file:
            data = json.load(new_file)
            print(data)


def main():
    book = AddressBook()

    choosing = input(
        "If you want to update addressBook press 1 if "
        "you want to see addressBook press 2"
    )

    if choosing == "1":
        while True:
            name = input('type your name: ')
            sur_name = input('type your sur_name : ')
            phone_number = input('type your phone_number: ')
            exit_input = input(
                "if you want to close addressBook please type 'exit'"
                " if not type '+'")

            if exit_input == "exit":
                book.create_account(phone_number, name, sur_name)
                print(book.dict_address_book)
                book.update_user()
                break
            else:
                book.create_account(phone_number, name, sur_name)
                print(book.dict_address_book)

    elif choosing == "2":
        book.address_book_reader()


if __name__ == "__main__":
    main()
