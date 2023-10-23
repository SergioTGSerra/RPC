import xmlrpc.client
import base64
from PIL import Image
import io

# Conecta ao servidor RPC
server = xmlrpc.client.ServerProxy('http://server:8000')

with open("./image.jpg", 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()

binary_grayscale_image = server.convert_to_grayscale(encoded_image).data

decoded_grayscale_bytes = base64.b64decode(binary_grayscale_image)

image = Image.open(io.BytesIO(decoded_grayscale_bytes))

image.save('/data/grayscale_image.jpg', 'JPEG')
