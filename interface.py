import tkinter as tk
from tkinter import ttk
import preprocessing as pre
import annotation as an
from pptree import *

plans = {}
input_textbox = qep_box = aqp_box = annotation_box = None
settings = pre.DEFAULT_PARAMS.copy()
checkboxes = []
aqp_mode = 'Single'
selection = None


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


def create_options(container):
    arr = []
    row_num = 0
    settings['enable_partitionwise_join'] = "ON"
    settings['enable_partitionwise_aggregate'] = "ON"
    for key in settings:
        option = tk.IntVar(value=1)
        checkbox = ttk.Checkbutton(container,
                                   text=key[7:],
                                   variable=option,
                                   command=lambda x=key, y=option: update_settings(x, y.get()),
                                   onvalue=1,
                                   offvalue=0
                                   )
        checkbox.grid(row=row_num % 10, column=row_num // 10, sticky='w')
        checkbox.state(['selected'])
        arr.append(checkbox)
        print(key, "=", option.get())
        row_num += 1

    return arr


def create_buttons_frame(container):
    frame = tk.Frame(container)

    settings_label = tk.Label(frame, text='Alternative Plan Configuration')
    settings_label.grid(row=0, pady=5, sticky='w')

    selected_mode = tk.StringVar()
    mode = ttk.Combobox(frame, textvariable=selected_mode, width=10)
    mode.grid(row=0, sticky='e')
    mode['values'] = ['Single', 'Multiple']
    mode['state'] = 'readonly'
    mode.bind('<<ComboboxSelected>>', lambda x: update_mode(selected_mode.get()))
    mode.current(0)

    options_frame = tk.Frame(frame)
    options_frame.grid(row=1)

    options = create_options(options_frame)

    ttk.Button(frame, text='Query Plan', command=lambda: get_plans(), width=40).grid(row=3, pady=5)

    return frame, options


def create_treeview(container):
    columns = 'total_cost'
    tree = ttk.Treeview(container, columns=columns)
    tree.pack()
    tree.column('#0', width=400)
    tree.column('total_cost', width=130)
    # tree.column('output', width=300)
    tree.heading('#0', text='Operator')
    tree.heading('total_cost', text='Total Cost')
    # tree.heading('output', text='Output')

    return tree


def create_qep_frame(container):
    frame = tk.Frame(container)

    # Enter Query
    qep_label = tk.Label(frame, text='Query Execution Plan')
    # .grid(column=0, row=0)
    qep_label.grid(row=0, pady=5, sticky='w')
    # qep_text = tk.Text(frame, width=66, height=20)
    # qep_text.grid(row=1)

    tree_frame = tk.Frame(frame)
    tree_frame.grid(row=1)

    tree = create_treeview(tree_frame)

    return frame, tree


def create_aqp_frame(container):
    frame = tk.Frame(container)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=15)

    aqp_id = tk.StringVar()
    showing = ttk.Combobox(frame, textvariable=aqp_id, width=25)
    showing.grid(row=0, column=1, sticky='w')
    showing['values'] = ['1']
    showing['state'] = 'readonly'
    showing.bind('<<ComboboxSelected>>', lambda x: update_treeview(plans['AQP'][int(aqp_id.get()) - 1]))
    showing.current(0)

    # Enter Query
    aqp_label = tk.Label(frame, text='Alternative Query Plan #')
    # .grid(column=0, row=0)
    aqp_label.grid(row=0, column=0, pady=5, sticky='w')
    # aqp_text = tk.Text(frame, width=66, height=20)
    # aqp_text.grid(row=1)

    tree_frame = tk.Frame(frame)
    tree_frame.grid(row=1, columnspan=2)

    tree = create_treeview(tree_frame)

    return frame, tree, showing


def create_annotation_frame(container):
    frame = tk.Frame(container)

    # Enter Query
    annotation_label = tk.Label(frame, text='Annotations')
    # .grid(column=0, row=0)
    annotation_label.grid(row=0, pady=5, sticky='w')
    annotation_text = tk.Text(frame, width=135)
    annotation_text.grid(row=1)

    return frame, annotation_text


def update_settings(key, value):
    if value == 0:
        settings.update({key: "OFF"})
        print(key, ":", settings.get(key))
    if value == 1:
        settings.update({key: "ON"})
        print(key, ":", settings.get(key))


def update_mode(mode):
    global aqp_mode
    aqp_mode = mode

    if mode == 'Multiple':
        for i in settings:
            settings[i] = 'OFF'
        for checkbox in checkboxes:
            checkbox.state(['!selected'])
    else:
        for i in settings:
            settings[i] = 'ON'
        for checkbox in checkboxes:
            checkbox.state(['selected'])


def update_treeview(plan):
    if plan == 'QEP':
        box = qep_box
        root = plans['QEP']
    elif plan == 'AQP':
        box = aqp_box
        root = plans['AQP']
    else:
        box = aqp_box
        root = plan

    box.delete(*box.get_children())

    root_id = box.insert('', 'end', text=root.op, values=root.cost, open=True)
    queue = [(root_id, root)]

    while queue:
        pid, parent = queue.pop(0)
        if parent.children:
            for child in parent.children:
                cid = box.insert(pid, 'end', text=child.op, values=child.cost, open=True)
                queue.append((cid, child))


def get_annotation(annotations):
    count = 1
    for annotation in annotations:
        annotation_box.insert(tk.END, 'Step {}: {} \n'.format(count, annotation))
        count += 1


def get_plans():
    query = input_textbox.get("1.0", "end-1c")

    if query == "" or not query:
        print("Empty query")
        return

    qep = pre.get_qep(query)

    if aqp_mode == 'Multiple':
        aqp = pre.get_multi_aqps(settings, query)
    else:
        aqp = pre.get_aqp(settings, query)

    plans['QEP'] = qep
    plans['AQP'] = aqp

    if not plans:
        return

    global selection

    update_treeview('QEP')
    get_annotation(an.build_annotation(qep))

    if aqp_mode == 'Multiple' and len(aqp) > 0:
        selection['values'] = [str(i + 1) for i in range(len(plans['AQP']))]
        print("here", aqp)
        update_treeview(aqp[0])
    elif aqp_mode == 'Single':
        selection['values'] = ['1']
        update_treeview('AQP')
    elif aqp_mode == 'Multiple' and len(aqp) == 0:
        selection['values'] = ['No distinct plan to display']

    selection.current(0)


def create_main_window():
    window = tk.Tk()
    window.title("Connecting Your Query ")
    # window.resizable(0,0)
    # window.geometry('400X400')

    # Layout
    # window.columnconfigure(0, weight=1)
    # window.columnconfigure(1, weight=1)

    global input_textbox, qep_box, aqp_box, annotation_box, checkboxes, selection

    f1 = tk.Frame(window)
    f1.grid(row=0)
    f2 = tk.Frame(window)
    f2.grid(row=1)

    input_frame, input_textbox = create_input_frame(f1)
    input_frame.grid(column=0, row=0, padx=10)

    settings_frame, checkboxes = create_buttons_frame(f1)
    settings_frame.grid(column=1, row=0, padx=10)

    qep_frame, qep_box = create_qep_frame(f2)
    qep_frame.grid(column=0, row=0, padx=10)

    aqp_frame, aqp_box, selection = create_aqp_frame(f2)
    aqp_frame.grid(column=1, row=0, padx=10)

    annotation_frame, annotation_box = create_annotation_frame(window)
    annotation_frame.grid(columnspan=2, row=2)

    # Example query
    input_textbox.insert(tk.END, ("select\n"
                                  "	ps_partkey,\n"
                                  "	sum(ps_supplycost * ps_availqty) as value\n"
                                  "from\n"
                                  "	partsupp,\n"
                                  "	supplier,\n"
                                  "	nation\n"
                                  "where\n"
                                  "	ps_suppkey = s_suppkey\n"
                                  "	and s_nationkey = n_nationkey\n"
                                  "	and n_name = 'GERMANY'\n"
                                  "	and ps_supplycost > 10000\n"
                                  "	and s_acctbal < 10000\n"
                                  "group by\n"
                                  "	ps_partkey having\n"
                                  "		sum(ps_supplycost * ps_availqty) > (\n"
                                  "			select\n"
                                  "				sum(ps_supplycost * ps_availqty) * 0.0001000000\n"
                                  "			from\n"
                                  "				partsupp,\n"
                                  "				supplier,\n"
                                  "				nation\n"
                                  "			where\n"
                                  "				ps_suppkey = s_suppkey\n"
                                  "				and s_nationkey = n_nationkey\n"
                                  "				and n_name = 'GERMANY'\n"
                                  "		)\n"
                                  "order by\n"
                                  "	value desc"))

    window.mainloop()


if __name__ == '__main__':
    create_main_window()
