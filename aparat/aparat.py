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

class VideoNotFoundError(Exception):
    """Exception raised for video not found errors."""
    def __init__(self, message="Video does not exist."):
        self.message = message
        super().__init__(self.message)

class Video(object):
    """ Aparat Video Model
        
    Attributes:
        id (str): The ID of the video.
        title (str): The title of the video.
        description (str): The description of the video.
        uid (str): The UID of the video.
        visit_cnt (int): The visit count of the video.
        visit_cnt_non_formatted (str): The non-formatted visit count of the video.
        like_cnt_non_formatted (str): The non-formatted like count of the video.
        big_poster (str): The URL of the big poster of the video.
        medium_poster (str): The URL of the medium poster of the video.
        small_poster (str): The URL of the small poster of the video.
        duration (str): The duration of the video.
        meta_duration (str): The meta duration of the video.
        date_exact (str): The exact date of the video.
        sdate (str): The sdate of the video.
        sdate_timediff (str): The time difference of the video.
        sdate_real (str): The real sdate of the video.
        deleted (str): The deleted status of the video.
        mdate (str): The mdate of the video.
        file_link_all (str): The all file link of the video.
        file_link (str): The file link of the video.
        hls_link (str): The HLS link of the video.
        can_download (str): The download status of the video.
        tags (str): The tags of the video.
        tags_str (str): The string representation of tags of the video.
        tags_fa (str): The Persian tags of the video.
        frame_src (str): The frame source of the video.
        category (str): The category of the video.
        360d (str): The 360d status of the video.
        comment_enable (str): The comment enable status of the video.
        official (str): The official status of the video.
        extra_data (str): The extra data of the video.
        content_type (str): The content type of the video.
        file_hash (str): The file hash of the video.
        isCompany (str): The company status of the video.
        isAbroad (str): The abroad status of the video.
        kids_friendly (str): The kids friendly status of the video.
        owner_username (str): The owner's username of the video.
        max_width (str): The maximum width of the video.
        max_height (str): The maximum height of the video.
    """

    def __init__(self, data: Dict[str, Union[str, int]], is_logged_in, session):
        self.data = data
        self.is_logged_in = is_logged_in
        self.session = session
        data_ = data['data']['attributes']
        for key, value in data_.items():
            if key in ['id', 'title', 'description', 'uid', 'visit_cnt', 'visit_cnt_non_formatted',
                       'like_cnt_non_formatted', 'big_poster', 'medium_poster', 'small_poster', 'duration',
                       'meta_duration', 'date_exact', 'sdate', 'sdate_timediff', 'sdate_real', 'deleted', 'mdate',
                       'file_link_all', 'file_link', 'hls_link', 'can_download', 'tags', 'tags_str', 'tags_fa',
                       'frame_src', 'category', '360d', 'comment_enable', 'official', 'extra_data', 'content_type',
                       'file_hash', 'isCompany', 'isAbroad', 'kids_friendly', 'owner_username', 'max_width',
                       'max_height']:
                setattr(self, key, value)
    
    def commentSend(self, comment):
        """Send a comment for this video.

        Args:
            comment (str): The comment to be sent.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        if not self.data['data']['attributes'].get('commentSendLink'):
            raise ValueError("This video does not have a comment link.")

        if self.data['data']['attributes']['comment_enable'] != 'yes':
            raise ValueError("Comments are disabled for this video.")

        data = {'commentbody': comment}
        response = self.session.post(self.data['data']['attributes']['commentSendLink'], data=data)
        
        return response.json()

class Aparat:
    """Aparat API Client
    
    Attributes:
        proxy (str): The proxy URL, if used.
        session (requests.Session): The requests session object.
        is_logged_in (bool): Flag indicating if the client is logged in.
    """

    def __init__(self, proxy=None):
        """Initialize Aparat API client.
        
        Args:
            proxy (str, optional): The proxy URL. Defaults to None.
        """
        self.session = requests.Session()
        self.is_logged_in = False
        self.proxy = proxy

        if self.proxy:
            self.session.proxies.update({'https': self.proxy})

    def login(self, username: str, password: str, timeout: int = 10) -> bool:
        """
        Log in to the Aparat account.

        :param username: The username of the Aparat account.
        :param password: The password of the Aparat account.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: AuthV1 cookie if login is successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/signin?callbackType=postmessage', timeout=timeout)
        guid = response.text.split('guid: "')[1].split('",')[0]

        json_data = {'guid': guid}
        response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/auth?callbackType=postmessage', json=json_data, timeout=timeout)
        data = response.json()
        temp_id = data['data']['attributes']['temp_id']

        json_data = {
            'account': username,
            'temp_id': temp_id,
            'guid': guid
        }
        response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/signin_step1?callbackType=postmessage', json=json_data, timeout=timeout)
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
            response = self.session.post(f'{base_url}/api/fa/v1/user/Authenticate/signin_step2?callbackType=postmessage', json=json_data, timeout=timeout)

            if response.status_code == 200:
                self.is_logged_in = True
                return True
            elif response.status_code == 403 and response.json()['errors'][0]['type_info'] == 'get_max_tokens':
                url = base_url + response.json()['errors'][0]['uri']
                params = {
                    'callbackType': 'postmessage',
                    'guid': guid,
                }
                response = self.session.get(url, params=params, timeout=timeout).json()
                
                url = base_url + response['data']['attributes']['data'][list(response['data']['attributes']['data'].keys())[0]]['revoke_link']
                response = self.session.get(url, timeout=timeout)
                
                url = base_url + response.json()['data']['attributes']['uri']
                params = {
                    'callbackType': 'postmessage',
                    'guid': guid,
                }
                response = self.session.get(url, params=params, timeout=timeout)

                self.is_logged_in = True
                self.username = username
                return True
            elif response.status_code == 401:
                raise IncorrectPasswordError()
            else:
                raise LoginFailedError()
        elif response.status_code == 406:
            raise UsernameNotFoundError()
        else:
            raise LoginFailedError()

    def get_me(self, timeout: int = 10) -> Union[Dict, None]:
        """
        Get information about the current user.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing user information if successful, otherwise None.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    def username_information(self, user_id: str, timeout: int = 10) -> Union[Dict, None]:
        """
        Get information about a user by their username.

        :param user_id: The username of the user.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing user information if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    def notifications(self, timeout: int = 10) -> Union[Dict, None]:
        """
        Get notifications for the current user.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing notifications if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/message/list', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    def dashboard(self, timeout: int = 10) -> Union[Dict, None]:
        """
        Get the dashboard for the current user.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing the user's dashboard if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/dashboard/comments/list_type/all', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    def follow(self, user_id: str, timeout: int = 10) -> bool:
        """
        Follow a user.

        :param user_id: The ID of the user to follow.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}', timeout=timeout)

        if response.status_code == 200:
            data = response.json()
            for item in data['included']:
                if item['type'] == 'Follow':
                    if item['attributes']['status'] == 'unfollow':
                        follow_response = self.session.get(item['attributes']['link'], timeout=timeout)
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise UsernameNotFoundError()

    def unfollow(self, user_id: str, timeout: int = 10) -> bool:
        """
        Unfollow a user.

        :param user_id: The ID of the user to unfollow.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully unfollowed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}', timeout=timeout)

        if response.status_code == 200:
            data = response.json()
            for item in data['included']:
                if item['type'] == 'Follow':
                    if item['attributes']['status'] == 'follow':
                        follow_response = self.session.get(item['attributes']['link'], timeout=timeout)
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise UsernameNotFoundError()

    def like(self, vid: str, timeout: int = 10) -> bool:
        """
        Like a video.

        :param vid: The ID of the video to like.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the video is successfully liked, False otherwise.
        """

        response = self.session.get(f'{base_url}/api/fa/v1/video/video/show/videohash/{vid}?pr=1&mf=1', timeout=timeout)
        data = response.json()

        if 'meta' in data and 'status' not in data['meta']:
            for item in data['included']:
                if 'type' in item and item['type'] == 'Like':
                    if item['attributes']['status'] == 'unlike':
                        follow_response = self.session.get(item['attributes']['link'], timeout=timeout)
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise VideoNotFoundError()

    def unlike(self, vid: str, timeout: int = 10) -> bool:
        """
        Unlike a video.

        :param vid: The ID of the video to unlike.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the video is successfully unliked, False otherwise.
        """

        response = self.session.get(f'{base_url}/api/fa/v1/video/video/show/videohash/{vid}?pr=1&mf=1', timeout=timeout)
        data = response.json()

        if 'meta' in data and 'status' not in data['meta']:
            for item in data['included']:
                if item['type'] == 'Like':
                    if item['attributes']['status'] == 'like':
                        follow_response = self.session.get(item['attributes']['link'], timeout=timeout)
                        if follow_response.status_code == 200:
                            return True
            return False
        else:
            raise VideoNotFoundError()

    def get_video(self, vid: str, timeout: int = 10) -> Video:
        """Get video details from Aparat.
        
        Args:
            vid (str): The video ID.
            timeout (int, optional): The request timeout. Defaults to 10.
        
        Returns:
            Video: An instance of the Video class representing the video.
        
        Raises:
            VideoNotFoundError: If the requested video is not found.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/video/video/show/videohash/{vid}?pr=1&mf=1', timeout=timeout)
        data = response.json()

        if 'meta' in data and 'status' not in data['meta']:
            return Video(data, self.is_logged_in, self.session)
        else:
            raise VideoNotFoundError()

    def logout(self) -> None:
        """
        Log out from the Aparat account.
        """
        self.session = requests.Session()
        self.is_logged_in = False

    def save_session(self) -> None:
        """
        Save the session object to a file.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        with open(f'{self.username}.session', 'wb') as f:
            pickle.dump(self.session, f)

    def load_session(self, username: str, timeout: int = 10) -> None:
        """
        Load the session object from a file.
        """
        with open(f'{username}.session', 'rb') as f:
            session = pickle.load(f)

            response = session.get(f'{base_url}/api/fa/v1/etc/page/config/mode/full', timeout=timeout)
            if response.json()['included'][0]['attributes']:
                self.session = session
                self.is_logged_in = True
                self.username = username
                return True
            else:
                return False
