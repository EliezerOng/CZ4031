import tkinter as tk
from tkinter import ttk, TclError
import preprocessing as pre

plans = {}
input_textbox = None
visualizer_box = None
settings = pre.DEFAULT_PARAMS


def create_input_frame(container):
    frame = tk.Frame(container, width=400, height=180)
    # frame.pack()
    # frame.pack_propagate(0)

    # Enter Query
    query_label = tk.Label(frame, text='Enter Query Here: ')
    query_label.grid(column=0, row=0, pady=5, sticky=tk.W)
    query_text = tk.Text(frame, width=40, height=15)
    query_text.grid(column=0, row=1)

    # for widget in frame.winfo_children():
    #     widget.grid(padx=5, pady=5)

    return frame, query_text


def create_button_frame(container):
    frame = ttk.Frame(container)

    ttk.Button(frame, text='Query Plan', command=lambda: get_plans()).grid(pady=5)

    # for widget in frame.winfo_children():
    #     widget.grid(padx=5, pady=5)

    return frame


def create_settings_frame(container):
    frame = ttk.Frame(container, width=400, height=180)

    settings_label = tk.Label(frame, text='Alternative Plan Configuration')
    settings_label.grid(column=0, row=0, pady=5, sticky=tk.W)

    # options_frame = ttk.Frame(frame, width=40, height=15)

    def get_value(initial):
        if initial == "ON":
            return 1
        else:
            return 0

    row_num = 0
    for key, value in pre.DEFAULT_PARAMS.items():
        ttk.Checkbutton(frame,
                        text=key[7:],
                        variable=tk.IntVar(value=get_value(value)),
                        command=lambda: update_settings(key),
                        onvalue="ON",
                        offvalue="OFF").grid(row=row_num % 10 + 1, column=row_num // 10, sticky='w')
        row_num += 1

    return frame


def create_visualizer_frame(container):
    frame = tk.Frame(container, width=400, height=180)

    # Enter Query
    visualizer_label = tk.Label(frame, text='Showing plan #')  # TODO: Add dropdown to select between different plans
    # .grid(column=0, row=0)
    visualizer_label.grid(column=0, row=0, pady=5, sticky=tk.W)
    visualizer_text = tk.Text(frame, width=40, height=10)
    visualizer_text.grid(column=0, row=1)

    return frame, visualizer_text


def create_annotation_frame(container):
    frame = tk.Frame(container, width=400, height=180)

    # Enter Query
    annotation_label = tk.Label(frame, text='Annotations')
    # .grid(column=0, row=0)
    annotation_label.grid(column=0, row=0, pady=5, sticky=tk.W)
    annotation_text = tk.Text(frame, width=40, height=10)
    annotation_text.grid(column=0, row=1)

    return frame


def update_settings(key):
    if settings.get(key) == "ON":
        settings.update({key: "OFF"})
        print(settings.get(key))
    else:
        settings.update(({key: "ON"}))
        print(settings.get(key))


def get_plans():
    query = input_textbox.get("1.0", "end-1c")

    if query == "" or not query:
        print("Empty query")
        return

    qep = pre.get_qep(query)

    # aqp = pre.get_aqp(settings, query)
    # TODO: Retrieve multiple AQPs

    plans['QEP'] = qep
    # plans['AQP'] = aqp

    if plans:
        visualizer_box.insert(tk.END, plans['QEP'])


def create_main_window():
    window = tk.Tk()
    window.title("Connecting Your Query ")
    # window.resizable(0,0)
    # window.geometry('400X400')

    # Layout
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    global input_textbox, visualizer_box

    input_frame, input_textbox = create_input_frame(window)
    input_frame.grid(column=0, row=0)

    settings_frame = create_settings_frame(window)
    settings_frame.grid(column=1, row=0)

    button_frame = create_button_frame(window)
    button_frame.grid(columnspan=2, row=1)

    visualizer_frame, visualizer_box = create_visualizer_frame(window)
    visualizer_frame.grid(column=0, row=2)

    annotation_frame = create_annotation_frame(window)
    annotation_frame.grid(column=1, row=2)

    # input_textbox.insert(tk.END, "select * from customer where c_custkey < 5")

    window.mainloop()


if __name__ == '__main__':
    create_main_window()
