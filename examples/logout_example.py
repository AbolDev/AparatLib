from aparat import Aparat

def main():
    aparat = Aparat()
    auth_cookie = aparat.login('your_username', 'your_password')
    if auth_cookie:
        print("Login successful")
        aparat.logout()
        print("Logged out successfully.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
