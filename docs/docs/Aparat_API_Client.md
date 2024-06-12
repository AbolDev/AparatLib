# Aparat API Client

## Attributes:
- `proxy` (dict): The proxy dictionary, if used.
- `session` (requests.Session): The requests session object.
- `is_logged_in` (bool): Flag indicating if the client is logged in.

## Methods:

### `__init__(proxy: Union[None, dict] = None)`
Initialize Aparat API client.

- `proxy` (dict, optional): The proxy configuration dictionary. Defaults to None.

### `login(username: str, password: str, timeout: int = 10) -> bool`
Log in to the Aparat account.

- `username` (str): The username of the Aparat account.
- `password` (str): The password of the Aparat account.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - `True` if login is successful, otherwise `False`.

### `signup_step1(self, account: str) -> bool`
Perform the first step of the signup process.

- `account` (str): The account identifier (email or phone number).
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A dictionary containing user information if successful, otherwise `None`.

### `signup_step2(self, url: str, account: str, password: str, timeout: int = 10) -> bool`
Perform the second step of the signup process using the verification link.

- `url` (str): The URL or email text containing the signup confirmation link.
- `account` (str): The account identifier (email or phone number).
- `password` (str): The password for the new account.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: `True` if the signup process is successful, otherwise raises an exception.

### `get_me(timeout: int = 10) -> Union[Dict, None]`
Get information about the current user.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A dictionary containing user information if successful, otherwise `None`.

### `get_user(user_id: str, timeout: int = 10) -> User`
Get information about a user by their username.

- `user_id` (str): The username of the user.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A `User` object containing user information if successful, otherwise `None`.

### `get_my_videos(timeout: int = 10) -> list[MyVideo]`
Get my videos.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A list of `MyVideo` objects representing the user's videos.

### `get_my_video(id: str = None, uid: str = None, timeout: int = 10) -> MyVideo`
Get a video by its ID or UID.

- `id` (str, optional): The ID of the video.
- `uid` (str, optional): The UID of the video.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - The `MyVideo` object representing the video.

### `get_comment(vid: str, comment_id: str, timeout: int = 10) -> Comment`
Get information about a comment by its ID.

- `vid` (str): The video ID.
- `comment_id` (str): The comment ID.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - The `Comment` object representing the comment.

### `notifications(timeout: int = 10) -> Union[Dict, None]`
Get notifications for the current user.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A dictionary containing notifications if successful, otherwise `None`.

### `dashboard(timeout: int = 10) -> Union[Dict, None]`
Get the dashboard for the current user.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - A dictionary containing the user's dashboard if successful, otherwise `None`.

### `get_video(vid: str, timeout: int = 10) -> Video`
Get video details from Aparat.

- `vid` (str): The video ID.
- `timeout` (int, optional): The request timeout (default is 10).
- Returns:
    - An instance of the `Video` class representing the video.

### `get_playlist(self, playlist_id: int, timeout: int = 10) -> Playlist`
Get playlist details from Aparat.

- `playlist_id` (int): The ID of the playlist to retrieve.
- `timeout` (int, optional): The request timeout (default is 10).
- Returns:
    - An instance of the `Playlist` class containing the details of the requested playlist.
- Raises:
    - `ValueError`: If the playlist with the given ID is not found.

### `upload_video(video: str, title: str, category: VideoCategory, tag_list: list, comment: str = 'yes', watermark: bool = True, inappropriate_child_content: bool = False, thumbnail: str = '', description: str = '', retries: int = 6, timeout: int = 10) -> MyVideo`
Uploads a video to Aparat.

- `video` (str): The path to the video file to be uploaded.
- `title` (str): The title of the video.
- `category` (VideoCategory): The category of the video.
- `tag_list` (list): A list of tags for the video.
- `comment` (str, optional): Specifies whether comments are allowed on the video. Possible values are 'yes', 'approve', or 'no'. Defaults to 'yes'.
- `watermark` (bool, optional): Indicates whether to apply a watermark to the video. Defaults to True.
- `inappropriate_child_content` (bool, optional): Specifies whether the video contains inappropriate content for children. Defaults to False.
- `thumbnail` (str, optional): The path to the thumbnail image for the video. Defaults to ''.
- `description` (str, optional): The description of the video. Defaults to ''.
- `retries` (int, optional): The number of retries for uploading. Defaults to 6.
- `timeout` (int, optional): The timeout for each HTTP request in seconds. Defaults to 10.
- Returns:
    - An object representing the uploaded video.

### `logout() -> None`
Log out from the Aparat account.

### `save_session() -> None`
Save the session object to a file.

### `load_session(username: str, timeout: int = 10) -> bool`
Load the session object from a file.

- `username` (str): The username of the account.
- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: `True` if the session is successfully loaded and the user is logged in, `False` otherwise.

### `get_AuthV1(self) -> str`
Get the AuthV1 cookie.

- Returns:
    - The value of the AuthV1 cookie.

### `load_AuthV1(self, AuthV1: str, timeout: int = 10) -> bool`
Load the AuthV1 cookie.

- `AuthV1` (str): The value of the AuthV1 cookie.
- `timeout` (int, optional): The request timeout (default is 10).
- Returns:
    - `True` if the cookie is loaded successfully, otherwise `False`.
