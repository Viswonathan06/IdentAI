LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "admin1234"


def passwordLogin(username, password):
    if username.lower() == LOGIN_USERNAME.lower() and password==LOGIN_PASSWORD:
        return {"msg": "Login Success", "status": 'success'}
    else:
        return {"msg": "Invalid username or password", "status": "error"}