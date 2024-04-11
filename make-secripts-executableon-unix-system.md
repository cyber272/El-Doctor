## To make the Python scripts (`monitoring_tool.py`) executable on Unix-like systems (such as Linux or macOS), follow these steps:

### 1. Add Shebang Line:
At the top of each Python script, add a shebang line (`#!`) followed by the path to the Python (`whitch python3`) interpreter. This line tells the system which interpreter to use when executing the script.

#### Determine Python Interpreter Path:
```bash
which python3
```
```commandline
/sur/bin/python3
```


#### Example for `monitoring_tool.py`:
```python
#!/usr/bin/python3
import psutil
import csv
import curses
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Rest of your script...
```
#### Verify Shebang Line:
- head -n 1 monitoring_tool.py

### 2. Set Execute Permission:
Set the (`+x`) on the script files to make them executable.

```bash
sudo chmod +x monitoring_tool.py dashboard.py
```

### 3. Running the Scripts:

```bash
./monitoring_tool.py
```

### Notes: 
- Ensure that the shebang line is correctly set to the path of your Python interpreter (`#!/usr/bin/python3` for Python 3).
- Make sure the email settings is present and accessible in your scripts.
- If you encounter any issues with permissions, ensure that you have the necessary permissions to modify file permissions (`chmod`) in your environment.

By following these steps, you'll be able to execute your Python monitoring scripts (`monitoring_tool.py`) directly from the terminal as executable files on Unix-like systems.