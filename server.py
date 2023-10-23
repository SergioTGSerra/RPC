import base64
from PIL import Image
from io import BytesIO
from xmlrpc.server import SimpleXMLRPCServer

def convert_to_grayscale(encoded_image):
    # Decodificando a imagem recebida
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    
    # Converte para escala de cinza
    grayscale_image = image.convert("L")
    
    # Codifica a imagem em escala de cinza de volta para o formato desejado (por exemplo, JPEG)
    buffered = BytesIO()
    grayscale_image.save(buffered, format="JPEG")
    encoded_grayscale_image = base64.b64encode(buffered.getvalue())
        
    return encoded_grayscale_image

def resize_image(encoded_image, width, height):
    # Decodifica a imagem
    decoded_image = Image.open(BytesIO(encoded_image))
    
    # Redimensiona a imagem mantendo as proporções
    resized_image = decoded_image.resize((width, height))
    
    # Codifica a nova imagem de volta para o formato desejado (por exemplo, JPEG)
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format="JPEG")
    encoded_resized_image = output_buffer.getvalue()
    
    return encoded_resized_image

def rotate_image(encoded_image, angle):
    # Decodifica a imagem
    decoded_image = Image.open(BytesIO(encoded_image))
    
    # Rotaciona a imagem pelo ângulo especificado
    rotated_image = decoded_image.rotate(angle, expand=True)
    
    # Codifica a nova imagem de volta para o formato desejado (por exemplo, JPEG)
    output_buffer = BytesIO()
    rotated_image.save(output_buffer, format="JPEG")
    encoded_rotated_image = output_buffer.getvalue()
    
    return encoded_rotated_image


# Inicialização do servidor RPC
server = SimpleXMLRPCServer(('server', 8000))
server.register_function(convert_to_grayscale, 'convert_to_grayscale')
server.register_function(resize_image, 'resize_image')
server.register_function(rotate_image, 'rotate_image')

# Inicia o servidor
print("Servidor RPC iniciado na porta 8000...")
server.serve_forever()