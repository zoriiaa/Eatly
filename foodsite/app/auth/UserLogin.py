class UserLogin:
    def __init__(self, user):
        self.user = user

    @property
    def is_authenticated(self):
        # Користувач вважається авторизованим
        return True

    @property
    def is_active(self):
        # Користувач активний (не заблокований)
        return True

    @property
    def is_anonymous(self):
        # Не анонімний
        return False

    def get_id(self):
        #збереження сесії
        return str(self.user.id)

    @property
    def name(self):
        return self.user.name



