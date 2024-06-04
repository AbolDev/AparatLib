# Aparat

A Python library to interact with the Aparat API.

## Installation

```bash
pip install AparatLib
```

## Login & save session

```python
from aparat import Aparat

aparat = Aparat()
if aparat.login('your_username', 'your_password'):
    print("Login successful")
    aparat.save_session()
    print("Session saved successfully.")
else:
    print("Login failed.")

```

## Video

```python
from aparat import Aparat

aparat = Aparat()
if aparat.load_session('your_username'):
    print("Session loaded successfully.")

    video = aparat.get_video('m98gm8j')
    
    # Send a comment
    print(video.send_comment('Hello World!'))

    # Like the video
    print(video.like())

    # Unlike the video
    print(video.unlike())

    # Download video with 480p resolution
    video_path = video.download('480p')
    print("Video path: ", video_path)
else:
    print("Login failed.")
```

## User

```python
from aparat import Aparat

aparat = Aparat()
if aparat.load_session('your_username'):
    print("Session loaded successfully.")

    user = aparat.get_user('aparat')
    
    # Follow the user
    print(user.follow())

    # Unfollow the user
    print(user.unfollow())
else:
    print("Login failed.")
```
