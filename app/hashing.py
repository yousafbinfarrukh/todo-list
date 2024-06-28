from passlib.context import CryptContext

class Hash():
    def __init__(self):
        self.pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def bcrypt(self, password):
        return self.pwd_cxt.hash(password)

    def verify (self, user_password, request_password):
        return self.pwd_cxt.verify(request_password, user_password)
