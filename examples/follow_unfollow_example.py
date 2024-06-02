from aparat import Aparat

def main():
    aparat = Aparat()
    auth_cookie = aparat.login('your_username', 'your_password')
    if auth_cookie:
        print("Login successful. Auth cookie:", auth_cookie)
        user_id = 'user_id_to_follow'

        if aparat.follow(user_id):
            print(f"Successfully followed {user_id}.")
        else:
            print(f"Failed to follow {user_id}.")

        if aparat.unfollow(user_id):
            print(f"Successfully unfollowed {user_id}.")
        else:
            print(f"Failed to unfollow {user_id}.")

        aparat.logout()
        print("Logged out successfully.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
