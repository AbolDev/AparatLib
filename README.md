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
    if aparat.login('your_username', 'your_password'):
        print("Login successful")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
```

For the complete documentation, you can visit this [**GitHub link**](https://github.com/AbolDev/AparatLib).
