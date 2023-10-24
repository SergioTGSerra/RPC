import xmlrpc.client
import base64
from PIL import Image
import io

# Conecta ao servidor RPC
server = xmlrpc.client.ServerProxy('http://server:8000')

def apply_image_operation_and_save(encoded_image, operation_func, *args, save_path):
    binary_result_image = operation_func(encoded_image, *args).data
    decoded_result_bytes = base64.b64decode(binary_result_image)
    result_image = Image.open(io.BytesIO(decoded_result_bytes))
    result_image.save(save_path, 'JPEG')

def convert_to_grayscale(encoded_image, save_path):
    apply_image_operation_and_save(encoded_image, server.convert_to_grayscale, save_path=save_path)

def resize_image(encoded_image, width, height, save_path):
    apply_image_operation_and_save(encoded_image, server.resize_image, width, height, save_path=save_path)

def rotate_image(encoded_image, angle, save_path):
    apply_image_operation_and_save(encoded_image, server.rotate_image, angle, save_path=save_path)

with open("./image.jpg", 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode()

convert_to_grayscale(encoded_image, '/data/grayscale_image.jpg')
resize_image(encoded_image, 800, 600, '/data/resized_image.jpg')
rotate_image(encoded_image, 90, '/data/rotated_image.jpg')
