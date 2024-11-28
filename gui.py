from tkinter import *
from tkinter.ttk import Combobox, Label, Treeview, Scrollbar, Progressbar, Button
from tkinter import Label
from tkinter import Button as But
from tkinter import Toplevel, scrolledtext
from PIL import Image, ImageTk
import io
from saver_loader import * 

class GUI:
    def __init__(self, window, saver_loader, groups):
        # Инициализация атрибутов
        self.window = window
        self.saver_loader = saver_loader
        self.question_window = None
        self.table_window = None
        self.info_window = None
        self.current_page = 0
        self.rows_per_page = 50  # Количество строк на странице
        self.groups = groups
        self.selected_duplicate_column = None
        self.selected_connection_column = None
        self.selected_data_column = None
        self.setup_ui()

    def setup_ui(self):
        self.window.config(background='lightgrey')
        self.window.title("Создание золотой записи из данных пользователя")
        self.window.geometry("1200x700")

        frame = Frame(self.window, relief=GROOVE, borderwidth=10, bg="darkgrey")
        frame.place(x=180, y=25, width=460, height=420)

        # Инициализируем option_frame с Canvas и Scrollbar
        self.option_frame = Frame(self.window, relief=GROOVE, borderwidth=10, bg="darkgrey")
        self.option_frame.place(x=900, y=25, width=460, height=420)

        # Создание комбобоксов для выбора
        self.combobox = Combobox(frame, values=["Human", "Computer"], width=37, state="readonly")
        self.combobox.place(x=10, y=145)
        self.combobox.set("Метод подтверждения преобразований")
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        self.combobox1 = Combobox(self.option_frame, values=["LCS", "Cell"], width=23, state="readonly")
        self.combobox1.place(x=10, y=195)
        self.combobox1.set("Выберите метод")
        self.combobox1.bind("<<ComboboxSelected>>", self.selected)

        self.combobox2 = Combobox(self.option_frame, values=["Struct", "Program"], width=40, state="readonly")
        self.combobox2.place(x=10, y=255)
        self.combobox2.set("Выберите метод")
        self.combobox2.bind("<<ComboboxSelected>>", self.selected)

        self.duplicate_combobox = Combobox(self.option_frame, values=[], width=40, state="readonly")
        self.duplicate_combobox.place(x=10, y=75)
        self.duplicate_combobox.set("Колонка, в которой искать дубликаты")

        self.connection_combobox = Combobox(self.option_frame, values=[], width=40, state="readonly")
        self.connection_combobox.place(x=10, y=135)
        self.connection_combobox.set("Колонка, в которой искать связи")

        self.data_combobox = Combobox(self.option_frame, values=[], width=40, state="readonly")
        self.data_combobox.place(x=10, y=315)
        self.data_combobox.set("Колонка с датой")

        self.create_widgets(frame)

    def create_widgets(self, frame):
        method_lbl = Label(self.option_frame, text="Дополнительные опции", bg="darkgrey", font=("Courier", 18, "bold"))
        method_lbl.place(x=80, y=5)

        method_lbl = Label(self.option_frame, text="Поиск дубликатов в", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=45)

        method_lbl = Label(self.option_frame, text="Поиск связей в", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=105)

        method_lbl = Label(self.option_frame, text="Метод создания связей:", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=165)

        method_lbl = Label(self.option_frame, text="Метод аггрегации груп преобразований:", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=225)

        method_lbl = Label(self.option_frame, text="Указать колонку с датой:", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=285)

        method_lbl = Label(frame, text="Укажите путь до необработанного датасета (в CSV формате):", bg="darkgrey", font=("Courier", 9, "bold"))
        method_lbl.place(x=10, y=5)

        cur_table = Label(frame, text="Текущая таблица: ", bg="darkgrey", font=("Courier", 10, "bold"))
        cur_table.place(x=10, y=70)

        method_lbl = Label(frame, text="Укажите путь сохранения золотого датасета:", bg="darkgrey", font=("Courier", 12, "bold"))
        method_lbl.place(x=10, y=330)

        submit_btn = Button(frame, text="Запустить алгоритм", command=self.run_algorithm)
        submit_btn.place(x=10, y=190)

        make_btn = Button(frame, text="Сделать золотую запись", command=self.makeGolden)
        make_btn.place(x=160, y=190)

        save_button = Button(frame, text="Сохранить файл", command=self.saver_loader.save_file)
        save_button.place(x=10, y=360, width=420)

        show_table_btn = Button(frame, text="Просмотр текущей таблицы", command=self.show_table)
        show_table_btn.place(x=10, y=240, width=170)

        show_info_btn = Button(frame, text="Просмотр информации о текущей таблице", command=self.show_info)
        show_info_btn.place(x=10, y=290, width=300)

        progress_bar = Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progress_bar.place(x=10, y=100, width=420)

        open_button = Button(frame, text="Открыть файл", command=lambda: self.saver_loader.open_file(progress_bar, cur_table))
        open_button.place(x=10, y=35, width=420)

        img = Image.open('question.png')
        button_image = ImageTk.PhotoImage(img.resize((50, 50)))
        question_button = Button(self.window, image=button_image, command=self.open_question_window)
        question_button.place(x=740, y=715, width=60, height=60)
        question_button.image = button_image

    def update_option_frame(self, columns):
        # Заполнение комбобоксов данными после загрузки таблицы
        self.duplicate_combobox['values'] = columns
        self.duplicate_combobox.set("Выберите колонку")

        # Разрешаем выбор для первого комбобокса только один раз
        self.duplicate_combobox.config(state="readonly")

        # Для второго комбобокса — остаётся доступным для выбора в любой момент
        self.connection_combobox['values'] = columns
        self.connection_combobox.set("Выберите колонку")
        self.connection_combobox.config(state="readonly")
        self.data_combobox['values'] = columns
        self.data_combobox.set("Выберите колонку")
        self.data_combobox.config(state="readonly")

        self.duplicate_combobox.bind("<<ComboboxSelected>>", self.on_column_select)
        self.connection_combobox.bind("<<ComboboxSelected>>", self.on_column_select)
        self.data_combobox.bind("<<ComboboxSelected>>", self.on_column_select)

    def on_column_select(self, event):
        self.selected_duplicate_column = self.duplicate_combobox.get()
        self.duplicate_combobox.config(state="disabled")
        self.selected_connection_column = self.connection_combobox.get()
        self.connection_combobox.config(state="readonly")
        self.selected_data_column = self.data_combobox.get()
        self.data_combobox.config(state="readonly")

    def selected(self, event):
        selection = self.combobox.get()
        selection1 = self.combobox1.get()
        selection2 = self.combobox2.get()
        if selection == "Human":
            self.saver_loader.flags[0] = "Human"
        elif selection == "Computer":
            self.saver_loader.flags[0] = "Computer"
        if selection1 == "LCS":
            self.saver_loader.flags[1] = "LCS"
        elif selection1 == "Cell":
            self.saver_loader.flags[1] = "Cell"
        if selection2 == "Struct":
            self.saver_loader.flags[2] = "Struct"
        elif selection2 == "Program":
            self.saver_loader.flags[2] = "Program"

    def makeGolden(self):
        self.saver_loader.result_df = self.saver_loader.GF.getGolden(self.selected_data_column)
        
    def run_algorithm(self):
        if self.saver_loader.flags[0] == "Human":
            uniqueCol = self.selected_duplicate_column
            matchCol = self.selected_connection_column

            self.saver_loader.GF.getClusters(uniqueCol, matchCol)
            self.saver_loader.GF.getMatchings(self.saver_loader.flags[1])
            print("MATCHED!")
            self.saver_loader.GF.getTransformations()
            self.saver_loader.GF.getGroups(self.saver_loader.flags[2]) 
            
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

            yes_button = But(button_frame, text="Да", command=lambda: handle_response(1), bg="lightgreen")
            yes_button.pack(side=LEFT, expand=True, fill=X, padx=5)

            no_button = But(button_frame, text="Нет", command=lambda: handle_response(0), bg="lightcoral")
            no_button.pack(side=LEFT, expand=True, fill=X, padx=5)

            finish_button = But(button_frame, text="Завершить", command=algo_window.destroy, bg="lightblue")
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
