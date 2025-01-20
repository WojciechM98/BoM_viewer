import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from bom_engine import BoM


# Functions
def open_file_from_browser(bom, treeview, frame):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                          filetypes=(("Excel files", "*.csv *.xlsx"), ("All Files", "*.*")))
    frame["text"] = filename
    load_excel_data(bom, treeview, filename)
    return filename


def open_multiple_files():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a file",
                                          filetypes=(("Excel files", "*.csv *.xlsx"), ("All Files", "*.*")))
    if not filenames:
        return tk.messagebox.showerror("Error", "No files selected")
    else:
        # For each file create df
        list_of_df = []
        for file in filenames:
            bom = BoM()
            bom.load_file(r"{}".format(file))
            list_of_df.append(bom)
        print(list_of_df)
    combined_bom = BoM()
    last_df = None
    for df in list_of_df:
        if last_df is not None:
            pass
        last_df = df
    # TODO after making Qty summing function, end this function of combining boms to generate purchase file

def load_excel_data(bom, treeview, file_path):
    # file_path = open_file_from_browser(frame1 if treeview == tv1 else frame2)
    #file_path = label_file["text"]
    try:
        excel_filepath = r"{}".format(file_path)
        bom.load_file(excel_filepath)
    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None
    except:
        tk.messagebox.showerror("Information", "Unknown error")
        return None
    load_into_treeview(bom, treeview)


def load_into_treeview(bom, treeview):
    clear_data(treeview)
    # Adding columns from DataFrame
    treeview["columns"] = list(bom.df.columns)
    for column in bom.df.columns:
        treeview.heading(column, text=column)
        treeview.column(column)

    # Adding rows from DataFrame
    for index, row in bom.df.iterrows():
        treeview.insert("", "end", values=list(row))
    treeview.pack(fill="both", expand=True)
    return None


def filename_dialog_window():
    file_path = filedialog.asksaveasfilename(initialdir="/", title="Save file", defaultextension="*.xlsx",
                                             filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
    file_path = r"{}".format(file_path)
    return file_path


def save_as(bom):
    file_path = filename_dialog_window()
    print(file_path)
    bom.save_file(file_path)


def save(frame):
    file_path = frame["text"]
    print(file_path)


def save_purchase_file(bom, main_bom):
    file_path = filename_dialog_window()
    bom_to_save = BoM()
    bom_to_save.extract_differences(bom.df, main_bom.df)
    bom_to_save.save_file(file_path)


def clear_data(treeview):
    treeview.delete(*treeview.get_children())
    return None


def copy_to_clipboard(value):
    root.clipboard_clear()
    root.clipboard_append(value)


def on_right_click(event):
    # Find position (item) in Treeview where cursor is
    item_id = tv1.identify_row(event.y)
    column_id = tv1.identify_column(event.x)

    # Take value from chosen row and column
    if item_id and column_id:
        value = tv1.set(item_id, column_id)
        # Call out context menu
        copy_to_clipboard(value)


def on_left_click(event):
    # Find position (item) in Treeview where cursor is
    item_id = tv1.identify_row(event.y)
    column_id = tv1.identify_column(event.x)
    # Take value from chosen row and column
    if item_id and column_id:
        value = tv1.set(item_id, column_id)
        column = tv1.column(column_id, "id")
        # Place holder for function that do something when left mouse button is clicked
        search_in_treeview(value, column)
        Main_BoM.search_for_value(column, value)


def get_selected_row_data(item, treeview):
    values = treeview.item(item, "values")
    # Creating dict from columns and rows
    row_data = {treeview.column(col, "id"): values[idx] for idx, col in enumerate(treeview["columns"])}
    return row_data


def multiple_xview(*args):
    tv1.xview(*args)
    tv2.xview(*args)


def search_in_treeview(value, column):
    tv2.selection_remove(tv2.selection())
    for item in tv2.get_children():
        if get_selected_row_data(item, tv2)[column] == value:
            tv2.see(item)
            tv2.selection_set(item)
            break


def combine_documents(bom, main_bom):
    combined_bom = BoM()
    combined_bom.extract_differences(bom.df, main_bom.df)
    combined_bom.combine_dataframes(combined_bom.df, main_bom.df)
    load_into_treeview(combined_bom, tv2)
    Main_BoM.df = combined_bom.df


# ------------------------ Second Window -------------------------
def top_window(bom):
    chngs_window = Toplevel(root)
    chngs_window.title('Value changer')
    chngs_window.geometry('800x550')
    tv = ttk.Treeview(chngs_window, show="headings")
    tv.place(relheight=1, relwidth=1)

    tvscrolly = Scrollbar(chngs_window, orient="vertical", command=tv1.yview)
    tvscrollx = Scrollbar(chngs_window, orient="horizontal")
    tvscrolly.pack(side="right", fill="y")
    tvscrollx.pack(side="bottom", fill="x")
    tvscrollx.config(command=multiple_xview)

    # Coppy event
    tv1.bind("<Button-3>", on_right_click)  # <Button-3> is mouse right click

    # Load into treeview
    load_into_treeview(bom, tv)


# ------------------------ BoM Engine -------------------------

# Initializing BoM Engine Classes
Main_BoM = BoM()
Second_BoM = BoM()

# ------------------------ Tkinter -------------------------

root = Tk()

# root window dimensions
root.title('BoM viewer')
root.geometry('800x550')
root.pack_propagate(False)
#root.resizable(0, 0)

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="BoM")
frame1.place(relx=0, y=0, height=200, relwidth=1)

frame2 = tk.LabelFrame(root, text="Main BoM")
frame2.place(relx=0, y=210, height=200, relwidth=1)

# Application Menu
menu_bar = Menu(root)
root["menu"] = menu_bar

# Creating menu bars
menu_file = Menu(menu_bar)
menu_edit = Menu(menu_bar)

# Creating submenus
menu_open = Menu(menu_file)
menu_save = Menu(menu_file)
menu_save_as = Menu(menu_file)

# Connecting menu bars
menu_bar.add_cascade(menu=menu_file, label="File")
menu_bar.add_cascade(menu=menu_edit, label="Edit")
menu_file.add_cascade(menu=menu_open, label="Open")
menu_file.add_cascade(menu=menu_save, label="Save")
menu_file.add_cascade(menu=menu_save_as, label="Save as")

# Adding menu items
menu_open.add_command(label="Open BoM", command=lambda: open_file_from_browser(Second_BoM, tv1, frame1))
menu_open.add_command(label="Open Main BoM", command=lambda: open_file_from_browser(Main_BoM, tv2, frame2))

menu_save.add_command(label="Save BoM", command=lambda: save(frame1))
menu_save.add_command(label="Save Main BoM", command=lambda: save(frame2))
menu_save_as.add_command(label="Save BoM as", command=lambda: save_as(Second_BoM))
menu_save_as.add_command(label="Save Main BoM as", command=lambda: save_as(Main_BoM))

menu_file.add_command(label="Create purchase file", command=lambda: save_purchase_file(Second_BoM, Main_BoM))
menu_edit.add_command(label="Add positions from BoM to Main BoM", command=lambda: combine_documents(Second_BoM, Main_BoM))



# Treeview Widget
tv1 = ttk.Treeview(frame1, show="headings")
tv1.place(relheight=1, relwidth=1)

tv2 = ttk.Treeview(frame2, show="headings")
tv2.place(relheight=1, relwidth=1)

treescrolly = Scrollbar(frame1, orient="vertical", command=tv1.yview)
treescrollx = Scrollbar(frame1, orient="horizontal")
treescrolly.pack(side="right", fill="y")
treescrollx.pack(side="bottom", fill="x")
treescrollx.config(command=multiple_xview)

# Coppy event
tv1.bind("<Button-3>", on_right_click) # <Button-3> is mouse right click

# Search for row in another DataFrame
tv1.bind("<Button-1>", on_left_click) # <Button-1> is mouse left click

# TODO  COMBINE BoMs:    combine two or more df into one - if the same rows sum Qty numbers if not concat the rest rows
#       CREATE PURCHASE FILE:    check if COMBINED BoM has the same rows as IN STOCK - if yes check if the Qty in
#                                IN STOCK is the same:
#                                --- less - subtract IN STOCK Qty from COMBINED BoM
#                                --- more - drop row from COMBINED BoM
#                                next save file as PURCHASE FILE xlsx
#       UPDATE PURCHASE Qty:    after shopping elements and knowing how many items was purchased
#                               (Excel file generated from Mouser) update PURCHASE FILE Qty values
#       COMBINE PURCHASE & IN STOCK:    concat PURCHASE FILE with IN STOCK. If:
#                                       --- row matched - sum up Qty value
#                                       --- row not matched - add row to IN STOCK

# Initial data load - for testing purpose only
load_excel_data(Second_BoM, tv1, "BoM_half_1.csv")
load_excel_data(Main_BoM, tv2, "BoM_DevKeyboard_1.csv")

test = BoM()
test.merge_and_sum_duplicates([Second_BoM.df, Second_BoM.df])
test.save_file("test.xlsx")
# top_window(Main_BoM)

root.mainloop()
