import base64
import numpy as np
import halcon as h
import cv2

def base64_to_hobject(base64_image, width, height):
    # Декодируем base64 в байты
    image_bytes = base64.b64decode(base64_image)  
    # Halcon коэффициент отступа (костыль)  
    offset = 30
    # Создаем numpy массив из байтов
    np_array = np.frombuffer(image_bytes, dtype=np.uint8, offset=offset)  
    # Преобразуем в 3D массив (высота, ширина, каналы)
    image_array = bytes(np_array)
    #image_array = bytes(np_array.reshape(height, width))
    # для цветного
    #image_array = bytes(np_array.reshape(height, width,3))
    # создаём новое изображение Halcon Image, передаём указатель на массив точек
    himage = h.gen_image1("byte", width, height, id(image_array))
    return himage
\
def convert_image_to_grayscale(image_path):
    # Читаем изображение
    image = cv2.imread(image_path)
    # Преобразуем изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Определяем ширину и высоту изображения
    height, width = gray_image.shape[:2]
    return gray_image, width, height


def grayscale_image_to_base64(gray_image):
    # Преобразуем изображение в формат JPEG, если требуется сжатие
    #_, img_encoded = cv2.imencode('.jpg', gray_image)
    # Кодируем изображение в base64
    base64_encoded = base64.b64encode(gray_image)
    return base64_encoded

# Пример использования
# Путь к изображению
image_path = "test.png"
image_path = '/home/andrew/Pictures/remmina_COPY My Work SES PC 2_192.168.0.66_20231116-093856.png'
#image_path = "path/to/your/image.jpg"
# Конвертируем изображение в оттенки серого
gray_image, width, height = convert_image_to_grayscale(image_path)
# Конвертируем изображение в base64
base64_string = grayscale_image_to_base64(gray_image)
# Преобразуем в HObject (halcon image format)
halcon_image = base64_to_hobject(base64_string, width, height)
# Записываем результат
h.write_image(halcon_image, "tiff", 0, "HO_from_base64")