# AdsPower Cache Cleanup Script

This Python script monitors a specified directory and deletes its contents if the total size exceeds a defined limit. The script uses the `watchdog` library to observe changes in the directory and periodically checks the folder size. If the folder size exceeds the limit, it clears all folders except for a specified exempt file.

## Features

- Monitors a specified directory for changes.
- Periodically checks the total size of the directory.
- Deletes folders and their contents if the total size exceeds the defined limit.
- Exempts a specified file from deletion.
- Logs actions and errors to a log file with timestamps.

## Prerequisites

- Python 3.x
- `watchdog` library

## Installation

1. Install Python 3.x if you don't already have it.
2. Install the `watchdog` library:
   ```sh
   pip install watchdog
   ```

## Usage

1. Place the script in your project folder.
2. Update the `folder_path`, `exempt_filename`, `max_size`, and `check_interval` variables in the script as needed.
3. Run the script:
   ```sh
   python main.py or py main.py
   ```

## Script Configuration

- `folder_path`: The path to the directory to be monitored.
- `exempt_filename`: The name of the file that should not be deleted.
- `max_size`: The maximum allowed size of the directory in bytes (e.g., 1 MB = 1 * 1024 * 1024 bytes).
- `check_interval`: The interval in seconds at which the folder size is checked.

## Example

```python
folder_path = r'C:\.ADSPOWER_GLOBAL\cache'  # Replace with your folder path
exempt_filename = 'cache_time'  # File that should not be deleted
max_size = 200 * 1024 * 1024 * 1024  # 200 GB in bytes
check_interval = 60  # Interval to check folder size in seconds

monitor_folder(folder_path, exempt_filename, max_size, check_interval)
```

## Logging

The script logs its actions and any errors to a file named `folder_cleanup.log` in the project directory. Each log entry includes a timestamp, log level, and message.

## Error Handling

- Skips files or folders that cannot be deleted due to permission issues.
- Logs errors to the log file for further analysis.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [watchdog](https://pypi.org/project/watchdog/) library for monitoring file system events.

---

By following the above instructions, you should be able to set up and run the cache cleanup script to monitor and manage your directory effectively.
