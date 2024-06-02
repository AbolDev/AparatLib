# Aparat

A Python library to interact with the Aparat API.

## Installation

```bash
pip install AparatLib
```

## Login

```python
from aparat import Aparat

def main():
    aparat = Aparat()
    login = aparat.login('aparat', 'your_password')
    if login:
        print("Login successful")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
```
