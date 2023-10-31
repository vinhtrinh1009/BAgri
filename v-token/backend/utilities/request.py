'''
Utility functions for working with requests
Contributors: 
    - minhdq99hp@gmail.com
'''
from __future__ import unicode_literals
from magic import from_buffer
import collections.abc
import io
import os
import traceback
from pathlib import Path
from time import sleep
from uuid import uuid4
from rest_framework.exceptions import ParseError

import requests
import magic
from datetime import datetime
# import youtube_dl
# from PIL import Image

# from utilities.image import convert_image


class RetryLimitExceededException(Exception):
    pass

def send_request(url, data={}, method='post', headers={}, timeout=60, max_retry=3, delay=0, silent=True, exc_msg=''):
    '''
    Send HTTP request to url with retry and delay if needed.

    The sending data should be json. Otherwise, you have to specific headers to send request. 

    If not silent:
        RetryLimitExceededException will be raised after max_retry retries.
    else:
        return None
    '''

    retry = 0
    while retry < max_retry:
        try:
            if isinstance(data, dict):
                res = requests.request(method, url, json=data, timeout=timeout, headers=headers)
            elif data is not None:
                res = requests.request(method, url, data=data, timeout=timeout, headers=headers)
            else:
                res = requests.request(method, url, timeout=timeout, headers=headers)
            return res
        except requests.exceptions.RequestException:
            traceback.print_exc()
            retry += 1
            sleep(delay)

    if not silent:
        raise RetryLimitExceededException(f"Unable to send request after {max_retry} retries.")

    return None


class UnexpectedFileFormat(Exception):
    pass

class NotSupportedType(Exception):
    pass

def download_file_from_url(url, expected_types=[], headers={}, timeout=None, output_dir='', filename=None):
    '''
    Download file and write it to output_path.

    Args:
        url (str): direct link of the file
        expected_type: the expected type of the file, must be specify to guess the extension.

    Return:
        dict: 
        {
            'status': 0 if success
            'mime_type': e.g. image/png, image/jpeg. Return None if the mime type can't be guessed.
            'path': the downloaded filepath.
        }
    '''
    if filename is None:
        filename = f'{uuid4()}'
    filepath = os.path.join(output_dir, filename)

    mime_type = ''
    media_type = 'undefined'

    result = {
        'status': 1,
        'path': filepath,
        'filename': filename,
        'type': media_type
    }
    buf = b''

    try:
        with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for i, chunk in enumerate(r.iter_content(chunk_size=8192)):
                    #if chunk: 
                    f.write(chunk)

                    if i == 0:
                        # get the first chunk to guess mime_type in the next step
                        buf = chunk
                
    except requests.exceptions.RequestException:
        traceback.print_exc()
        Path(filepath).unlink(missing_ok=True)
        return result

    try:
        mime_type = magic.from_buffer(buf, mime=True)
    except:
        mime_type = ''
    
    result['mime_type'] = mime_type if mime_type else None

    # correct the filename with the guessed extension
    if mime_type.startswith(('video/', 'image/', 'audio/', 'text/')):
        filename = f'{filename}.{mime_type.split("/")[1]}'
        new_filepath = os.path.join(output_dir, filename)
        os.rename(filepath, new_filepath)
        result['path'] = new_filepath
        result['filename'] = filename
    

    if mime_type == 'application/octet-stream':
        if 'sound' in expected_types:
            mime_type = 'audio/wav'
            result['media_type'] = 'sound'
            result['status'] = 0
            return result
        else:
            return result
    elif not expected_types:
        result['status'] = 0
        return result
    elif mime_type.startswith('image/') and 'image' in expected_types:
        media_type = 'image'
    elif mime_type.startswith('video/') and 'video' in expected_types:
        media_type = 'video'
    elif mime_type.startswith('audio/') and 'sound' in expected_types:
        media_type = 'sound'
    elif mime_type.startswith('text/') and 'text' in expected_types:
        media_type = 'text'
    else:
        return result
    
    result['type'] = media_type
    result['status'] = 0
    return result


def download_file_from_youtube_url(url, ydl_opts={}, output_dir='', filename=None):
    '''Download video from YouTube
    
    Will only return True if the extension is mp4.
    '''
    if filename is None:
        filename = f'{uuid4()}.mp4'
    
    filepath = os.path.join(output_dir, filename)
    extension = None

    result = {
        'status': 1,
        'path': filepath
    }

    opts = {
        'noplaylist': True,
        'format': 'bestvideo[height<=1080,ext=mp4]+bestaudio/best',
        'quiet': True,
        # 'merge_output_format': 'mp4',
        'outtmpl': filepath
    }
    opts.update(ydl_opts)

    if 'mp4' in opts['format']:
        extension = 'mp4'

    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])

    except Exception:
        Path(filepath).unlink(missing_ok=True)
        return result
    
    
    result['filename'] = filename
    result['mime_type'] = 'video/mp4'
    result['status'] = 0
    return result



def download_sound_file_from_youtube_url(url, ydl_opts={}, output_dir='', filename=None):
    '''Download sound from YouTube
    
    Will only return True if the extension is m4a.
    '''
    if filename is None:
        filename = f'{uuid4()}.m4a'
    filepath = os.path.join(output_dir, filename)
    extension = None

    result = {
        'status': 1,
        'path': filepath
    }

    opts = {
        'noplaylist': True,
        'format': 'bestaudio/best[ext=m4a]',
        'quiet': True,
        'outtmpl': filepath
    }
    opts.update(ydl_opts)

    if 'mp4' in opts['format']:
        extension = 'm4a'

    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])

    except Exception:
        return result
    
    
    result['filename'] = filename
    result['extension'] = extension
    result['status'] = 0
    return result



def parse_int_or_400(data, key, default=None):
    """Parse the data[key] to integer."""
    
    if key not in data:
        return default

    try:
        value = int(data.get(key))
    except ValueError:
        raise ParseError(detail=f"Unable to parse param '{key}'.")
    else:
        return value


def parse_bool_or_400(data, key, default=None):
    """
    Parse the data[key] to boolean
    """
    if key not in data:
        return default
    
    return data[key].lower() in ('true', '1')


def parse_datetime_or_400(data, key, default=None, format='%Y-%m-%d'):
    """Parse the data[key] to datetime"""

    if key not in data:
        return default
    
    try:
        d = datetime.strptime(data[key], format)
    except ValueError:
        raise ParseError(detail=f"Unable to parse param '{key}'.")
    else:
        return d


def parse_string_array_or_400(data, key, default=None, delimiter=','):
    """Parse the data[key] to an array of string"""

    if key not in data:
        return default

    d = data[key].split(delimiter)
    return d


def parse_int_array_or_400(data, key, default=None, delimiter=','):
    """Parse the data[key] to an array of int"""

    if key not in data:
        return default
    
    if isinstance(data[key], list):
        return data[key]
    
    try:
        return [int(_) for _ in data[key].split(delimiter)]
    except ValueError:
        raise ParseError(detail=f"Unable to parse param '{key}'.")
