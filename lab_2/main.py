import argparse
import csv
import os
from argparse import ArgumentParser
from ImageIterator import ImgIterator
from icrawler.builtin import GoogleImageCrawler



def pars_args()->tuple:
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
        parser.add_argument('keyword',type=str)
        parser.add_argument('save_dir_path',type=str)
        parser.add_argument('note_path',type=str)
        args=parser.parse_args()
        return args.keyword,args.save_dir_path,args.note_path
    except:
        raise SyntaxError("Arguments can not be blank")

def img_downloader(_keyword,dir_path)->None:
    """
    Скачивает используя гугл 50 изображений по ключевому слову
    :param _keyword:
    ключевое слово для скачивания изображений
    :param dir_path:
    путь к директории для хранения изображений
    :return:
    None
    """
    try:
        google_crawler = GoogleImageCrawler(storage={'root_dir' : dir_path})
        google_crawler.crawl(keyword=_keyword,max_num=50)
    except:
        raise NotADirectoryError("Wrong directory to save images")

def get_dir_files(dir_path)->list:
    """
    Находит названия всех файлов в папке
    :param dir_path:
    путь к папке с файлами
    :return:
    список имён всех файлов
    """
    try:
        for i in os.walk(dir_path):
            files = i[2]
            paths_to_img=[]
            for file in files:
                paths_to_img.append(os.path.join(dir_path,file))
            return paths_to_img
    except:
        raise NotADirectoryError("Wrong path to images")

def create_note(note_path,files)->None:
    """
    Записывает и создаёт если требуется файл аннотацию
    содержащую абсолютный и относительный путь к каждому изображению
    :param note_path:
    путь к файлу аннотации
    :param files:
    список файлов изображений
    :return:
    None
    """
    try:
        cur_file = os.path.dirname(note_path)
        with open(note_path,mode='w',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Absolute path","Relative path"])
            for i in files:
                abs_path = os.path.abspath(i)
                relative_path = os.path.relpath(i,cur_file)
                writer.writerow([abs_path, relative_path])
    except:
        raise FileExistsError("Wrong directory to annotation file")



if __name__ == "__main__":
    try:
        arguments = pars_args()
        keyword = arguments[0]
        save_dir_path = arguments[1]
        note_path = arguments[2]
        "img_downloader(keyword,save_dir_path)"
        downloaded_files = get_dir_files(save_dir_path)
        create_note(note_path,downloaded_files)
        useless_iterator = ImgIterator(note_path)
        for i in useless_iterator:
            print(i)
    except Exception as exc:
        print(exc)
