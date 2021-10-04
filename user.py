import re 

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

def checkEmail(email):   
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def checkPassword(password):
    len_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None 
    uppercase_error = re.search(r"[A-Z]", password) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    return not (len_error or digit_error or uppercase_error or symbol_error)

class User:
    id_count = 0
    #constructor
    def __init__(self, user_email, user_password, user_type = 'Patient'):
        if checkEmail(user_email) and checkPassword(user_password):
            self.email = user_email
            self.password = user_password
            self.type = user_type
            User.id_count += 1
            self.ID = str(User.id_count).zfill(7)
        else:
            print(checkEmail(user_email))
            print(checkPassword(user_password))
        
    """ #getters
    def getType(self):
        return self.type
    
    def getEmail(self):
        return self.email
    
    def getPass(self):"""  """
        return self.password """

    #modifiers
    def changeType(self, new_type):
        self.type = new_type

    def changeEmail(self, new_email):
        if(checkEmail(new_email)):
            self.email = new_email

    def changePass(self, new_pass):
        self.password = new_pass
    
test_user = User('jzheng1818@bths.edu', 'Pineapple1!', user_type= 'Doctor')

print(test_user.ID)
    
