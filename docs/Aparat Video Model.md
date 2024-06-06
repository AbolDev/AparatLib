# Aparat Video Model

The `Video` class represents a video on Aparat and provides methods to interact with the video, such as liking, reporting, and downloading.

## Attributes

- `id` (int): The ID of the video.
- `title` (str): The title of the video.
- `description` (str): The description of the video.
- `uid` (str): The UID of the video.
- `visit_cnt` (int): The visit count of the video.
- `visit_cnt_non_formatted` (int): The non-formatted visit count of the video.
- `like_cnt_non_formatted` (int): The non-formatted like count of the video.
- `big_poster` (str): The URL of the big poster of the video.
- `medium_poster` (str): The URL of the medium poster of the video.
- `small_poster` (str): The URL of the small poster of the video.
- `duration` (str): The duration of the video.
- `meta_duration` (str): The meta duration of the video.
- `date_exact` (str): The exact date of the video.
- `sdate` (str): The sdate of the video.
- `sdate_timediff` (int): The time difference of the video.
- `sdate_real` (str): The real sdate of the video.
- `deleted` (str): The deleted status of the video.
- `mdate` (str): The mdate of the video.
- `file_link_all` (List[Dict[str, Union[str, List[str]]]]): List of dictionaries containing file links and their details.
- `file_link` (str): The file link of the video.
- `hls_link` (str): The HLS link of the video.
- `can_download` (bool): The download status of the video.
- `tags` (str): The tags of the video.
- `tags_str` (str): The string representation of tags of the video.
- `tags_fa` (List[str]): The Persian tags of the video.
- `frame_src` (str): The frame source of the video.
- `category` (str): The category of the video.
- `_360d` (str): The 360d status of the video.
- `comment_enable` (str): The comment enable status of the video.
- `official` (str): The official status of the video.
- `extra_data` (str): The extra data of the video.
- `content_type` (str): The content type of the video.
- `file_hash` (str): The file hash of the video.
- `isCompany` (str): The company status of the video.
- `isAbroad` (str): The abroad status of the video.
- `kids_friendly` (str): The kids friendly status of the video.
- `owner_username` (str): The owner's username of the video.
- `max_width` (str): The maximum width of the video.
- `max_height` (str): The maximum height of the video.

## Methods

### `__init__(data: Dict[str, Union[str, int]], is_logged_in, session)`

Initialize a Video object.

- `data`: Dictionary containing video data.
- `is_logged_in`: Boolean indicating whether the user is logged in.
- `session`: Session object for making HTTP requests.

### `send_comment(comment: str, timeout: int = 10) -> Comment`

Send a comment for this video.

- `comment` (str): The comment to be sent.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).

### `like(timeout: int = 10) -> bool`

Like a video.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: True if the video is successfully liked, False otherwise.

### `unlike(timeout: int = 10) -> bool`

Unlike a video.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: True if the video is successfully unliked, False otherwise.

### `download(resolution: str = None, download_highest_resolution: bool = None, path: str = None, chunk_size: int = 1024 * 1024 * 4) -> str`

Download the video with the specified resolution.

- `resolution` (str, optional): The desired video resolution (e.g., '144p', '720p').
- `download_highest_resolution` (bool, optional): If True, download the highest available resolution.
- `path` (str, optional): The path where the video will be saved. Defaults to the video's name.
- `chunk_size` (int, optional): The size of chunks to download at a time (default is 4 MB).

### `report(reason: ReportReason, main_time: str = '', main_time1: str = '', main_time2: str = '', body: str = None, timeout: int = 10) -> Union[str, bool]`

Report the video for a specified reason.

- `reason` (str, optional): The reason for reporting the video.
- `main_time` (str, optional): The main time point of the issue in the video.
- `main_time1` (str, optional): An additional time point of the issue in the video.
- `main_time2` (str, optional): Another additional time point of the issue in the video.
- `body` (str, optional): Additional details about the report.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - Union[str, bool]: A success message if the report is successful, False otherwise.

### `follow(toggle_push_notifications: bool = False, timeout: int = 10) -> bool`

Follow a user.

- `toggle_push_notifications` (bool): A boolean indicating whether to toggle push notifications for the followed user.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: True if the user is successfully followed, False otherwise.

### `unfollow(timeout: int = 10) -> bool`

Unfollow a user.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: True if the user is successfully unfollowed, False otherwise.

### `republish(timeout: int = 10) -> MyVideo`

Republish video.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - MyVideo: The republished video object.

### `get_my_video(id: str = None, uid: str = None, timeout: int = 10) -> MyVideo`

Get a video by its ID or UID.

- `id` (str, optional): The ID of the video.
- `uid` (str, optional): The UID of the video.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).

- Returns:
    - MyVideo: The video object corresponding to the provided ID or UID. If neither id nor uid is provided, returns None.
