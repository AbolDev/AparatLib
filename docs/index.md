# AparatLib
---
A library for interacting with the Aparat API.

## Installation
---
```bash
pip install AparatLib
```

# Usage
---
## Login & save session
---
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

1. [Aparat API Client](Aparat%20API%20Client.md)
2. [Aparat Comment Model](Aparat%20Comment%20Model.md)
3. [Aparat MyVideo Model](Aparat%20MyVideo%20Model.md)
4. [Aparat User Model](Aparat%20User%20Model.md)
5. [Aparat Video Model](Aparat%20Video%20Model.md)
6. [Errors and Enums](Errors%20and%20Enums.md)
