from aparat import Aparat

def main():
    aparat = Aparat()
    if aparat.login('your_username', 'your_password'):
        print("Login successful")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
