import base64
from PIL import Image
from io import BytesIO
from xmlrpc.server import SimpleXMLRPCServer

def apply_image_operation(encoded_image, operation_func, *args):
    decoded_image = base64.b64decode(encoded_image)
    with Image.open(BytesIO(decoded_image)) as image:
        result_image = operation_func(image, *args)

    with BytesIO() as buffered:
        result_image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue())

def convert_to_grayscale(image):
    return image.convert("L")

def resize_image(image, width, height):
    return image.resize((width, height))

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

server = SimpleXMLRPCServer(('server', 8000))

server.register_function(lambda img: apply_image_operation(img, convert_to_grayscale), 'convert_to_grayscale')
server.register_function(lambda img, w, h: apply_image_operation(img, resize_image, w, h), 'resize_image')
server.register_function(lambda img, a: apply_image_operation(img, rotate_image, a), 'rotate_image')

print("Servidor RPC iniciado na porta 8000...")
server.serve_forever()