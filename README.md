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
