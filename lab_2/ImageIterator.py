import csv

class ImgIterator:
    def __init__(self,note_path):
        """
        записывает в поле data строки аннотации
        и в поле limit их количество
        :param note_path:
        путь к аннотации
        """
        with open(note_path, 'r') as file:
            reader = csv.reader(file)
            self.data = [row for row in reader]
            self.limit = len(self.data)
            self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        """
        перебирает элементы в data
        :return:
        элементы из data в виде строки с разделителем пробелом
        """
        if self.counter < self.limit:
            cur_row = "   ".join(self.data[self.counter])
            self.counter +=1
            return cur_row
        else:
            raise StopIteration