import pandas as pd
import cv2
import argparse
import matplotlib.pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame


def pars_args()->str:
    """
    Извлекает из командной строки
    ключевое слово для поиска изображений
    путь в папку для сохранения изображений
    путь к аннотации
    :return:
    кортеж из аргументов командной строки
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('note_path',type=str)
        args=parser.parse_args()
        return args.note_path
    except:
        raise SyntaxError("Arguments can not be blank")

def get_height_width_depth(path:str)->tuple:
    """
    Получает путь к изображению и вычисляет
    его шириyу, высоту и глубину
    :param path:
    Путь к изображению
    :return:
    Ширина, высота, глубина(количество каналов)
    """
    try:
        img = cv2.imread(path,0)
        height, width = img.shape[:2]
        depth = len(img.shape)
        return height, width, depth
    except:
        raise OSError("Incorrect image path")

def filtered_data(max_height:int,max_width:int,data:DataFrame)->DataFrame:
    """
    Находит в дата фрейме все изображения, подходящие
    по критериям ширины и высоты
    :param max_height:
    Максимальная высота
    :param max_width:
    Максимальная ширина
    :param data:
    Датафрейм, в котором идёт поиск
    :return:
    Новый датафрейм, удовлетворяющий условию
    """
    result_df = data[data['Height'] <= max_height]
    result_df = result_df[result_df['Width'] <= max_width]
    return result_df


def create_square_hist(df:DataFrame)->None:
    """
    Строит гистограмму по площадям изображений в датафрейме
    :param df:
    Датафрейм с данными
    """
    count = df['Square'].value_counts()
    plt.figure(figsize=(16, 8))
    plt.hist(df['Square'],bins = len(count),color='skyblue', edgecolor='black')
    plt.xlabel("Площадь")
    plt.ylabel("Количество")
    plt.show()



if __name__ == "__main__":
    try:
        note_path = pars_args()
        df = pd.read_csv(note_path)
        new_cols = ['Height','Width','Depth', 'Square']
        df[new_cols[0]] = 0
        df[new_cols[1]] = 0
        df[new_cols[2]] = 0
        paths = df['Absolute path']
        for i in range(50):
            height, width, depth = get_height_width_depth(paths[i])
            df.loc[i:i+1,new_cols[0]] = height
            df.loc[i:i+1, new_cols[1]] = width
            df.loc[i:i+1, new_cols[2]] = depth
            df.loc[i:i + 1, new_cols[3]] = height*width
        print(df.describe())
        df = df.sort_values(new_cols[3],ascending=False)
        print("\n")
        print(df[new_cols[3]])
        print(len(filtered_data(500,500,df)))
        create_square_hist(df)
    except Exception as exc:
        print(exc)
