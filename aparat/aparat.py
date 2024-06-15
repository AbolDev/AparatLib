import requests
import base64
import pickle
import magic
import uuid
import re
import os
from typing import Dict, Union
from tqdm import tqdm
from enum import Enum

base_url = 'https://www.aparat.com'
upload_base_url = 'https://uc3.aparat.com'

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

class VideoCategory(Enum):
    VIDEO_GAME = 22
    SPORTS = 11
    CARTOON_ANIMATION = 18
    COMEDY = 2
    EDUCATION = 3
    ENTERTAINMENT = 4
    MOVIE_SERIES_DOCUMENTARY = 5
    RELIGION = 6
    MUSIC = 7
    NEWS = 8
    LAW_POLITICS = 9
    TECHNOLOGY_COMPUTER = 10
    TRAVEL_TOURISM = 13
    ANIMALS = 14
    BUSINESS = 16
    CULTURE_ART = 17
    FASHION_STYLE = 20
    HEALTH = 21
    FOOD_DRINK = 23
    AUTOMOTIVE = 24
    FAMILY_CHILD = 25
    HOME_LIFE = 26
    ENVIRONMENT = 27
    FINANCE_ECONOMY = 28
    SOCIAL = 29
    BASIC_SCIENCES = 30
    AGRICULTURE_HORTICULTURE = 31

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
    """

    def __init__(self, data: Dict[str, Union[str, int]], uid: int, is_logged_in: bool, session):
        """
        Initialize a Comment object.

        :param data: Dictionary containing comment data.
        :param uid: UID of the associated video.
        :param is_logged_in: Boolean indicating whether the user is logged in.
        :param session: Session object for making HTTP requests.
        """
        self.uid = uid
        self.data = data
        self.session = session
        self.is_logged_in = is_logged_in

        self.id = data.get('id')
        self.body = data.get('body')
        self.reply = data.get('reply')
        self.sdate = data.get('sdate')
        self.sdate_timediff = data.get('sdate_timediff')
        self.sdate_gregorian = data.get('sdate_gregorian')
        self.replyAction = data.get('replyAction')
        self.replyDelete = data.get('replyDelete')
        self.text = data.get('text')
        self.type = data.get('type')
        self.approve_link_text = data.get('approve_link_text')
        self.approve_link_href = data.get('approve_link_href')
        self.approved = data.get('approved')
        self.approve_raw = data.get('approve_raw')
        self.isYours = data.get('isYours')
        self.deleted = data.get('deleted')
        self.like_cnt = data.get('like_cnt')
        self.reply_cnt = data.get('reply_cnt')
        self.mentioned_user_id = data.get('mentioned_user_id')
        self.mentioned_name = data.get('mentioned_name')
        self.need_approve = data.get('need_approve')
        self.spam = data.get('spam')
        self.is_pinned = data.get('is_pinned')
    
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

        response = self.session.post(f'{base_url}/api/fa/v1/video/comment/reply_v2/videohash/{self.uid}', json=json_data, timeout=timeout)
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

        response = self.session.get(f'{base_url}/api/fa/v1/video/comment/list_replies/comment_id/{self.id}/videohash/{self.uid}', timeout=timeout)
        data = response.json()
        if response.status_code == 200:
            if data['data']:
                return data['data']
            else:
                return []
        else:
            return False

class MyVideo(object):
    """ Aparat MyVideo Model
        
    Attributes:
        id (str): The unique identifier of the user.
        uid (str): The unique identifier of the video.
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
        self.session = session
        self.is_logged_in = is_logged_in
        
        self.id = data['attributes'].get('id')
        self.uid = data['attributes'].get('uid')
        self.hash_user_id = data['attributes'].get('hash_user_id')
        self.afcn = data['attributes'].get('afcn')
        self.username = data['attributes'].get('username')
        self.name = data['attributes'].get('name')
        self.pic_s = data['attributes'].get('pic_s')
        self.pic_m = data['attributes'].get('pic_m')
        self.pic_b = data['attributes'].get('pic_b')
        self.follower_cnt = data['attributes'].get('follower_cnt')
        self.follow_cnt = data['attributes'].get('follow_cnt')
        self.official = data['attributes'].get('official')
        self.url = data['attributes'].get('url')
        self.video_cnt = data['attributes'].get('video_cnt')
        self.cover_src = data['attributes'].get('cover_src')
        self.video_visit = data['attributes'].get('video_visit')
        self.priority = data['attributes'].get('priority')
        self.brand_priority = data['attributes'].get('brand_priority')
        self.description = data['attributes'].get('description')
        self.start_date = data['attributes'].get('start_date')
        self.start_date_jalali = data['attributes'].get('start_date_jalali')
        self.show_kids_friendly = data['attributes'].get('show_kids_friendly')
        self.banned = data['attributes'].get('banned')
        self.has_event = data['attributes'].get('has_event')
        
    def delete(self, timeout: int = 10) -> bool:
        """
        Deletes the video.

        This method deletes a video by sending an HTTP GET request to the appropriate delete URL.
        The method checks if the user is logged in and if the delete URL is available.

        Args:
            timeout (int, optional): The timeout for the HTTP request in seconds. Defaults to 10.

        Returns:
            bool: True if the video is successfully deleted, False otherwise.

        Raises:
            LoginRequiredError: If the user is not logged in.
            ValueError: If neither 'share_delete_url' nor 'delete_url' is available.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()
        
        url = self.data['attributes'].get('share_delete_url') if self.data['attributes'].get('share_delete_url') else self.data['attributes'].get('delete_url')

        if not url:
            raise ValueError('delete_url does not exist.')

        response = self.session.get(base_url + url, timeout=timeout)
        if response.status_code == 200:
            return True
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
        _360d (str): The 360d status of the video.
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
        
        self.id = data['data']['attributes'].get('id')
        self.title = data['data']['attributes'].get('title')
        self.description = data['data']['attributes'].get('description')
        self.uid = data['data']['attributes'].get('uid')
        self.visit_cnt = data['data']['attributes'].get('visit_cnt')
        self.visit_cnt_non_formatted = data['data']['attributes'].get('visit_cnt_non_formatted')
        self.like_cnt_non_formatted = data['data']['attributes'].get('like_cnt_non_formatted')
        self.big_poster = data['data']['attributes'].get('big_poster')
        self.medium_poster = data['data']['attributes'].get('medium_poster')
        self.small_poster = data['data']['attributes'].get('small_poster')
        self.duration = data['data']['attributes'].get('duration')
        self.meta_duration = data['data']['attributes'].get('meta_duration')
        self.date_exact = data['data']['attributes'].get('date_exact')
        self.sdate = data['data']['attributes'].get('sdate')
        self.sdate_timediff = data['data']['attributes'].get('sdate_timediff')
        self.sdate_real = data['data']['attributes'].get('sdate_real')
        self.deleted = data['data']['attributes'].get('deleted')
        self.mdate = data['data']['attributes'].get('mdate')
        self.file_link_all = data['data']['attributes'].get('file_link_all')
        self.file_link = data['data']['attributes'].get('file_link')
        self.hls_link = data['data']['attributes'].get('hls_link')
        self.can_download = data['data']['attributes'].get('can_download')
        self.tags = data['data']['attributes'].get('tags')
        self.tags_str = data['data']['attributes'].get('tags_str')
        self.tags_fa = data['data']['attributes'].get('tags_fa')
        self.frame_src = data['data']['attributes'].get('frame_src')
        self.category = data['data']['attributes'].get('category')
        self._360d = data['data']['attributes'].get('360d')
        self.comment_enable = data['data']['attributes'].get('comment_enable')
        self.official = data['data']['attributes'].get('official')
        self.extra_data = data['data']['attributes'].get('extra_data')
        self.content_type = data['data']['attributes'].get('content_type')
        self.file_hash = data['data']['attributes'].get('file_hash')
        self.isCompany = data['data']['attributes'].get('isCompany')
        self.isAbroad = data['data']['attributes'].get('isAbroad')
        self.kids_friendly = data['data']['attributes'].get('kids_friendly')
        self.owner_username = data['data']['attributes'].get('owner_username')
        self.max_width = data['data']['attributes'].get('max_width')
        self.max_height = data['data']['attributes'].get('max_height')
    
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
                    response = self.session.get(f"{data['links']['more']}&perpage=100", timeout=timeout)
                    data = None
                    if response.status_code == 200:
                        data = response.json()
                        for comment in data['data']:
                            if str(comment['id']) == str(comment_id):
                                return Comment(comment['attributes'], self.uid, self.is_logged_in, self.session)
        else:
            raise ValueError(data)

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

    def download(self, resolution: str = None, download_highest_resolution: bool = None, path: str = None, show_progress_bar: bool = True) -> str:
        """
        Download the video with the specified resolution.

        Args:
            resolution (str, optional): The desired video resolution (e.g., '144p', '720p').
            download_highest_resolution (bool, optional): If True, download the highest available resolution.
            path (str, optional): The path where the video will be saved. Defaults to the video's name.
            show_progress_bar (bool, optional): If True, show the download progress bar. Defaults to True.

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

        if path.endswith(os.sep) or os.path.isdir(path):
            file_path = os.path.join(path, url.split('/')[-1].split('?')[0])
        elif os.path.isfile(path) or '.' in os.path.basename(path):
            file_path = path
        else:
            file_path = url.split('/')[-1].split('?')[0]

        with self.session.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('Content-Length', 0))
            chunk_size = 1024 * 1024  # 1 MB
            with open(file_path, 'wb') as f:
                if show_progress_bar:
                    pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(file_path))
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        if show_progress_bar:
                            pbar.update(len(chunk))
                if show_progress_bar:
                    pbar.close()
        
        return file_path

    def report(self, reason: ReportReason, main_time: str = '', main_time1: str = '', main_time2: str = '', body: str = None, timeout: int = 10) -> Union[str, bool]:
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
            'videoURL': f'{base_url}/v/{self.uid}',
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

    def republish(self, timeout: int = 10) -> MyVideo:
        """
        republish video.

        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: True if the user is successfully followed, False otherwise.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        if not self.data['data']['attributes'].get('addToChannelLink'):
            raise ValueError('addToChannelLink does not exist.')

        response = self.session.get(base_url + self.data['data']['attributes']['addToChannelLink'], timeout=timeout)
        data = response.json()
        if response.status_code == 200 and 'data' in data:
            return self.get_my_video(id=data['data']['id'])
        else:
            raise ValueError(response.json())

    def get_my_video(self, id: str = None, uid: str = None, timeout: int = 10) -> MyVideo:
        """
        Get a video by its ID or UID.

        Args:
            id (str, optional): The ID of the video.
            uid (str, optional): The UID of the video.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            MyVideo: The video object.

        Raises:
            ValueError: If neither id nor uid is provided.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()

        if not id and not uid:
            raise ValueError("At least one of 'id' or 'uid' must be provided.")

        response = self.session.get(f'{base_url}/api/fa/v1/user/video/videos', timeout=timeout)
        data = response.json()
        if response.status_code == 200 and data.get('included'):
            for video in data['included']:
                if id:
                    if str(video['id']) == str(id):
                        return MyVideo(video, self.is_logged_in, self.session)
                elif uid:
                    if video['attributes']['uid'] == uid:
                        return MyVideo(video, self.is_logged_in, self.session)
        return None

class Playlist(object):
    """Aparat Playlist Model
    
    Attributes:
        id (int): The ID of the playlist.
        title (str): The title of the playlist.
        description (str): The description of the playlist.
        cnt (int): The count of videos in the playlist.
        big_poster (str): The URL of the big poster image.
        small_poster (str): The URL of the small poster image.
        uid (str): The unique identifier of the playlist.
        toggle_url (str): The URL for toggling the playlist state.
        publish_type (str): The publish type of the playlist.
        create_type (str): The creation type of the playlist.
        checked (bool): The checked status of the playlist.
        order (int): The order of the playlist.
        last_update (str): The last update timestamp of the playlist.
        isYours (bool): Flag indicating if the playlist belongs to the user.
        playlist_follow_link (str): The URL for following the playlist.
        playlist_follow_status (str): The follow status of the playlist.
        list_videos_playlist (list): The list of videos in the playlist.
        videos (list[Video]): The list of Video objects in the playlist.
    """

    def __init__(self, data: Dict[str, Union[str, int]], is_logged_in, session, timeout: int = 10):
        self.is_logged_in = is_logged_in
        self.session = session
        
        self.id = data['data']['attributes'].get('id')
        self.title = data['data']['attributes'].get('title')
        self.description = data['data']['attributes'].get('description')
        self.cnt = data['data']['attributes'].get('cnt')
        self.big_poster = data['data']['attributes'].get('big_poster')
        self.small_poster = data['data']['attributes'].get('small_poster')
        self.uid = data['data']['attributes'].get('uid')
        self.toggle_url = data['data']['attributes'].get('toggle_url')
        self.publish_type = data['data']['attributes'].get('publish_type')
        self.create_type = data['data']['attributes'].get('create_type')
        self.checked = data['data']['attributes'].get('checked')
        self.order = data['data']['attributes'].get('order')
        self.last_update = data['data']['attributes'].get('last_update')
        self.isYours = data['data']['attributes'].get('isYours')
        self.playlist_follow_link = data['data']['attributes'].get('playlist_follow_link')
        self.playlist_follow_status = data['data']['attributes'].get('playlist_follow_status')
        self.list_videos_playlist = data['data']['attributes'].get('list_videos_playlist')
        
        # self.videos: list[Video] = [Video({'data': video, 'included': []}, self.is_logged_in, self.session) for video in data['included'] if video['type'] == 'Video']

        videos_data = []
        for video in data['included']:
            if video['type'] == 'Video':
                response = self.session.get(f"{base_url}/api/fa/v1/video/video/show/videohash/{video['attributes']['uid']}?pr=1&mf=1", timeout=timeout)
                data = response.json()

                if 'meta' in data and 'status' not in data['meta']:
                    videos_data.append(Video(data, self.is_logged_in, self.session))
                else:
                    self.videos = {'data': video, 'included': []}
        
        self.videos: list[Video] = videos_data

    def follow_playlist(self, timeout: int = 10) -> bool:
        """Follow the playlist.
        
        Args:
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).
        
        Returns:
            bool: True if the playlist was successfully followed, False otherwise.
        
        Raises:
            LoginRequiredError: If the user is not logged in.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()

        if self.playlist_follow_status == 'no':
            response = self.session.get(f'{base_url}{self.playlist_follow_link}', timeout=timeout)
            data = response.json()

            if response.status_code == 200 and data['data']['attributes']['type'] == 'success':
                self.playlist_follow_link = data['data']['attributes']['link']
                self.playlist_follow_status = 'yes'
                return True
        return False

    def unfollow_playlist(self, timeout: int = 10) -> bool:
        """Unfollow the playlist.
        
        Args:
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).
        
        Returns:
            bool: True if the playlist was successfully unfollowed, False otherwise.
        
        Raises:
            LoginRequiredError: If the user is not logged in.
        """

        if not self.is_logged_in:
            raise LoginRequiredError()

        if self.playlist_follow_status == 'yes':
            response = self.session.get(f'{base_url}{self.playlist_follow_link}', timeout=timeout)
            data = response.json()

            if response.status_code == 200 and data['data']['attributes']['type'] == 'success':
                self.playlist_follow_link = data['data']['attributes']['link']
                self.playlist_follow_status = 'no'
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
        self.session = session
        self.is_logged_in = is_logged_in
        
        self.id = data['data']['attributes'].get('id')
        self.hash_user_id = data['data']['attributes'].get('hash_user_id')
        self.afcn = data['data']['attributes'].get('afcn')
        self.username = data['data']['attributes'].get('username')
        self.name = data['data']['attributes'].get('name')
        self.pic_s = data['data']['attributes'].get('pic_s')
        self.pic_m = data['data']['attributes'].get('pic_m')
        self.pic_b = data['data']['attributes'].get('pic_b')
        self.follower_cnt = data['data']['attributes'].get('follower_cnt')
        self.follow_cnt = data['data']['attributes'].get('follow_cnt')
        self.official = data['data']['attributes'].get('official')
        self.url = data['data']['attributes'].get('url')
        self.video_cnt = data['data']['attributes'].get('video_cnt')
        self.cover_src = data['data']['attributes'].get('cover_src')
        self.video_visit = data['data']['attributes'].get('video_visit')
        self.priority = data['data']['attributes'].get('priority')
        self.brand_priority = data['data']['attributes'].get('brand_priority')
        self.description = data['data']['attributes'].get('description')
        self.start_date = data['data']['attributes'].get('start_date')
        self.start_date_jalali = data['data']['attributes'].get('start_date_jalali')
        self.show_kids_friendly = data['data']['attributes'].get('show_kids_friendly')
        self.banned = data['data']['attributes'].get('banned')
        self.has_event = data['data']['attributes'].get('has_event')
    
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
        proxy (dict): The proxy dictionary, if used.
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

    def __get_guid(self, timeout: int = 10) -> str:
        """Fetch the GUID required for further authentication steps.
        Args:
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            str: The GUID extracted from the response.
        """
        response = self.session.get('https://www.aparat.com/signin?callbackType=postmessage', timeout=timeout)
        return response.text.split('guid: "')[1].split('",')[0]

    def __get_temp_id(self, guid: str, timeout: int = 10) -> str:
        """Fetch the temporary ID using the provided GUID.

        Args:
            guid (str): The GUID obtained from the initial request.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            str: The temporary ID extracted from the response.
        """
        json_data = {'guid': guid}
        response = self.session.post('https://www.aparat.com/api/fa/v1/user/Authenticate/auth?callbackType=postmessage', json=json_data, timeout=timeout)
        return response.json()['data']['attributes']['temp_id']

    def signup_step1(self, account: str, timeout: int = 10) -> bool:
        """Perform the first step of the signup process.
        
        Args:
            account (str): The account identifier (email or phone number).
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            bool: True if the first step is successful, otherwise raises an exception.
        """
        guid = self.__get_guid(timeout)
        temp_id = self.__get_temp_id(guid, timeout)
        json_data = {
            'account': account,
            'temp_id': temp_id,
            'guid': guid
        }
        response = self.session.post('https://www.aparat.com/api/fa/v1/user/Authenticate/signup_step1?callbackType=postmessage', json=json_data, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            data = response.json()
            raise ValueError(data)

    def signup_step2(self, url: str, account: str, password: str, timeout: int = 10) -> bool:
        """Perform the second step of the signup process using the verification link.

        Args:
            url (str): The URL or email text containing the signup confirmation link.
            account (str): The account identifier (email or phone number).
            password (str): The password for the new account.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            bool: True if the signup process is successful, otherwise raises an exception.
        """
        pattern = r'http://email\.aparat\.com/ls/click\?upn=u001\.[^\s\]\)"\']+'
        match = re.search(pattern, url)

        if match:
            url = match.group()
        else:
            raise ValueError("No matching link found.")

        response = self.session.get(url, timeout=timeout)
        guid = response.text.split('guid: "')[1].split('",')[0]
        additionalget = response.text.split('additionalGet: "')[1].split('",')[0]
        code = response.text.split('?code=')[1].split('&account=')[0]

        json_data = {
            'type': 'email',
            'code': code,
            'account': account,
            'guid': guid
        }
        response = self.session.post(f'https://www.aparat.com/api/fa/v1/user/Authenticate/signup_step2{additionalget}', json=json_data, timeout=timeout).json()

        temp_id = response['data']['attributes']['temp_id']
        json_data = {
            'type': 'email',
            'code': code,
            'account': account,
            'pass': password,
            'temp_id': temp_id,
            'guid': guid,
        }
        response = self.session.post(f'https://www.aparat.com/api/fa/v1/user/Authenticate/signup_step2{additionalget}', json=json_data, timeout=timeout)
        self.is_logged_in = True
        self.username = account
        return True

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

    def get_my_videos(self, timeout: int = 10) -> list[MyVideo]:
        """
        Get my videos.

        This method retrieves the videos uploaded by the logged-in user by sending an HTTP GET request
        to the Aparat API. It returns a list of MyVideo objects representing the user's videos.

        Args:
            timeout (int, optional): The timeout for the HTTP request in seconds. Defaults to 10.

        Returns:
            list[MyVideo]: A list of MyVideo objects if successful, otherwise an empty list.

        Raises:
            LoginRequiredError: If the user is not logged in.
        """
        
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        response = self.session.get(f'{base_url}/api/fa/v1/user/video/videos', timeout=timeout)
        data = response.json()
        if response.status_code == 200 and 'included' in data:
            return [MyVideo(video, self.is_logged_in, self.session) for video in data['included']]
        return []

    def get_my_video(self, id: str = None, uid: str = None, timeout: int = 10) -> MyVideo:
        """
        Get a video by its ID or UID.

        Args:
            id (str, optional): The ID of the video.
            uid (str, optional): The UID of the video.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).

        Returns:
            MyVideo: The video object.

        Raises:
            ValueError: If neither id nor uid is provided.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        if not id and not uid:
            raise ValueError("At least one of 'id' or 'uid' must be provided.")
        
        response = self.session.get(f'{base_url}/api/fa/v1/user/video/videos', timeout=timeout)
        data = response.json()
        if response.status_code == 200 and data.get('included'):
            for video in data['included']:
                if id:
                    if str(video['id']) == str(id):
                        return MyVideo(video, self.is_logged_in, self.session)
                elif uid:
                    if video['attributes']['uid'] == uid:
                        return MyVideo(video, self.is_logged_in, self.session)
        return None

    def get_comment(self, uid: str, comment_id: str, timeout: int = 10) -> Comment:
        """
        Get information about a comment by their username.

        :param uid: The UID of the video.
        :param comment_id: The ID of the comment.
        :param timeout: The timeout for the HTTP request (default is 10 seconds).
        :return: A Comment object containing comment information if successful.
        :raises ValueError: If the comment is not found.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/video/comment/list/videohash/{uid}?perpage=100', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            for comment in data['data']:
                if comment['id'] == comment_id:
                    return Comment(comment['attributes'], uid, self.is_logged_in, self.session)
            while 'links' in data and 'more' in data['links'] and data['links']['more']:
                response = self.session.get(f"{data['links']['more']}&perpage=100", timeout=timeout)
                data = None
                if response.status_code == 200:
                    data = response.json()
                    for comment in data['data']:
                        if comment['id'] == comment_id:
                            return Comment(comment['attributes'], uid, self.is_logged_in, self.session)
        raise ValueError('No comment found.')

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

    def get_video(self, uid: str, timeout: int = 10) -> Video:
        """Get video details from Aparat.
        
        Args:
            uid (str): The video UID.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).
        
        Returns:
            Video: An instance of the Video class representing the video.
        
        Raises:
            VideoNotFoundError: If the requested video is not found.
        """
        response = self.session.get(f'{base_url}/api/fa/v1/video/video/show/videohash/{uid}?pr=1&mf=1', timeout=timeout)
        data = response.json()

        if 'meta' in data and 'status' not in data['meta']:
            return Video(data, self.is_logged_in, self.session)
        else:
            raise VideoNotFoundError()

    def get_playlist(self, playlist_id: int, timeout: int = 10) -> Playlist:
        """Get playlist details from Aparat.
        
        Args:
            playlist_id (int): The ID of the playlist to retrieve.
            timeout (int, optional): The timeout for the request in seconds. Defaults to 10.
        
        Returns:
            Playlist: An instance of the Playlist class containing the details of the requested playlist.
        
        Raises:
            ValueError: If the playlist with the given ID is not found.
        
        Example:
            >>> client = Aparat()
            >>> playlist = client.get_playlist(12345)
            >>> print(playlist.title)
        """
        response = self.session.get(f'{base_url}/api/fa/v1/video/playlist/one/playlist_id/{playlist_id}', timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return Playlist(data, self.is_logged_in, self.session)
        else:
            raise ValueError('There is no playlist with this ID.')

    # import chardet
    # def __fetch_csrf_tokens(self, retries: int = 6, timeout: int = 10):
    #     for attempt in range(retries):
    #         try:
    #             response = self.session.get(f'{base_url}/upload', timeout=timeout)
    #             detected_encoding = chardet.detect(response.content)['encoding']
    #             response.encoding = detected_encoding

    #             csrf_name = response.text.split("name='csrf_name' value='")[1].split("'")[0]
    #             csrf_value = response.text.split("name='csrf_value' value='")[1].split("'")[0]
                
    #             # Return the csrf tokens if successful
    #             return csrf_name, csrf_value
    #         except:
    #             print(f"Attempt {attempt + 1} failed.")
    #             if attempt == retries - 1:
    #                 raise ValueError("All attempts failed.")

    def __generate_unique_uuid(self, timeout: int = 10) -> str:
        """
        Generates a unique UUID that does not already exist on the server.

        :return: A unique UUID.
        """
        while True:
            new_uuid = str(uuid.uuid4())
            check_url = f'{upload_base_url}/chunks/{new_uuid}'
            response = self.session.head(check_url, timeout=timeout)
            
            if response.status_code == 404:
                return new_uuid

    def upload_video(self, video: str, title: str, category: VideoCategory, tag_list: list, comment: str = 'yes', watermark: bool = True, inappropriate_child_content: bool = False, thumbnail: str = '', description: str = '', retries: int = 6, timeout: int = 10) -> MyVideo:
        """Uploads a video to Aparat.

        Args:
            video (str): The path to the video file to be uploaded.
            title (str): The title of the video.
            tag_list (list): A list of tags for the video.
            comment (str, optional): Specifies whether comments are allowed on the video. Possible values are 'yes', 'approve', or 'no'. Defaults to 'yes'.
            watermark (bool, optional): Indicates whether to apply a watermark to the video. Defaults to True.
            inappropriate_child_content (bool, optional): Specifies whether the video contains inappropriate content for children. Defaults to False.
            thumbnail (str, optional): The path to the thumbnail image for the video. Defaults to ''.
            description (str, optional): The description of the video. Defaults to ''.
            retries (int, optional): The number of retries for uploading. Defaults to 6.
            timeout (int, optional): The timeout for each HTTP request in seconds. Defaults to 10.

        Returns:
            MyVideo: An object representing the uploaded video.

        Raises:
            FileNotFoundError: If the specified file or thumbnail does not exist.
            ValueError: If there are errors during the upload process.
        """
        
        # Check if the file exists
        if not os.path.isfile(video):
            raise FileNotFoundError(f"The file at path {video} does not exist.")
        
        # Check if thumbnail exists
        if thumbnail and not os.path.isfile(thumbnail):
            raise FileNotFoundError(f"The file at path {thumbnail} does not exist.")
        
        # Set thumbnail to empty string if not provided
        if not thumbnail:
            thumbnail = ''

        # Determine file MIME type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(video)

        # Get upload URL from Aparat API
        json_data = {
            'uploadIds': [0],
            'upload_base_url': upload_base_url,
            'upload_cnt': 1
        }
        response = self.session.post(f'{base_url}/api/fa/v1/video/upload/upload_url', json=json_data, timeout=timeout)
        data = response.json()

        # Get file size
        size = os.path.getsize(video)

        # Prepare headers for upload request
        headers = {'x-token': data['data'][0]['attributes']['token']}
        uploadId = data['data'][0]['attributes']['uploadId']
        uuid_ = self.__generate_unique_uuid(timeout)

        # Prepare files for upload
        files = {
            'qqpartindex': (None, '0'),
            'qqchunksize': (None, size),
            'qqpartbyteoffset': (None, '0'),
            'qqtotalfilesize': (None, size),
            'qqtype': (None, mime_type),
            'qquuid': (None, uuid_),
            'qqfilename': (None, video),
            'qqfilepath': (None, video),
            'qqtotalparts': (None, '1'),
            'qqfile': (video, open(video, 'rb'), 'application/octet-stream')
        }

        # Upload video file
        response = requests.post(f'{upload_base_url}/upload', headers=headers, files=files)

        # If upload is successful
        if response.json()['success']:
            requests.post(f'{upload_base_url}/file/{uuid_}', timeout=timeout)

            # Notify server that upload chunks are done
            data = {
                'qquuid': uuid_,
                'qqfilename': video,
                'qqtotalfilesize': size,
                'qqtotalparts': '1'
            }
            requests.post(f'{upload_base_url}/chunksdone', headers=headers, data=data, timeout=timeout)

            # Prepare thumbnail data if provided
            if thumbnail:
                with open(thumbnail, "rb") as file:
                    image_content = file.read()
                    image_base64 = base64.b64encode(image_content).decode('utf-8')

                thumbnail = f'data:image/jpeg;base64,{image_base64}'

            # Prepare JSON data for video metadata
            json_data = {
                'uploadId': uploadId,
                'video': uuid_,

                'watermark': '1' if watermark else '0',
                'watermark_bool': watermark,
                'comment': comment,  # 'yes', 'approve', 'no'
                'kids_friendly': inappropriate_child_content,
                'title': title,
                'descr': description,
                'thumbnail': thumbnail,
                'tags': '-'.join(tag_list),
                'category': category.value if type(category) == VideoCategory else category,
                'upload_base_url': upload_base_url,

                'new_playlist': '',
                'playlist_temp': '',
                'playlistid': [],
                'subtitle': [],
                'subtitle_temp': [],
                'publish_date': '',
                'video_pass': 0,
            }

            # Upload video metadata
            response = self.session.post(f'{base_url}/api/fa/v1/video/upload/upload/uploadId/{uploadId}', json=json_data, timeout=timeout)
            data = response.json()
            if 'data' in data:
                return self.get_my_video(id=data['data']['id'])
            else:
                raise ValueError(data)

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
        
        with open(f'{self.username}.session', 'wb') as file:
            pickle.dump(self.session, file)

    def load_session(self, username: str, timeout: int = 10) -> bool:
        """
        Load the session object from a file.
        
        Args:
            username (str): The username of the account.
            timeout (int, optional): The timeout for the HTTP request (default is 10 seconds).
            
        Returns:
            bool: True if the session is successfully loaded and the user is logged in, False otherwise.
        """
        with open(f'{username}.session', 'rb') as file:
            session = pickle.load(file)

            response = session.get(f'{base_url}/api/fa/v1/etc/page/config/mode/full', timeout=timeout)
            if response.json()['included'][0]['attributes']:
                self.session = session
                self.is_logged_in = True
                self.username = username
                return True
            else:
                return False
    
    def get_AuthV1(self) -> str:
        """
        Get the AuthV1 cookie.

        Raises:
            LoginRequiredError: If the client is not logged in.

        Returns:
            str: The value of the AuthV1 cookie.
        """
        if not self.is_logged_in:
            raise LoginRequiredError()
        
        return self.session.cookies.get('AuthV1')

    def load_AuthV1(self, AuthV1: str, timeout: int = 10) -> bool:
        """
        Load the AuthV1 cookie.

        Args:
            AuthV1 (str): The value of the AuthV1 cookie.
            timeout (int, optional): The timeout for the server request. Defaults to 10 seconds.

        Returns:
            bool: `True` if the cookie is loaded successfully, otherwise `False`.
        """
        cookies = {'AuthV1': AuthV1}

        response = requests.get(f'{base_url}/api/fa/v1/user/user/information', cookies=cookies, timeout=timeout)
        data = response.json()
        if response.status_code == 200:
            self.session.cookies.set('AuthV1', AuthV1)
            self.is_logged_in = True
            self.username = data['data']['attributes']['email'] if data['data']['attributes']['has_email'] else data['data']['attributes']['username']
            return True
        else:
            return False
