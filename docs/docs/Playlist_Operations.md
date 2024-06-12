# Playlist Operations

The `Playlist` class represents a playlist on Aparat and provides methods to interact with and manage the playlist.

## Attributes

- `id` (int): The ID of the playlist.
- `title` (str): The title of the playlist.
- `description` (str): The description of the playlist.
- `cnt` (int): The count of videos in the playlist.
- `big_poster` (str): The URL of the big poster image.
- `small_poster` (str): The URL of the small poster image.
- `uid` (str): The unique identifier of the playlist.
- `toggle_url` (str): The URL for toggling the playlist state.
- `publish_type` (str): The publish type of the playlist.
- `create_type` (str): The creation type of the playlist.
- `checked` (bool): The checked status of the playlist.
- `order` (int): The order of the playlist.
- `last_update` (str): The last update timestamp of the playlist.
- `isYours` (bool): Flag indicating if the playlist belongs to the user.
- `playlist_follow_link` (str): The URL for following the playlist.
- `playlist_follow_status` (str): The follow status of the playlist.
- `list_videos_playlist` (list): The list of videos in the playlist.
- `videos` (list[Video]): The list of Video objects in the playlist.

## Methods

### `__init__(self, data: Dict[str, Union[str, int]], is_logged_in, session, timeout: int = 10)`

Initializes a `Playlist` object with the provided data.

- `data`: A dictionary containing the raw data for the playlist.
- `is_logged_in`: Boolean indicating whether the user is logged in.
- `session`: Session object for making HTTP requests.
- `timeout` (int, optional): The timeout for the HTTP requests (default is 10 seconds).

### `follow_playlist(self, timeout: int = 10) -> bool`

Follow the playlist.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: `True` if the playlist was successfully followed, `False` otherwise.
- Raises:
    - `LoginRequiredError`: If the user is not logged in.

### `unfollow_playlist(self, timeout: int = 10) -> bool`

Unfollow the playlist.

- `timeout` (int, optional): The timeout for the HTTP request (default is 10 seconds).
- Returns:
    - bool: `True` if the playlist was successfully unfollowed, `False` otherwise.
- Raises:
    - `LoginRequiredError`: If the user is not logged in.
