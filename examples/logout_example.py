from aparat import Aparat

def main():
    aparat = Aparat()
    if aparat.login('your_username', 'your_password'):
        print("Login successful")
        aparat.logout()
        print("Logged out successfully.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
