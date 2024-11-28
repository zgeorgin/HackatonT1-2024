from tkinter import *
from tkinter.ttk import Combobox, Button, Label, Treeview, Scrollbar, Progressbar
from tkinter import Label, Button
from tkinter import Toplevel, scrolledtext
from PIL import Image, ImageTk
import io


class GUI:
    def __init__(self, window, saver_loader, groups):
        self.window = window
        self.saver_loader = saver_loader
        self.question_window = None
        self.table_window = None
        self.info_window = None
        self.current_page = 0
        self.rows_per_page = 50  # Количество строк на странице
        self.setup_ui()
        self.groups = groups

    def setup_ui(self):
        self.window.config(background='lightgrey')
        self.window.title("Создание золотой записи из данных пользователя")
        self.window.geometry("1200x700")

        frame = Frame(self.window, relief=GROOVE, borderwidth=10, padx=10, pady=10, bg="darkgrey")
        frame.place(x=100, y=100, width=460, height=360)

        self.combobox = Combobox(frame, values=["Вручную проверить группы связей", "Доверить проверке нейросети"], width=35, state="readonly")
        self.combobox.grid(row=2, column=1)
        self.combobox.set("Вручную проверить группы связей")

        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        self.create_widgets(frame)

    def create_widgets(self, frame):
        method_lbl = Label(frame, text="Укажите путь до необработанного датасета (в CSV формате)", bg="darkgrey")
        method_lbl.place(x=10, y=30)

        cur_table = Label(frame, text="Текущая таблица: ", bg="darkgrey")
        cur_table.place(x=10, y=100)

        method_lbl = Label(frame, text="Укажите путь сохранения золотого датасета", bg="darkgrey")
        method_lbl.place(x=10, y=260)

        submit_btn = Button(frame, text="Запустить алгоритм", command=self.run_algorithm)
        submit_btn.place(x=10, y=175)

        save_button = Button(frame, text="Сохранить файл", command=self.saver_loader.save_file)
        save_button.place(x=10, y=290, width=400)

        show_table_btn = Button(frame, text="Просмотр текущей таблицы", command=self.show_table)
        show_table_btn.place(x=160, y=175, width=230)

        show_info_btn = Button(frame, text="Просмотр информации о текущей таблице", command=self.show_info)
        show_info_btn.place(x=10, y=220, width=300)

        progress_bar = Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progress_bar.place(x=10, y=130)

        open_button = Button(frame, text="Открыть файл", command=lambda: self.saver_loader.open_file(progress_bar, cur_table))
        open_button.place(x=10, y=60, width=400)

        img = Image.open('question.png')
        button_image = ImageTk.PhotoImage(img.resize((50, 50)))
        question_button = Button(self.window, image=button_image, command=self.open_question_window)
        question_button.place(x=1100, y=600, width=60, height=60)
        question_button.image = button_image

    def selected(self, event):
        selection = self.combobox.get()
        if selection == "Вручную проверить группы связей":
            self.saver_loader.man_flag = 1
        elif selection == "Доверить проверке нейросети":
            self.saver_loader.man_flag = 0

    def run_algorithm(self):
        if self.saver_loader.man_flag == 1:
            uniqueCol = "client_fio_full"
            matchCol = "client_bplace"

            self.saver_loader.GF.getClusters(uniqueCol, matchCol)
            self.saver_loader.GF.getMatchings("LCS")
            print("MATCHED!")
            self.saver_loader.GF.getTransformations()
            self.saver_loader.GF.getGroups("Structs")
            print(len(self.saver_loader.GF.groups))
            
            #self.saver_loader.GF.groups = dict(list(self.saver_loader.GF.groups.items())[:15])
            formated_groups = []
            for key in self.saver_loader.GF.groups:
                formated_groups.append([key])
                for t in self.saver_loader.GF.groups[key][:20]:
                    formated_groups[-1].append(f"{t.m.a} -> {t.m.b}")
            
            self.groups = formated_groups
            results = []
            # Индекс текущей группы
            current_index = 0

            # Создание нового окна
            algo_window = Toplevel(self.window)
            algo_window.title("Проверка групп")
            algo_window.geometry("400x500")

            # Основной фрейм с прокруткой
            main_frame = Frame(algo_window)
            main_frame.pack(fill=BOTH, expand=True)

            # Создание Canvas для скроллинга
            canvas = Canvas(main_frame)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # Вертикальный скроллер
            scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Фрейм внутри Canvas для содержимого группы
            group_frame = Frame(canvas)
            canvas.create_window((0, 0), window=group_frame, anchor="nw")

            # Функция для обновления размеров Canvas
            def update_canvas_size(event=None):
                canvas.configure(scrollregion=canvas.bbox("all"))

            group_frame.bind("<Configure>", update_canvas_size)

            # Панель с кнопками
            button_frame = Frame(algo_window)
            button_frame.pack(fill=X, padx=10, pady=10)

            yes_button = Button(button_frame, text="Да", command=lambda: handle_response(1), bg="lightgreen")
            yes_button.pack(side=LEFT, expand=True, fill=X, padx=5)

            no_button = Button(button_frame, text="Нет", command=lambda: handle_response(0), bg="lightcoral")
            no_button.pack(side=LEFT, expand=True, fill=X, padx=5)

            finish_button = Button(button_frame, text="Завершить", command=algo_window.destroy, bg="lightblue")
            finish_button.pack(side=LEFT, expand=True, fill=X, padx=5)

            # Счётчик групп
            counter_label = Label(algo_window, text="", font=("Arial", 12))
            counter_label.pack(pady=5)

            # Функция для обновления отображаемой группы
            def update_group():
                # Очистить содержимое group_frame
                for widget in group_frame.winfo_children():
                    widget.destroy()
                if current_index < len(self.groups):
                    for line in self.groups[current_index]:
                        Label(group_frame, text=line, anchor="w", wraplength=350, justify=LEFT).pack(fill=X, padx=5, pady=2)
                    # Обновить счётчик групп
                    counter_label.config(text=f"Группа {current_index + 1} из {len(self.groups)}")

            # Функция для обработки нажатия кнопок "Да" или "Нет"
            def handle_response(response):
                nonlocal current_index
                results.append(response)
    
                if response:
                    self.saver_loader.GF.applyGroup(current_index)
                current_index += 1
                if current_index < len(self.groups):
                    update_group()
                else:
                    algo_window.destroy()

            # Отобразить первую группу
            update_group()

            # Убедиться, что всё обновлено
            algo_window.protocol("WM_DELETE_WINDOW", algo_window.destroy)
            algo_window.wait_window()

            return results

    def show_table(self):
        if self.table_window is None or not self.table_window.winfo_exists():
            self.table_window = Toplevel(self.window)
            self.table_window.title("Таблица")

            if self.saver_loader.df is not None:
                frame = Frame(self.table_window)
                frame.pack(fill=BOTH, expand=True)

                tree = Treeview(frame, show='headings')
                tree.pack(side=LEFT, fill=BOTH, expand=True)

                y_scroll = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
                y_scroll.pack(side=RIGHT, fill=Y)

                x_scroll = Scrollbar(self.table_window, orient=HORIZONTAL, command=tree.xview)
                x_scroll.pack(side=BOTTOM, fill=X)

                tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

                columns = list(self.saver_loader.df.columns)
                tree['columns'] = columns

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor=CENTER, width=150)

                def load_page(page):
                    tree.delete(*tree.get_children())
                    start_idx = page * self.rows_per_page
                    end_idx = start_idx + self.rows_per_page
                    for _, row in self.saver_loader.df.iloc[start_idx:end_idx].iterrows():
                        tree.insert('', END, values=list(row))

                load_page(self.current_page)

                def next_page():
                    if (self.current_page + 1) * self.rows_per_page < len(self.saver_loader.df):
                        self.current_page += 1
                        load_page(self.current_page)

                def prev_page():
                    if self.current_page > 0:
                        self.current_page -= 1
                        load_page(self.current_page)

                btn_frame = Frame(self.table_window)
                btn_frame.pack(fill=X)

                prev_btn = Button(btn_frame, text="Назад", command=prev_page)
                prev_btn.pack(side=LEFT, padx=10, pady=10)

                next_btn = Button(btn_frame, text="Вперед", command=next_page)
                next_btn.pack(side=RIGHT, padx=10, pady=10)
            else:
                Label(self.table_window, text="Нет данных для отображения.", font=("Arial", 14)).pack(pady=20)

            def close_table_window():
                self.table_window.destroy()
                self.table_window = None

            self.table_window.protocol("WM_DELETE_WINDOW", close_table_window)

    def show_info(self):
        if self.info_window is None or not self.info_window.winfo_exists():
            self.info_window = Toplevel(self.window)
            self.info_window.title("Информация о таблице")

            if self.saver_loader.df is not None:
                buffer_info = io.StringIO()
                self.saver_loader.df.info(buf=buffer_info)
                info_text = buffer_info.getvalue()

                describe_df = self.saver_loader.df.describe()
                describe_text = describe_df.to_string(max_cols=47, line_width=200)

                text_widget = scrolledtext.ScrolledText(self.info_window, wrap=NONE, font=("Courier New", 10), padx=10, pady=10)
                text_widget.pack(fill=BOTH, expand=True)

                text_widget.insert(END, "Информация о таблице:\n")
                text_widget.insert(END, info_text)
                text_widget.insert(END, "\n\nСтатистика (describe):\n")
                text_widget.insert(END, describe_text)
                text_widget.config(state=DISABLED)

                x_scroll = Scrollbar(self.info_window, orient=HORIZONTAL, command=text_widget.xview)
                x_scroll.pack(side=BOTTOM, fill=X)
                text_widget.configure(xscrollcommand=x_scroll.set)
            else:
                Label(self.info_window, text="Нет данных для отображения.", font=("Arial", 14)).pack(pady=20)

            def close_info_window():
                self.info_window.destroy()
                self.info_window = None

            self.info_window.protocol("WM_DELETE_WINDOW", close_info_window)

    def open_question_window(self):
        # global question_window

        if self.question_window is None or not self.question_window.winfo_exists():
            self.question_window = Toplevel(self.window)
            self.question_window.title("Вопросы")

            text_widget = Text(self.question_window, height=10, width=50)
            text_widget.pack(padx=20, pady=20)

            message = "1) Выберите датасет\n" \
                      "2) Выберите метод подтверждения преобразований\n" \
                      "3) Посмотрите информацию о датасете до запуска алгоритма\n"\
                      "4) Нажмите 'Запустить алгоритм' \n" \
                      "5) Посмотрите информацию о датасете после запуска алгоритма"
            text_widget.insert(END, message)

            def close_question_window():
                global question_window
                self.question_window.destroy()
                question_window = None

            self.question_window.protocol("WM_DELETE_WINDOW", close_question_window)
