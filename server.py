import base64
from PIL import Image
from io import BytesIO
from xmlrpc.server import SimpleXMLRPCServer
import threading

TASKS = {}

def create_image_processing_task(encoded_image, operation, *args):
    task_id = len(TASKS) + 1
    TASKS[task_id] = {'status': 'processing'}
    threading.Thread(target=process_image, args=(task_id, encoded_image, operation, *args)).start()
    return task_id

def process_image(task_id, encoded_image, operation_func, *args):
    decoded_image = base64.b64decode(encoded_image)
    with Image.open(BytesIO(decoded_image)) as image:
        result_image = operation_func(image, *args)

    with BytesIO() as buffered:
        result_image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue())

    TASKS[task_id]['status'] = 'completed'
    TASKS[task_id]['result'] = encoded_image

def convert_to_grayscale(image):
    return image.convert("L")

def resize_image(image, width, height):
    return image.resize((width, height))

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

def get_task_status(task_id):
    task_info = TASKS.get(task_id)
    if task_info is not None:
        return {'status': task_info.get('status')}
    else:
        return {'status': 'error', 'message': 'Tarefa não encontrada'}
    
def get_image(task_id):
    if TASKS.get(task_id).get('status') == 'completed': return TASKS.get(task_id).get('result')

server = SimpleXMLRPCServer(('0.0.0.0', 8000))

server.register_function(lambda img: create_image_processing_task(img, convert_to_grayscale), 'convert_to_grayscale')
server.register_function(lambda img, w, h: create_image_processing_task(img, resize_image, w, h), 'resize_image')
server.register_function(lambda img, a: create_image_processing_task(img, rotate_image, a), 'rotate_image')
server.register_function(lambda task_id: get_task_status(task_id), 'get_task_status')
server.register_function(lambda task_id: get_image(task_id), 'get_image')

print("Servidor RPC iniciado na porta 8000...")
server.serve_forever()