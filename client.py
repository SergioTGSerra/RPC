import xmlrpc.client
import base64
from PIL import Image
import io

# Conecta ao servidor RPC
server = xmlrpc.client.ServerProxy('http://server:8000')

def convert_to_grayscale(encoded_image):
    return send_task(encoded_image, server.convert_to_grayscale)

def resize_image(encoded_image, width, height):
    return send_task(encoded_image, server.resize_image, width, height)

def rotate_image(encoded_image, angle):
    return send_task(encoded_image, server.rotate_image, angle)

def send_task(encoded_image, operation_func, *args):
    return operation_func(encoded_image, *args)

def save_image(image, save_path):
    image.save(save_path, 'JPEG')

def get_image(task_id):
   binary_result_image = server.get_image(task_id).data
   decoded_result_bytes = base64.b64decode(binary_result_image)
   result_image = Image.open(io.BytesIO(decoded_result_bytes))
   return result_image

def get_task_status(task_id):
    return server.get_task_status(task_id)

with open("./image.jpg", 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode()

task_gray = convert_to_grayscale(encoded_image)
task_resize = resize_image(encoded_image, 800, 600)
task_rotate = rotate_image(encoded_image, 90)


while True:
    if(
        get_task_status(task_gray)['status'] == 'completed' and
        get_task_status(task_resize)['status'] == 'completed' and
        get_task_status(task_rotate)['status'] == 'completed'
       ):
            save_image(get_image(task_gray), '/data/grayscale_image.jpg')
            save_image(get_image(task_resize), '/data/resized_image.jpg')
            save_image(get_image(task_rotate), '/data/rotated_image.jpg')
            break