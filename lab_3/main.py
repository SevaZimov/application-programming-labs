import cv2
import argparse
import matplotlib.pyplot as plt
import numpy as np


def pars_img_path()->tuple:
    """
    Извлекает из командной строки
    абсолютный путь к изображению
    и путь для сохранения результата
    работы программы
    :return:
    Абсолютный путь к изображению,
    абсолютный путь в папку для сохранения
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('imgpath',type=str)
        parser.add_argument('savepath', type=str)
        args=parser.parse_args()
        return args.imgpath, args.savepath
    except:
        raise SyntaxError("Аргументы командной строки не должны быть пустыми")



def split_in_three(img:np.ndarray)->tuple:
    """
    Разделяет изображение на потоли красного,
    синего и зеленого
    :param img:
    Переменная, в которой хранится изображение
    :return:
    Три
    """
    b,g,r=cv2.split(img)
    return b,g,r






def create_color_histogram(streams:tuple,colors:list)->None:
    """
    Строим гистограмму интенсивности и частоты трёх основных цветов
    :param streams:
    Три потока, на которые было разбито изображение
    :param colors:
    Массив основных цветов
    """
    x = np.arange(256)
    bar_width = 0.5
    plt.figure(figsize=(16, 8))
    for i, (streams, color) in enumerate(zip(streams, colors)):
        hist = cv2.calcHist([streams], [0], None, [256], [0, 256]).flatten()
        plt.bar(x + i * bar_width, hist, width=bar_width, label=color, alpha=0.2)

    plt.title('Сравнительная гистограмма цветов')
    plt.xlabel('Интенсивность')
    plt.ylabel('Частота')
    plt.legend()
    plt.show()

def show_and_write(img:np.ndarray,path:str)->None:
    """
    Сохраняет и выводит пользователю изображение
    :param img:
    Обрабатываемое изображение
    :param path:
    Путь для сохранения изображения
    """
    if not(cv2.imwrite(path,img)):
        raise SystemError("Невозможно сохранить изображение в указанную директорию")
    cv2.imshow(path,img)



if __name__=="__main__":
    try:
        paths = pars_img_path()
        img=cv2.imread(paths[0])
        shape = img.shape
        print("Размер изображения: ",img.shape)
        cv2.imshow(paths[0],img)
        cv2.waitKey(0)
        colors = ["blue", "green", "red"]
        color_streams = split_in_three(img)
        create_color_histogram(color_streams,colors)
        for i ,j in enumerate(color_streams):
            show_and_write(j,paths[1]+"\\" + colors[i]+".jpg")
            cv2.waitKey(0)
    except Exception as exc:
        print(exc)