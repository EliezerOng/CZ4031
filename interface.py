import tkinter as tk
from tkinter import ttk, TclError
import preprocessing as pre

plans = {}
input_textbox = qep_box = aqp_box = None
settings = pre.DEFAULT_PARAMS.copy()


def create_input_frame(container):
    frame = tk.Frame(container)
    # frame.pack()
    # frame.pack_propagate(0)

    # Enter Query
    query_label = tk.Label(frame, text='Enter Query Here: ')
    query_label.grid(row=0, pady=5, sticky='w')
    query_text = tk.Text(frame, width=100, height=15)
    query_text.grid(row=1)

    # for widget in frame.winfo_children():
    #     widget.grid(padx=5, pady=5)

    return frame, query_text


def get_value(initial):
    if initial == "ON":
        return 1
    else:
        return 0


def create_buttons_frame(container):
    frame = tk.Frame(container)

    settings_label = tk.Label(frame, text='Alternative Plan Configuration')
    settings_label.grid(row=0, pady=5, sticky='w')

    options_frame = tk.Frame(frame)
    options_frame.grid(row=1)
    row_num = 0
    for key, value in pre.DEFAULT_PARAMS.items():
        checkbox = ttk.Checkbutton(options_frame,
                                   text=key[7:],
                                   variable=tk.IntVar(),
                                   command=lambda x=key: update_settings(x),
                                   onvalue="ON",
                                   offvalue="OFF"
                                   )
        checkbox.grid(row=row_num % 10, column=row_num // 10, sticky='w')
        checkbox.state(['!alternate'])
        if get_value(value) == 1:
            checkbox.state(['selected'])
        row_num += 1

    ttk.Button(frame, text='Query Plan', command=lambda: get_plans(), width=40).grid(row=3, pady=5)

    return frame


def create_qep_frame(container):
    frame = tk.Frame(container)

    # Enter Query
    qep_label = tk.Label(frame, text='Query Execution Plan')  # TODO: Add dropdown to select between different plans
    # .grid(column=0, row=0)
    qep_label.grid(row=0, pady=5, sticky='w')
    qep_text = tk.Text(frame, width=66, height=20)
    qep_text.grid(row=1)

    return frame, qep_text


def create_aqp_frame(container):
    frame = tk.Frame(container)

    # Enter Query
    aqp_label = tk.Label(frame, text='Alternative Query Plan #')  # TODO: Add dropdown to select between different plans
    # .grid(column=0, row=0)
    aqp_label.grid(row=0, pady=5, sticky='w')
    aqp_text = tk.Text(frame, width=66, height=20)
    aqp_text.grid(row=1)

    return frame, aqp_text


def create_annotation_frame(container):
    frame = tk.Frame(container)

    # Enter Query
    annotation_label = tk.Label(frame, text='Annotations')
    # .grid(column=0, row=0)
    annotation_label.grid(row=0, pady=5, sticky='w')
    annotation_text = tk.Text(frame, width=135)
    annotation_text.grid(row=1)

    return frame


def update_settings(key):
    if settings.get(key) == "ON":
        settings.update({key: "OFF"})
        print(key, ":", settings.get(key))
    else:
        settings.update(({key: "ON"}))
        print(key, ":", settings.get(key))


def get_plans():
    query = input_textbox.get("1.0", "end-1c")

    if query == "" or not query:
        print("Empty query")
        return

    qep, qep_json = pre.get_qep(query)

    aqp, aqp_json = pre.get_aqp(settings, query)
    # TODO: Retrieve multiple AQPs

    plans['QEP'] = qep
    plans['AQP'] = aqp
    plans['QEP_JSON'] = qep_json
    plans['AQP_JSON'] = aqp_json

    qep_box.delete("1.0", "end")
    aqp_box.delete("1.0", "end")
    if plans:
        # for line in plans['QEP']:
        #     qep_box.insert(tk.END, str(line) + '\n')
        # for line in plans['AQP']:
        #     aqp_box.insert(tk.END, str(line) + '\n')
        qep_box.insert(tk.END, plans['QEP'])
        aqp_box.insert(tk.END, plans['AQP'])

# def draw_tree():

def create_main_window():
    window = tk.Tk()
    window.title("Connecting Your Query ")
    # window.resizable(0,0)
    # window.geometry('400X400')

    # Layout
    # window.columnconfigure(0, weight=1)
    # window.columnconfigure(1, weight=1)

    global input_textbox, qep_box, aqp_box

    f1 = tk.Frame(window)
    f1.grid(row=0)
    f2 = tk.Frame(window)
    f2.grid(row=1)

    input_frame, input_textbox = create_input_frame(f1)
    input_frame.grid(column=0, row=0, padx=10)

    settings_frame = create_buttons_frame(f1)
    settings_frame.grid(column=1, row=0, padx=10)

    qep_frame, qep_box = create_qep_frame(f2)
    qep_frame.grid(column=0, row=0, padx=10)

    aqp_frame, aqp_box = create_aqp_frame(f2)
    aqp_frame.grid(column=1, row=0, padx=10)

    annotation_frame = create_annotation_frame(window)
    annotation_frame.grid(columnspan=2, row=2)

    input_textbox.insert(tk.END, "select * from customer where c_custkey < 5")

    window.mainloop()


if __name__ == '__main__':
    create_main_window()
