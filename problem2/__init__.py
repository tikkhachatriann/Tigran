class AddressBook:

    def __init__(self):
        self.address_book = {}

    def create_user(self, phone_number, name,surname):
        self.address_book[phone_number] = {name: surname}


def main():
    book = AddressBook()
    while True:
        name = input('type your name: ')
        sur_name = input('type your sur_name : ')
        phone_number = input('type your phone_number: ')
        exit = input("if you want to close addressBook please type 'exit' if not type '+'")
        book.create_user(phone_number, name, sur_name)
        if exit == "exit":
            print(book.address_book)
            break
        else:
            print(book.address_book)


if __name__ == "__main__":
    main()
