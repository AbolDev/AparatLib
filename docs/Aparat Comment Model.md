# Aparat Comment Model

The `Comment` class represents a comment on an Aparat video and provides methods to interact with the comment, such as liking, unliking, deleting, reporting, replying, and retrieving replies.

## Attributes

- `id` (str): Comment ID.
- `body` (str): Content of the comment.
- `reply` (str): Reply content if the comment is a reply to another comment.
- `sdate` (str): Submission date of the comment.
- `sdate_timediff` (str): Time difference since the comment was submitted.
- `sdate_gregorian` (str): Gregorian submission date of the comment.
- `replyAction` (str): Action link to reply to the comment.
- `replyDelete` (str): Action link to delete a reply to the comment.
- `text` (str): Text content of the comment.
- `type` (str): Type of the comment.
- `approve_link_text` (str): Text of the approval link.
- `approve_link_href` (str): Href of the approval link.
- `approved` (str): Approval status of the comment.
- `approve_raw` (str): Raw approval status of the comment.
- `isYours` (bool): Indicates if the comment is made by the logged-in user.
- `deleted` (bool): Indicates if the comment is deleted.
- `like_cnt` (int): Number of likes for the comment.
- `reply_cnt` (int): Number of replies to the comment.
- `mentioned_user_id` (str): ID of the mentioned user in the comment.
- `mentioned_name` (str): Name of the mentioned user in the comment.
- `need_approve` (bool): Indicates if the comment needs approval.
- `spam` (bool): Indicates if the comment is marked as spam.
- `is_pinned` (bool): Indicates if the comment is pinned.

## Methods

### `__init__(data: Dict[str, Union[str, int]], vid: int, is_logged_in: bool, session)`

Initialize a Comment object.

- `data`: Dictionary containing comment data.
- `vid`: ID of the associated video.
- `is_logged_in`: Boolean indicating whether the user is logged in.
- `session`: Session object for making HTTP requests.

### `like(timeout: int = 10) -> bool`

Like the comment.

- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: True if the comment is successfully liked, False otherwise.

### `unlike(timeout: int = 10) -> bool`

Unlike the comment.

- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: True if the comment is successfully unliked, False otherwise.

### `delete(timeout: int = 10) -> bool`

Delete the comment.

- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: True if the comment is successfully deleted, False otherwise.
- Raises:
  - `LoginRequiredError`: If the user is not logged in.
  - `ValueError`: If the comment does not have a delete URL.

### `report(timeout: int = 10) -> bool`

Report the comment.

- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: True if the comment is successfully reported, False otherwise.
- Raises: `ValueError` if the comment does not have a report URL.

### `reply_to_comment(body: str, timeout: int = 10) -> bool`

Reply to the comment.

- `body`: The content of the reply.
- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: True if the reply is successfully posted, False otherwise.

### `get_replies(timeout: int = 10) -> Union[Dict[str, Union[str, int]], bool]`

Get replies to the comment.

- `timeout`: Timeout for the HTTP request (default is 10 seconds).
- Returns: A dictionary containing reply data if replies exist, an empty list if there are no replies, or False if an error occurs.
