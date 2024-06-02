import requests
import pickle
from typing import Dict, Union

base_url = 'https://www.aparat.com'

class IncorrectPasswordError(Exception):
    """Exception raised for incorrect password errors."""
    def __init__(self, message="The password is not correct."):
        self.message = message
        super().__init__(self.message)

class LoginFailedError(Exception):
    """Exception raised for login failed errors."""
    def __init__(self, message="Login failed."):
        self.message = message
        super().__init__(self.message)

class UsernameNotFoundError(Exception):
    """Exception raised for username not found errors."""
    def __init__(self, message="Username does not exist."):
        self.message = message
        super().__init__(self.message)

class LoginRequiredError(Exception):
    """Exception raised for login required errors."""
    def __init__(self, message="Please login first."):
        self.message = message
        super().__init__(self.message)

class Aparat:
    def __init__(self):
        self.session = requests.Session()
        self.is_logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Log in to the Aparat account.

        :param username: The username of the Aparat account.
        :param password: The password of the Aparat account.
        :return: AuthV1 cookie if login is successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/signin?callbackType=postmessage')
        guid = response.text.split('guid: "')[1].split('",')[0]

        json_data = {'guid': guid}
        response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/auth?callbackType=postmessage', json=json_data)
        data = response.json()
        temp_id = data['data']['attributes']['temp_id']

        json_data = {
            'account': username,
            'temp_id': temp_id,
            'guid': guid
        }
        response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/signin_step1?callbackType=postmessage', json=json_data)
        if response.status_code == 200:
            data = response.json()
            temp_id = data['data']['attributes']['temp_id']

            json_data = {
                'temp_id': temp_id,
                'account': username,
                'codepass_type': 'pass',
                'code': password,
                'guid': guid
            }
            response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/signin_step2?callbackType=postmessage', json=json_data)

            if response.status_code == 200:
                self.is_logged_in = True
                # print("Logged in successfully.")
                return True
            elif response.status_code == 403 and response.json()['errors'][0]['type_info'] == 'get_max_tokens':
                url = '{base_url}' + response.json()['errors'][0]['uri']
                params = {
                    'callbackType': 'postmessage',
                    'guid': guid,
                }
                response = self.session.get(url, params=params).json()
                
                url = '{base_url}' + response['data']['attributes']['data'][list(response['data']['attributes']['data'].keys())[0]]['revoke_link']
                response = self.session.get(url)
                
                url = '{base_url}' + response.json()['data']['attributes']['uri']
                params = {
                    'callbackType': 'postmessage',
                    'guid': guid,
                }
                response = self.session.get(url, params=params)

                self.is_logged_in = True
                self.username = username
                # print("Logged in successfully.")
                return True
            elif response.status_code == 401:
                raise IncorrectPasswordError()
            elif response.status_code == 406:
                raise UsernameNotFoundError()
            else:
                raise LoginFailedError()
        else:
            raise LoginFailedError()

    def get_me(self) -> Union[Dict, None]:
        """
        Get information about the current user.

        :return: A dictionary containing user information if successful, otherwise None.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information')
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    def username_information(self, user_id: str) -> Union[Dict, None]:
        """
        Get information about a user by their username.

        :param user_id: The username of the user.
        :return: A dictionary containing user information if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}')
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    def notifications(self) -> Union[Dict, None]:
        """
        Get notifications for the current user.

        :return: A dictionary containing notifications if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/message/list')
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    def dashboard(self) -> Union[Dict, None]:
        """
        Get the dashboard for the current user.

        :return: A dictionary containing the user's dashboard if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/dashboard/comments/list_type/all')
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    def follow(self, user_id: str) -> bool:
        """
        Follow a user.

        :param user_id: The ID of the user to follow.
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}')

        if response.status_code == 200:
            data = response.json()
            for item in data['included']:
                if item['type'] == 'Follow':
                    if item['attributes']['status'] == 'unfollow':
                        follow_response = self.session.get(item['attributes']['link'])
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise UsernameNotFoundError()

    def unfollow(self, user_id: str) -> bool:
        """
        Unfollow a user.

        :param user_id: The ID of the user to unfollow.
        :return: True if the user is successfully unfollowed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}')

        if response.status_code == 200:
            data = response.json()
            for item in data['included']:
                if item['type'] == 'Follow':
                    if item['attributes']['status'] == 'follow':
                        follow_response = self.session.get(item['attributes']['link'])
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise UsernameNotFoundError()

    def logout(self) -> None:
        """
        Log out from the Aparat account.
        """
        self.session = requests.Session()
        self.is_logged_in = False
        # print("Logged out successfully.")

    def save_session(self) -> None:
        """
        Save the session object to a file.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        with open(f'{self.username}.session', 'wb') as f:
            pickle.dump(self.session, f)
        # print("Session saved successfully.")

    def load_session(self, username: str) -> None:
        """
        Load the session object from a file.
        """
        with open(f'{username}.session', 'rb') as f:
            session = pickle.load(f)

            response = session.get(f'{base_url}/api/fa/v1/etc/page/config/mode/full')
            if response.json()['included'][0]['attributes']:
                self.session = session
                self.is_logged_in = True
                self.username = username
                # print("Session loaded successfully.")
                return True
            else:
                return False
