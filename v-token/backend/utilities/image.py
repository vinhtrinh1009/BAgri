'''
Utility functions for working with images.
Contributors: 
    - minhdq99hp@gmail.com
'''
from inspect import trace
from io import BytesIO
import traceback
from os.path import splitext

# import cv2 as cv
# import numpy as np
# import requests
# from PIL import Image



# class UnsupportedExtension(Exception):
#     pass

# def convert_image(input_path, output_path, o_ext=None):
#     '''
#     Use PIL.Image to convert image format.
#     The output extension will be determined from output_path. 
#     You can also specify it by using o_ext.

#     Supported extensions: png, jpeg, webp
#     Warning: 
#     - Every image will be convert to RGB, 
#       which mean the output image will not have alpha value.
#     '''
#     supported_exts = ('png', 'jpeg', 'webp', 'bmp')
#     if not o_ext:
#         _, ext = splitext(output_path)
#         o_ext = ext[1:].lower().replace('jpg', 'jpeg')

#     if o_ext not in supported_exts:
#         raise UnsupportedExtension(f"Can't convert image to {o_ext}")

#     im = Image.open(input_path).convert("RGB")
#     im.save(output_path, o_ext)


# def validate_image(input_path, output_path, valid_modes=('RGB')):
#     '''
#     Validate and convert image to the suitable format for AE and ME
#     '''
#     im = Image.open(input_path)
#     im.verify()
    
#     if im.mode not in valid_modes:
#         im = im.convert('RGB')
        
#     image_type = im.get_format_mimetype()

#     if image_type not in ('image/jpeg', 'image/png'):
#        im.save(output_path, 'png')
#     else:
#         im.save(output_path)
    



# def save_frame_from_video(video_path, millisecond=0, frame_file_path):
#     '''Read a single frame from video_path at 
#     position _millisecond_ and write it to frame_file_path
#     '''
#     vidcap = cv.VideoCapture(video_path)

#     vidcap.set(cv.CAP_PROP_POS_MSEC, millisecond)

#     ret, image = vidcap.read()

#     if ret and not image.empty():     
#         # save image to temp file
#         cv.imwrite(frame_file_path, image)
#     else:
#         cv.imwrite(frame_file_path, np.zeros((120, 160, 3), np.uint8))
#     vidcap.release()


# def get_frame_from_video(video_path, millisecond=0, mode='s3'):
#     '''Read a single frame from video_path (file is stored at s3 bucket) at 
#     position _millisecond_ and write it to frame_file_path
#     '''
#     vidcap = cv.VideoCapture(video_path)

#     vidcap.set(cv.CAP_PROP_POS_MSEC, millisecond)

#     ret, image = vidcap.read()

#     if ret and not image.empty():  
#         is_success, buffer = cv.imencode(".jpg", image)
#         io_buf = BytesIO(buffer)
#     else:
#         is_success, buffer = cv.imencode(".jpg", np.zeros((120, 160, 3), np.uint8))
#         io_buf = BytesIO(buffer)
#     vidcap.release()

#     return io_buf

# def get_black_thumbnail(width=160, height=120):
#     '''
#     Return:
#         - JPEG encoded image buffer
#     '''
#     is_success, buffer = cv.imencode(".jpg", np.zeros((height, width, 3), np.uint8))
#     return buffer

# def get_video_thumbnail_from_url(url, width=160, height=120):
#     '''
#     In the optimal case, it will choose the frame at 1 sec position as the thumbnail. 
#     If the video is shorter, it will take the first frame as thumbnail.
#     In the worst case, it will return a black frame.

#     Return:
#         - JPEG encoded image buffer
#     '''
#     res = None

#     try:
#         cap = cv.VideoCapture(url)
#         if cap.isOpened():
#             i = 0
#             first_frame = None
#             best_frame = None
#             length = int(cv.VideoCapture.get(cap, int(cv.CAP_PROP_FRAME_COUNT)))
#             fps = int(cv.VideoCapture.get(cap, int(cv.CAP_PROP_FPS)))

#             if length < 1 or fps < 1:
#                 res = get_black_thumbnail(width, height)
#             else:
#                 while True:
#                     # Capture frame-by-frame
#                     ret, frame = cap.read()
#                     if frame is not None:
#                         if i == 0:
#                             first_frame = frame
#                             if fps > length:
#                                 break
#                         elif i == fps - 1: # get the frame at 1 sec position
#                             best_frame = frame
#                             break
#                     else:
#                         break
#                     i += 1

#                 if best_frame is not None:
#                     _, res = cv.imencode('.jpg', best_frame)
#                 elif first_frame is not None:
#                     _, res = cv.imencode('.jpg', first_frame)                
#     except Exception:
#         traceback.print_exc()
#     finally:
#         cap.release()

#     if res is None:
#         return get_black_thumbnail(width, height)
#     return res