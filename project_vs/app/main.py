import re
import bcrypt

from app.database import get_db, get_cursor


class UserController:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Hash password

        Parameters
        ----------
        password : str

        Returns
        -------
        bytes

        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, hashed_password: bytes) -> bool:
        """
        Check password

        Parameters
        ----------
        password : str
        hashed_password : bytes

        Returns
        -------
        bool

        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    def is_valid_email(self, mail_address: str) -> bool:
        """
        Is valid email

        Parameters
        ----------
        mail_address : str

        Returns
        -------
        bool

        """
        return re.match(r"^[\w\.-]+@[\w\.-]+$", mail_address)

    def is_valid_password(self, password: str) -> bool:
        """
        Is valid email

        Parameters
        ----------
        password : str

        Returns
        -------
        bool

        """
        return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password)

    def get_user(self, user_name: str) -> tuple:
        """
        Get user

        Parameters
        ----------
        user_name : str

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute("SELECT * FROM USER WHERE username = ?", (user_name,))
        return cursor.fetchone()

    def validate_user(self, user_name: str, password: str) -> tuple:
        """
        Validate user

        Parameters
        ----------
        user_name : str
        password : str

        Returns
        -------
        tuple

        """
        if user := self.get_user(user_name):
            if self.check_password(password, user["password"]):
                return user

    def register_user(self, user_data: dict):
        """
        Register user

        Parameters
        ----------
        user_data: dict

        """

        if not self.is_valid_email(user_data["mail"]):
            raise ValueError("Invalid email address. Please enter valid email.")

        if not self.is_valid_password(user_data["password"]):
            raise ValueError(
                "Length: At least 8 characters\
                Both lowercase and uppercase letters\
                At least one digit"
            )

        if user_data["password"] != user_data["password2"]:
            raise ValueError("The passwords do not match. Please try again.")

        if not (hashed_password := self.hash_password(user_data["password"])):
            raise ValueError("Username alredy exists. Replace your username")

        if any(value.strip() == "" for value in user_data.values()):
            raise ValueError("Fields cannot be empty or contains whitespaces")

        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO USER(name, surname, mail, username, password)\
                VALUES(?, ?, ?, ?, ?)",
                (
                    user_data["name"],
                    user_data["surname"],
                    user_data["mail"],
                    user_data["username"],
                    hashed_password,
                ),
            )
            con.commit()


class BookingController:
    @staticmethod
    def get_tables() -> tuple:
        """
        Get tables

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute("SELECT * FROM RESERVES")
        return cursor
    
    @staticmethod
    def get_events(event_id=None) -> tuple:
        """
        Get events

        Parameters
        ----------
        event_id : optional, int

        Returns
        -------
        tuple

        """
        with get_db() as con:
            cursor = con.cursor()
            if event_id is None:
                cursor.execute("SELECT id, week_day, date, dj_name FROM EVENTS")
                return cursor
            else:
                cursor.execute("SELECT * FROM EVENTS WHERE id = ?", (event_id,))
                return cursor.fetchone()
    
    def get_list(self, event_id: int) -> list:
        """
        Get list

        Parameters
        ----------
        event_id : int

        Returns
        -------
        list

        """
        event_data = self.get_events(event_id)

        if event_data and event_data['table_id_list']:
            table_id_list = [
                int(id_str) for id_str in event_data['table_id_list'].split(',')
            ]
        else:
            table_id_list = []
        
        return table_id_list


    def book_table(self, table_id: int, event_id: int):
        """
        Book table

        Parameters
        ----------
        table_id : int
        event_id : int

        """
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT table_id_list FROM EVENTS WHERE id = ?",
                (event_id,)
            )

            current_list_str = cursor.fetchone()

            if table_ids := current_list_str["table_id_list"]:
                new_list = table_ids.split(",")
                new_list.append(table_id)
            else:
                new_list = [table_id]

            updated_list_str = ",".join(set(new_list))

            cursor.execute(
                "UPDATE EVENTS SET table_id_list = ? WHERE id = ?",
                (updated_list_str, event_id),
            )
            con.commit()
