import argparse
import os
import json
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable


def _start_file_watcher(folder: str, stop_file: str, callback: Callable[[str], None], file_extensions: list[str], timeout: int = 120000, debug: bool = False) -> None:
    """
    Spawn a thread to watch a folder for file changes. Thread contains a while loop that runs the callback on the most recent file in the folder.

    Parameters:
        - folder: The folder to watch for file changes.
        - stop_file: The file that will be created should the file watcher throw an error.
        - callback: Callback function that will be looped upon.
        - file_extensions: A list of file extensions that the file watcher will check for.
        - timeout: The number of seconds to wait before exiting if no files are present in the folder.
    """
    def process():
        last_populate_time = time.time()
        last_processed_file = None

        file_extension_tuple = tuple(file_extensions)

        while True:
            sorted_files = None
            try:
                with os.scandir(folder) as entries:
                    # Sort by modified time, oldest first, newest last
                    sorted_files = sorted((entry for entry in entries if entry.name.lower(
                    ).endswith(file_extension_tuple)), key=lambda entry: entry.stat().st_mtime)
            except FileNotFoundError as error:
                if debug:
                    print(f"start_file_watcher: {error}")
                continue

            if len(list(sorted_files)) == 0:
                if time.time() - last_populate_time > timeout:
                    error_msg = f"Folder {folder} is empty and has not been populated for {timeout} seconds"
                    exit_plugin_on_error(error_msg, stop_file)
                else:
                    continue

            jpeg_file = sorted_files.pop()
            if last_processed_file is not None and jpeg_file.path == last_processed_file.path and jpeg_file.stat().st_mtime == last_processed_file.stat().st_mtime:
                continue
            last_processed_file = jpeg_file

            jpeg_path = jpeg_file.path
            callback(jpeg_path)

            last_populate_time = time.time()

    # Setup processing thread
    processing_thread = threading.Thread(
        target=process, args=())
    processing_thread.daemon = True
    processing_thread.start()
    print(f"File watcher started on folder: {folder}")


def start_image_watcher(folder: str, stop_file: str, callback: Callable[[str], None], timeout: int = 120000, debug: bool = False) -> None:
    """
    Spawn a thread to watch a folder for image (.jpeg and .jpg) file changes. Thread contains a while loop that runs the callback on the most recent file in the folder.

    Parameters:
        - folder: The folder to watch for file changes.
        - stop_file: The file that will be created should the file watcher throw an error.
        - callback: Callback function that will be looped upon.
        - timeout: The number of seconds to wait before exiting if no files are present in the folder.
    """
    file_extensions = ['.jpeg', '.jpg']
    _start_file_watcher(folder, stop_file, callback,
                        file_extensions, timeout, debug)


def start_json_watcher(folder: str, stop_file: str, callback: Callable[[str], None], timeout: int = 120000, debug: bool = False) -> None:
    """
    Spawn a thread to watch a folder for json file changes. Thread contains a while loop that runs the callback on the most recent file in the folder.

    Parameters:
        - folder: The folder to watch for file changes.
        - stop_file: The file that will be created should the file watcher throw an error.
        - callback: Callback function that will be looped upon.
        - timeout: The number of seconds to wait before exiting if no files are present in the folder.
    """
    file_extensions = ['.json']
    _start_file_watcher(folder, stop_file, callback,
                        file_extensions, timeout, debug)


class StopFileHandler(FileSystemEventHandler):
    def __init__(self, stop_file):
        self.stop_file = stop_file

    def on_created(self, event):
        if event.src_path == self.stop_file:
            msg = 'Stop file detected'
            print(msg)
            os._exit(0)


def start_stop_file_watcher(stop_file: str):
    """
    Spawn a thread to watch for a stop file and gracefully exit when the stop file exists.

    Parameters:
    - stop_file: The stop file to watch for.

    :return: The stop file watcher thread.
    """

    stop_folder = os.path.dirname(stop_file)

    stop_file_handler = StopFileHandler(stop_file)
    stop_observer = Observer()
    stop_observer.schedule(stop_file_handler, stop_folder)
    stop_observer.start()
    print(f"Stop file watcher started for {stop_file}")

    return stop_observer


def join_stop_file_watcher(stop_observer):
    """
    Join the stop file watcher thread.

    Parameters:
    - stop_observer: The stop file watcher thread.
    """

    stop_observer.join()


def exit_plugin_on_error(msg: str, stop_file: str) -> None:
    """
    Exit the plugin with an error message.

    Parameters:
    - msg: The error message.
    - stop_file: The stop file to write the error message to.
    """

    print(msg)
    with open(stop_file, 'w') as file:
        json.dump({'error': msg}, file)
    exit(1)


def write_string_to_file(data: str, file: str) -> None:
    """
    Write a string to a file.

    Parameters:
      - data: The string to write.
      - file: The file to write to.
    """
    with open(file, 'w') as f:
        f.write(data)

    os.chmod(file, 0o777)


def parse_args():
    """
    Parse command-line arguments.

    :return: The parsed command-line arguments.

    Example:
        ```
        args = parse_args()
        request_file = args.request_file
        result_folder = args.result_folder
        result_file = args.result_file
        stop_file = args.stop_file
        input_channel_folder = args.input_channel_folder
        output_channel_folder = args.output_channel_folder
        telemetry_stream_folder = args.telemetry_stream_folder
        ```
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--request-file', dest='request_file',
                        help='The PlugInRequest json')
    parser.add_argument('--result-folder', dest='result_folder',
                        help='The folder that will be zipped and then backed up to the bucket')
    parser.add_argument('--result-file', dest='result_file',
                        help='The result file json that will be backed up to the bucket')
    parser.add_argument('--stop-file', dest='stop_file',
                        help='Location of the file to monitor/write the stop file')
    parser.add_argument('--input-channel-folder', dest='input_channel_folder',
                        help='Input channel folder that contains channel sub folders')
    parser.add_argument('--output-channel-folder', dest='output_channel_folder',
                        help='Output channel folder that contains channel sub folders')
    parser.add_argument('--telemetry-stream-folder', dest='telemetry_stream_folder',
                        help='Telemetry stream folder that contains telemetry stream sub folders')

    args = parser.parse_args()

    if not (args.request_file and args.result_folder and args.result_file and args.stop_file and args.input_channel_folder and args.output_channel_folder and args.telemetry_stream_folder):
        error_msg = 'Missing required arguments'
        exit_plugin_on_error(error_msg, args.stop_file)

    return args
