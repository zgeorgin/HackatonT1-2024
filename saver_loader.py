import pandas as pd
from tkinter import filedialog
import threading
import chardet

class SaverLoader:
    def __init__(self, window, df=None, open_path=None, save_path=None, man_flag=None):
        self.window = window
        self.df = df
        self.open_path = open_path
        self.save_path = save_path
        self.man_flag = 1

    def open_file(self, progress_bar, cur_table):
        self.open_path = filedialog.askopenfilename()
        if not self.open_path:
            return  # Если файл не выбран, выходим

        progress_bar['value'] = 0
        self.window.update_idletasks()

        try:
            def load_data():
                try:
                    # Определяем кодировку файла
                    detected_encoding = detect_encoding(self.open_path)

                    # Сначала узнаем количество строк в файле
                    with open(self.open_path, 'r', encoding=detected_encoding, errors='replace') as f:
                        total_lines = sum(1 for _ in f) - 1  # Учитываем строку заголовков
                    chunk_size = 1000
                    total_chunks = (total_lines // chunk_size) + 1

                    chunks = pd.read_csv(self.open_path, chunksize=chunk_size, encoding=detected_encoding)
                    data = []
                    for i, chunk in enumerate(chunks):
                        data.append(chunk)
                        progress_bar['value'] = ((i + 1) / total_chunks) * 100
                        self.window.update_idletasks()

                    self.df = pd.concat(data, ignore_index=True)

                    cur_table.config(text=f"Текущая таблица: {self.open_path.split('/')[-1]}")
                except Exception as e:
                    cur_table.config(text="Ошибка загрузки файла")
                    print(f"Ошибка: {e}")
                finally:
                    progress_bar.grid_remove()

            threading.Thread(target=load_data).start()

        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            cur_table.config(text="Ошибка загрузки файла")
            progress_bar.grid_remove()

    def save_file(self):
        self.save_path = filedialog.asksaveasfilename()
        self.save_path += '.csv'
        with open(self.save_path, 'w+') as f:
            self.df.to_csv(self.save_path)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Читаем часть файла
        result = chardet.detect(raw_data)
        return result['encoding']
