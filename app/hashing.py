from passlib.context import CryptContext

class Hash():
    def __init__(self):
        self.pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def bcrypt(self, password):
        return self.pwd_cxt.hash(password)
