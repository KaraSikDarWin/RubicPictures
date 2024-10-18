import cv2
import numpy as np
from PIL import Image

# Палитра цветов кубика Рубика без зеленого (в RGB)
rubik_colors = [
    [0, 0, 255],  # blue
    [255, 0, 0],  # red
    [255, 165, 0],  # orange
    [255, 255, 0],  # yellow
    [255, 255, 255]  # white
]

# Функция для квантования уровня серого в цвет кубика
def grayscale_to_rubik_color(value, thresholds, colors):
    # Проверяем, в какой диапазон попадает значение серого и возвращаем соответствующий цвет
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return colors[i]
    return colors[-1]  # Если значение выше последнего порога, возвращаем самый светлый цвет


# основная функция
def image_to_rubik_scheme_bw(file_name ,wcube, hcube):
    # Загружаем изображение и преобразуем его в серый градиет
    width = wcube*3 #вычисление ширины в пикселях
    hieght = hcube*3 #вычисление высоты в пикселях
    image = cv2.imread(file_name)

    # Проверка, если изображение не было загружено
    if image is None:
        raise ValueError("Не удалось загрузить изображение. Проверьте путь.")

    #
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Изменяем размер изображения
    small_image = cv2.resize(gray_image, (width, hieght), interpolation=cv2.INTER_AREA)

    # Определяем пороги для уровней серого, разделенные по количеству цветов
    #thresholds = np.linspace(0, 255, len(rubik_colors) + 1)[1:]  # Пороговые значения для каждого цвета.

    # Равномерно разделяем диапозон от 0 до 255. и выкидываем правую границу с 0, чтобы не делать лишнее сравнение
    thresholds =  [51, 102, 153, 204, 255]
    print(thresholds)

    # Создаем пустой массив для результата. Непосредственно матрицв пикселей
    rubik_scheme = np.zeros((small_image.shape[0], small_image.shape[1], 3), dtype=np.uint8)
    #Переводим каждый пиксель исходного изображения в ограниченную палитру. Передаем в grayscale_to_rubik_color яркость серого пикселя.
    for i in range(small_image.shape[0]):
        for j in range(small_image.shape[1]):
            gray_value = small_image[i, j]
            rubik_scheme[i, j] = grayscale_to_rubik_color(gray_value, thresholds, rubik_colors)

    im_sc = Image.fromarray(rubik_scheme)
    im_sc.show()
    #im_sc.save(file_name.split(".")[0]+"_new.jpg")
    #Раскомментировать если нужно сохранить

    return rubik_scheme

rubik_image_bw = image_to_rubik_scheme_bw("example1.jpg", 18, 25)


