# My Videos Management

The `MyVideo` class represents a video on Aparat and provides methods to interact with the video, such as deleting it.

## Attributes

- `id` (str): The unique identifier of the user.
- `uid` (str): The unique identifier of the video.
- `hash_user_id` (str): The hashed identifier of the user.
- `afcn` (str): The user's name in a format suitable for related publications.
- `username` (str): The username of the user.
- `name` (str): The name of the user.
- `pic_s` (str): The URL of the small profile picture of the user.
- `pic_m` (str): The URL of the medium profile picture of the user.
- `pic_b` (str): The URL of the large profile picture of the user.
- `follower_cnt` (int): The number of followers of the user.
- `follow_cnt` (int): The number of users that the user follows.
- `official` (str): The official status of the user.
- `url` (str): The URL of the user's profile.
- `video_cnt` (int): The number of videos uploaded by the user.
- `cover_src` (str): The URL of the user's cover image.
- `video_visit` (int): The number of visits to the user's videos.
- `priority` (str): The priority of the user.
- `brand_priority` (str): The brand priority of the user.
- `description` (str): The description of the user.
- `start_date` (str): The start date of the user's activity.
- `start_date_jalali` (str): The start date of the user's activity in the Jalali calendar.
- `show_kids_friendly` (str): The display of a suitable label for children.
- `banned` (str): The banned status of the user.
- `has_event` (str): The event status of the user.

## Methods

### `__init__(data: Dict[str, Union[str, int]], is_logged_in, session)`

Initialize a MyVideo object.

- `data`: Dictionary containing video data.
- `is_logged_in`: Boolean indicating whether the user is logged in.
- `session`: Session object for making HTTP requests.

### `delete(timeout: int = 10) -> bool`

Deletes the video.

This method deletes a video by sending an HTTP GET request to the appropriate delete URL. The method checks if the user is logged in and if the delete URL is available.

- `timeout` (int, optional): The timeout for the HTTP request in seconds. Defaults to 10.

- Returns:
    - bool: True if the video is successfully deleted, False otherwise.

- Raises:
    - LoginRequiredError: If the user is not logged in.
    - ValueError: If neither 'share_delete_url' nor 'delete_url' is available.
