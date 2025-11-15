class UserLogin:
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return str(self.user.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_name(self):
        return self.user.name

    def get_email(self):
        return self.user.email





