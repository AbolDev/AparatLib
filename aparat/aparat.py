import requests
import pickle
from typing import Dict, Union
from enum import Enum

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

class ResolutionError(Exception):
    """Exception raised when the specified video resolution is unavailable."""
    
    def __init__(self, message="The requested video resolution is unavailable."):
        self.message = message
        super().__init__(self.message)

class ReportReason(Enum):
    FAKE_NEWS = 45
    NATIONAL_SECURITY = 24
    IMPROPER_CLOTHING = 25
    SEXUAL_CONTENT = 26
    ETHNIC_INSULTS = 27
    RELIGIOUS_INSULTS = 28
    POLITICAL_INSULTS = 29
    VIOLENT_CONTENT = 30
    DEFAMATION = 31
    DANGEROUS_ACTIVITIES = 32
    HATE_SPEECH = 33
    CHILD_ABUSE = 34
    INAPPROPRIATE_FOR_CHILDREN = 35
    IMITATIVE_BEHAVIOR = 36
    MISLEADING_CONTENT = 37
    VIOLATION_OF_RULES = 38
    MISLEADING_TITLE = 39
    PRIVACY_VIOLATION = 40
    COPYRIGHT_VIOLATION = 41
    UNAUTHORIZED_ADVERTISING = 42
    TECHNICAL_PROBLEM = 43
    OTHER = 44

class Comment(object):
    """Aparat Comment Model.

    This class represents a comment on an Aparat video and provides methods
    to interact with the comment, such as liking, unliking, deleting, reporting,
    replying, and retrieving replies.

    Attributes:
        id (str): Comment ID.
        body (str): Content of the comment.
        reply (str): Reply content if the comment is a reply to another comment.
        sdate (str): Submission date of the comment.
        sdate_timediff (str): Time difference since the comment was submitted.
        sdate_gregorian (str): Gregorian submission date of the comment.
        replyAction (str): Action link to reply to the comment.
        replyDelete (str): Action link to delete a reply to the comment.
        text (str): Text content of the comment.
        type (str): Type of the comment.
        approve_link_text (str): Text of the approval link.
        approve_link_href (str): Href of the approval link.
        approved (str): Approval status of the comment.
        approve_raw (str): Raw approval status of the comment.
        isYours (bool): Indicates if the comment is made by the logged-in user.
        deleted (bool): Indicates if the comment is deleted.
        like_cnt (int): Number of likes for the comment.
        reply_cnt (int): Number of replies to the comment.
        mentioned_user_id (str): ID of the mentioned user in the comment.
        mentioned_name (str): Name of the mentioned user in the comment.
        need_approve (bool): Indicates if the comment needs approval.
        spam (bool): Indicates if the comment is marked as spam.
        is_pinned (bool): Indicates if the comment is pinned.
        vid (int): ID of the associated video.
        is_logged_in (bool): Boolean indicating whether the user is logged in.
        session: Session object for making HTTP requests.
    """

    def __init__(self, data: Dict[str, Union[str, int]], vid: int, is_logged_in: bool, session):
        """
        Initialize a Comment object.

        :param data: Dictionary containing comment data.
        :param vid: ID of the associated video.
        :param is_logged_in: Boolean indicating whether the user is logged in.
        :param session: Session object for making HTTP requests.
        """

        self.data = data
        self.vid = vid
        self.is_logged_in = is_logged_in
        self.session = session
        for key, value in data.items():
            if key in ['id', 'body', 'reply', 'sdate', 'sdate_timediff', 'sdate_gregorian', 'replyAction', 'replyDelete',
                       'text', 'type', 'approve_link_text', 'approve_link_href', 'approved', 'approve_raw', 'isYours', 'deleted',
                       'like_cnt', 'reply_cnt', 'mentioned_user_id', 'mentioned_name', 'need_approve', 'spam', 'is_pinned']:
                setattr(self, key, value)
    
    def like(self, timeout: int = 10) -> bool:
        """
        Like the comment.

        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: True if the comment is successfully liked, False otherwise.
        """

        if self.data['like']['status'] == 'unlike':
            response = self.session.get(self.data['like']['link'], timeout=timeout)
            if response.status_code == 200:
                return True
        return False

    def unlike(self, timeout: int = 10) -> bool:
        """
        Unlike the comment.

        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: True if the comment is successfully unliked, False otherwise.
        """

        if self.data['like']['status'] == 'like':
            response = self.session.get(self.data['like']['link'], timeout=timeout)
            if response.status_code == 200:
                return True
        return False

    def delete(self, timeout: int = 10) -> bool:
        """
        Delete the comment.

        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: True if the comment is successfully deleted, False otherwise.
        
        Raises:
            LoginRequiredError: If the user is not logged in.
            ValueError: If the comment does not have a delete URL.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()

        if not self.data['delete_url']:
            raise ValueError("This comment does not have a delete URL.")
        
        response = self.session.get(self.data['delete_url'], timeout=timeout)
        data = response.json()
        if response.status_code == 200 and data['data'] and data['data']['attributes']['type'] == 'success':
            return True
        else:
            return False

    def report(self, timeout: int = 10) -> bool:
        """
        Report the comment.

        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: True if the comment is successfully reported, False otherwise.
        
        Raises:
            ValueError: If the comment does not have a report URL.
        """

        if not self.data['report_url']:
            raise ValueError("This comment does not have a report URL.")
        
        response = self.session.get(self.data['report_url'], timeout=timeout)
        data = response.json()
        if response.status_code == 200 and data['data'] and data['data']['type'] == 'success':
            return True
        else:
            return False

    def reply_to_comment(self, body: str, timeout: int = 10) -> bool:
        """
        Reply to the comment.

        :param body: The content of the reply.
        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: True if the reply is successfully posted, False otherwise.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()
        
        json_data = {
            'comment_id': self.id,
            'body': body
        }

        response = self.session.post(f'https://www.aparat.com/api/fa/v1/video/comment/reply_v2/videohash/{self.vid}', json=json_data, timeout=timeout)
        data = response.json()
        if response.status_code == 200 and data['data'] and data['data']['type'] == 'success':
            return True
        else:
            return False

    def get_replies(self, timeout: int = 10) -> Union[Dict[str, Union[str, int]], bool]:
        """
        Get replies to the comment.

        :param timeout: Timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing reply data if replies exist, an empty list if there are no replies,
                 or False if an error occurs.
        """

        response = self.session.get(f'https://www.aparat.com/api/fa/v1/video/comment/list_replies/comment_id/{self.id}/videohash/{self.vid}', timeout=timeout)
        data = response.json()
        if response.status_code == 200:
            if data['data']:
                return data['data']
            else:
                return []
        else:
            return False

class Video(object):
    """ Aparat Video Model
        
    Attributes:
        id (int): The ID of the video.
        title (str): The title of the video.
        description (str): The description of the video.
        uid (str): The UID of the video.
        visit_cnt (int): The visit count of the video.
        visit_cnt_non_formatted (int): The non-formatted visit count of the video.
        like_cnt_non_formatted (int): The non-formatted like count of the video.
        big_poster (str): The URL of the big poster of the video.
        medium_poster (str): The URL of the medium poster of the video.
        small_poster (str): The URL of the small poster of the video.
        duration (str): The duration of the video.
        meta_duration (str): The meta duration of the video.
        date_exact (str): The exact date of the video.
        sdate (str): The sdate of the video.
        sdate_timediff (int): The time difference of the video.
        sdate_real (str): The real sdate of the video.
        deleted (str): The deleted status of the video.
        mdate (str): The mdate of the video.
        file_link_all (List[Dict[str, Union[str, List[str]]]]): List of dictionaries containing file links and their details.
        file_link (str): The file link of the video.
        hls_link (str): The HLS link of the video.
        can_download (bool): The download status of the video.
        tags (str): The tags of the video.
        tags_str (str): The string representation of tags of the video.
        tags_fa (List[str]): The Persian tags of the video.
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
        self.uid = data['data']['attributes']['uid']
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
    
    def send_comment(self, comment: str, timeout: int = 10) -> Comment:
        """Send a comment for this video.

        Args:
            comment (str): The comment to be sent.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            Comment: A Comment object representing the sent comment.
        
        Raises:
            LoginRequiredError: If the user is not logged in.
            ValueError: If the video does not have a comment link or if comments are disabled for the video.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()
        
        if not self.data['data']['attributes'].get('commentSendLink'):
            raise ValueError("This video does not have a comment link.")

        if self.data['data']['attributes']['comment_enable'] not in ['yes', 'approve']:
            raise ValueError("Comments are disabled for this video.")

        data = {'commentbody': comment}
        response = self.session.post(self.data['data']['attributes']['commentSendLink'], data=data)
        
        data = response.json()
        if 'data' in data and data['data']['attributes']['type'] == 'success' and data['data']['id']:
            response = self.session.get(f'{base_url}/api/fa/v1/video/comment/list/videohash/{self.uid}?perpage=100', timeout=timeout)
            comment_id = data['data']['id']
            if response.status_code == 200:
                data = response.json()
                for comment in data['data']:
                    if str(comment['id']) == str(comment_id):
                        return Comment(comment['attributes'], self.uid, self.is_logged_in, self.session)
                while 'links' in data and 'more' in data['links'] and data['links']['more']:
                    response = self.session.get(f'{data['links']['more']}&perpage=100', timeout=timeout)
                    data = None
                    if response.status_code == 200:
                        data = response.json()
                        for comment in data['data']:
                            if str(comment['id']) == str(comment_id):
                                return Comment(comment['attributes'], self.uid, self.is_logged_in, self.session)
        elif 'errors' in data:
            raise ValueError(data['errors'][0]['detail'])

    def like(self, timeout: int = 10) -> bool:
        """
        Like a video.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the video is successfully liked, False otherwise.
        """

        for item in self.data['included']:
            if 'type' in item and item['type'] == 'Like':
                if item['attributes']['status'] == 'unlike':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        return True
        return False

    def unlike(self, timeout: int = 10) -> bool:
        """
        Unlike a video.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the video is successfully liked, False otherwise.
        """

        for item in self.data['included']:
            if 'type' in item and item['type'] == 'Like':
                if item['attributes']['status'] == 'like':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        return True
        return False

    def download(self, resolution: str = None, download_highest_resolution: bool = None, path: str = None, chunk_size: int = 1024 * 1024 * 4) -> str:
        """
        Download the video with the specified resolution.

        Args:
            resolution (str, optional): The desired video resolution (e.g., '144p', '720p').
            download_highest_resolution (bool, optional): If True, download the highest available resolution.
            path (str, optional): The path where the video will be saved. Defaults to the video's name.
            chunk_size (int, optional): The size of chunks to download at a time (default is 4 MB).

        Raises:
            ValueError: If neither `resolution` nor `download_highest_resolution` is specified.
            ResolutionError: If the specified video resolution is not found.

        Returns:
            str: The path where the downloaded video is saved.
        """
        url = None
        if not resolution and not download_highest_resolution:
            raise ValueError("Either 'resolution' or 'download_highest_resolution' must be specified.")

        elif download_highest_resolution:
            url = self.data['data']['attributes']['file_link_all'][-1]['urls'][0]

        else:
            for link in self.data['data']['attributes']['file_link_all']:
                if link['profile'] == resolution:
                    url = link['urls'][0]
                    break
        
        if not url:
            raise ResolutionError()

        path = path if path else url.split('/')[-1].split('?')[0]

        with self.session.get(url, stream=True) as response:
            with open(path, 'wb') as file:
                for chunk in response.iter_content(chunk_size):
                    file.write(chunk)
            return path
        
    def report(self, reason: ReportReason = '', main_time: str = '', main_time1: str = '', main_time2: str = '', body: str = None, timeout: int = 10) -> Union[str, bool]:
        """
        Report the video for a specified reason.

        Args:
            reason (str, optional): The reason for reporting the video.
            main_time (str, optional): The main time point of the issue in the video.
            main_time1 (str, optional): An additional time point of the issue in the video.
            main_time2 (str, optional): Another additional time point of the issue in the video.
            body (str, optional): Additional details about the report.

        Raises:
            LoginRequiredError: If the user is not logged in.
            ValueError: If the video is not reportable.

        Returns:
            Union[str, bool]: A success message if the report is successful, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError("User must be logged in to report a video.")
        
        if not self.data['data']['attributes']['is_reportable']:
            raise ValueError("This video cannot be reported.")

        json_data = {
            'videoURL': f'https://www.aparat.com/v/{self.uid}',
            'reason': reason.value if type(reason) == ReportReason else reason,
            'main_time': main_time,
            'main_time1': main_time1,
            'main_time2': main_time2,
        }

        if body:
            json_data['body'] = body

        response = self.session.post(f'{base_url}/api/fa/v1/video/video/report/videohash/{self.uid}', json=json_data, timeout=timeout)
        data = response.json()

        try:
            if data['data']['attributes']['type'] == 'success':
                return data['data']['attributes']['text'].split('<span>')[1].split('</span>')[0].strip()
            else:
                return False
        except (KeyError, IndexError):
            return False

    def follow(self, toggle_push_notifications: bool = False, timeout: int = 10) -> bool:
        """
        Follow a user.

        :param toggle_push_notifications: A boolean indicating whether to toggle push notifications for the followed user.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        for item in self.data['included']:
            if item['type'] == 'Follow':
                if item['attributes']['status'] == 'unfollow':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        if toggle_push_notifications:
                            data = response.json()
                            self.session.get(data['data']['attributes']['link_toggle_push_follow'], timeout=timeout)
                        return True
        return False

    def unfollow(self, timeout: int = 10) -> bool:
        """
        Unfollow a user.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        for item in self.data['included']:
            if item['type'] == 'Follow':
                if item['attributes']['status'] == 'follow':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        return True
        return False


class User(object):
    """ Aparat User Model
        
    Attributes:
        id (str): The unique identifier of the user.
        hash_user_id (str): The hashed identifier of the user.
        afcn (str): The user's name in a format suitable for related publications.
        username (str): The username of the user.
        name (str): The name of the user.
        pic_s (str): The URL of the small profile picture of the user.
        pic_m (str): The URL of the medium profile picture of the user.
        pic_b (str): The URL of the large profile picture of the user.
        follower_cnt (int): The number of followers of the user.
        follow_cnt (int): The number of users that the user follows.
        official (str): The official status of the user.
        url (str): The URL of the user's profile.
        video_cnt (int): The number of videos uploaded by the user.
        cover_src (str): The URL of the user's cover image.
        video_visit (int): The number of visits to the user's videos.
        priority (str): The priority of the user.
        brand_priority (str): The brand priority of the user.
        description (str): The description of the user.
        start_date (str): The start date of the user's activity.
        start_date_jalali (str): The start date of the user's activity in the Jalali calendar.
        show_kids_friendly (str): The display of a suitable label for children.
        banned (str): The banned status of the user.
        has_event (str): The event status of the user.
    """

    def __init__(self, data: Dict[str, Union[str, int]], is_logged_in, session):
        self.data = data
        self.is_logged_in = is_logged_in
        self.session = session
        data_ = data['data']['attributes']
        for key, value in data_.items():
            if key in ['id', 'hash_user_id', 'afcn', 'username', 'name', 'pic_s', 'pic_m', 'pic_b', 'follower_cnt',
                       'follow_cnt', 'official', 'url', 'video_cnt', 'cover_src', 'video_visit', 'priority', 'brand_priority',
                       'description', 'start_date', 'start_date_jalali','show_kids_friendly', 'banned', 'has_event']:
                setattr(self, key, value)
    
    def follow(self, toggle_push_notifications: bool = False, timeout: int = 10) -> bool:
        """
        Follow a user.

        :param toggle_push_notifications: A boolean indicating whether to toggle push notifications for the followed user.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        for item in self.data['included']:
            if item['type'] == 'Follow':
                if item['attributes']['status'] == 'unfollow':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        if toggle_push_notifications:
                            data = response.json()
                            self.session.get(data['data']['attributes']['link_toggle_push_follow'], timeout=timeout)
                        return True
        return False

    def unfollow(self, timeout: int = 10) -> bool:
        """
        Unfollow a user.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        for item in self.data['included']:
            if item['type'] == 'Follow':
                if item['attributes']['status'] == 'follow':
                    response = self.session.get(item['attributes']['link'], timeout=timeout)
                    if response.status_code == 200:
                        return True
        return False

class Aparat:
    """Aparat API Client
    
    Attributes:
        proxy (str): The proxy URL, if used.
        session (requests.Session): The requests session object.
        is_logged_in (bool): Flag indicating if the client is logged in.
    """

    def __init__(self, proxy: Union[None, dict] = None):
        """Initialize Aparat API client.
        
        Args:
            proxy (dict, optional): The proxy configuration dictionary. Defaults to None.
                Example: {'http': 'http://proxy.example.com:8080', 'https': 'https://proxy.example.com:8080'}
        """
        self.session = requests.Session()
        self.is_logged_in = False
        self.proxy = proxy

        if self.proxy:
            self.session.proxies.update(self.proxy)

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
                self.username = username
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

    def get_user(self, user_id: str, timeout: int = 10) -> User:
        """
        Get information about a user by their username.

        :param user_id: The username of the user.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing user information if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/user/user/information/username/{user_id}', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return User(data, self.is_logged_in, self.session)
        return None

    def get_comment(self, vid: str, comment_id: str, timeout: int = 10) -> Comment:
        """
        Get information about a comment by their username.

        :param user_id: The username of the user.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A dictionary containing user information if successful, otherwise None.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/video/comment/list/videohash/{vid}?perpage=100', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            for comment in data['data']:
                if comment['id'] == comment_id:
                    return Comment(comment['attributes'], vid, self.is_logged_in, self.session)
            while 'links' in data and 'more' in data['links'] and data['links']['more']:
                response = self.session.get(f'{data['links']['more']}&perpage=100', timeout=timeout)
                data = None
                if response.status_code == 200:
                    data = response.json()
                    for comment in data['data']:
                        if comment['id'] == comment_id:
                            return Comment(comment['attributes'], vid, self.is_logged_in, self.session)
        raise ValueError('...')

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
