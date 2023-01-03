from ...common.utils import get_random_string, get_current_datetime

class Notification:
    description = "General purpose JSON form storage"

    def __init__(self, user_id, noti_data):
        self.PK = f"USER#{user_id}"
        self.SK = f"FORM#{get_random_string(10)}"
        self.user_id = user_id
        self.noti_data = noti_data
        self.created_at = get_current_datetime()
        self.updated_at = get_current_datetime()

    # Instance method
    def get_keys(self):
        return {"PK": self.PK, "SK": self.SK}

    def to_json(self):
        return vars(self)

    def __str__(self):
        return f"{vars(self)}"