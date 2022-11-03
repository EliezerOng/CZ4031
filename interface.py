import tkinter as tk
from tkinter import ttk, TclError
import preprocessing as pre

plans = {}
input_query = ""


def create_input_frame(container):
    frame = tk.Frame(container, width=400, height=180)
    frame.pack()
    frame.pack_propagate(0)

    # Enter Query
    query_label = tk.Label(frame, text='Enter Query Here: ')
    # .grid(column=0, row=0)
    query_label.pack(side=tk.LEFT)
    query_text = tk.Text(frame, width=40, height=10)
    query_text.pack(side=tk.RIGHT)

    global input_query
    input_query = query_text.get("1.0", "end-1c")

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame


def create_visualizer_frame(container):
    frame = tk.Frame(container, width=400, height=180)

    # Enter Query
    visualizer_label = tk.Label(frame, text='Showing plan #')  # TODO: Add dropdown to select between different plans
    # .grid(column=0, row=0)
    visualizer_label.grid(column=0, row=0, pady=5, sticky=tk.W)
    visualizer_text = tk.Text(frame, width=40, height=10)
    visualizer_text.grid(column=0, row=1)

    if plans:
        visualizer_text.insert(tk.END, plans['QEP'])

    return frame


def create_annotation_frame(container):
    frame = tk.Frame(container, width=400, height=180)

    # Enter Query
    annotation_label = tk.Label(frame, text='Annotations')
    # .grid(column=0, row=0)
    annotation_label.grid(column=0, row=0, pady=5, sticky=tk.W)
    annotation_text = tk.Text(frame, width=40, height=10)
    annotation_text.grid(column=0, row=1)

    return frame


def create_button_frame(container):
    frame = ttk.Frame(container, width=400, height=180)

    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Query Plan', command=lambda: get_plans(input_query, {})).grid(column=0, row=0)

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame


def get_plans(query, disabled_settings: dict):
    params = pre.DEFAULT_PARAMS
    qep = pre.get_qep(query)

    params.update(disabled_settings)
    aqp = pre.get_aqp(params, query)
    # TODO: Retrieve multiple AQPs

    plans['QEP'] = qep
    plans['AQP'] = aqp


def create_main_window():
    window = tk.Tk()
    window.title("Connecting Your Query ")
    # window.resizable(0,0)
    # window.geometry('400X400')

    # Layout
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    input_frame = create_input_frame(window)
    input_frame.grid(row=0, columnspan=2)

    button_frame = create_button_frame(window)
    button_frame.grid(row=1, columnspan=2)

    visualizer_frame = create_visualizer_frame(window)
    visualizer_frame.grid(column=0, row=2)

    annotation_frame = create_annotation_frame(window)
    annotation_frame.grid(column=1, row=2)

    window.mainloop()


if __name__ == '__main__':
    create_main_window()
