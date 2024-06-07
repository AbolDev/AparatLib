# User Interactions

## Attributes:
- `id` (str): The unique identifier of the user.
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

## Methods:

### `follow(toggle_push_notifications: bool = False, timeout: int = 10) -> bool`
Follow a user.

- `toggle_push_notifications` (bool, optional): A boolean indicating whether to toggle push notifications for the followed user. Default is `False`.
- `timeout` (int, optional): The timeout for the HTTP request. Default is 10 seconds.
- Returns:
    - `True` if the user is successfully followed, `False` otherwise.

### `unfollow(timeout: int = 10) -> bool`
Unfollow a user.

- `timeout` (int, optional): The timeout for the HTTP request. Default is 10 seconds.
- Returns:
    - `True` if the user is successfully unfollowed, `False` otherwise.
