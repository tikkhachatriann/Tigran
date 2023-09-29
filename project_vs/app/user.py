from flask_login import UserMixin

from app.database import get_cursor


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    @classmethod
    def get(cls, user_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM USER WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data["id"])
            
