class AllowableRoles:
    ADMIN = "admin"
    USER = "user"

    @classmethod
    def all(cls):
        return [cls.ADMIN, cls.USER]
