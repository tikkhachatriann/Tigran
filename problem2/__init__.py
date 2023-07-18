class AddressBook:

    def __init__(self, name: str, sur_name: str, phone_number: str):
        self.name = name
        self.surName = sur_name
        self.phoneNumber = phone_number
        self.address_book = {}
        if self.phoneNumber.startswith("+374"):
            print("Armenian number")
            self.phoneNumber = phone_number
        elif self.phoneNumber.startswith("+7"):
            print("Russian number")
            self.phoneNumber = phone_number
        else:
            print("Another area code")
            self.phoneNumber = phone_number


def main():
    address_book_ = {}
    book = AddressBook
    while True:
        book.name = input('type your name: ')
        book.sur_name = input('type your sur_name : ')
        book.phone_number = input('type your phone_number: ')
        exit = input("if you want to close addressBook please type 'exit' if not type '+'")
        if exit == "exit":
            address_book_[book.phone_number] = {book.name: book.sur_name}
            print(address_book_)
            break
        else:
            address_book_[book.phone_number] = {book.name: book.sur_name}
            print(address_book_)


if __name__ == "__main__":
    main()
