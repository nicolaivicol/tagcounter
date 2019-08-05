import tkinter as tk
from tkinter import ttk
import json
from tagcounter.db import DbRecSiteTagCounts

class MainWindowGUI:
    def __init__(self, master, db_session, get_from_site, view_from_db, write_to_db):

        self.master = master
        self.db_session = db_session
        self.get_from_site = get_from_site
        self.view_from_db = view_from_db
        self.write_to_db = write_to_db

        master.title("Tag counter")
        # master.geometry('400x400')

        self.url = tk.StringVar(master)  # url of page to be read
        self.url.set('')

        tk.Label(master, text="Write or select web page from list:").grid(row=1, column=0)

        self.combo_site = ttk.Combobox(
            master=master,
            textvariable=self.url,
            values = sorted([r.site_url for r in db_session.query(DbRecSiteTagCounts).all()]))
        self.combo_site.grid(row=1, column=1)

        self.button_get = ttk.Button(
            master=master,
            text="Get from web page",
            command=lambda: self.action_button_get())
        self.button_get.grid(row=1, column=2)

        self.button_view = ttk.Button(
            master=master,
            text="View from data base",
            command=lambda: self.action_button_view())
        self.button_view.grid(row=1, column=3)

        self.txt_box_show = tk.Text(master=master) #.gdri(row=2) # , height=10, width=30
        self.txt_box_show.grid(row=2, column=0, columnspan=4, rowspan=2, padx=5, pady=5, sticky="nsew")

    def action_button_get(self):
        self.txt_box_show.delete(1.0, tk.END)
        tags_count_json = self.get_from_site(self.url.get())
        self.write_to_db(self.url.get(), tags_count_json, self.db_session)
        self.txt_box_show.insert(tk.END, json.dumps(json.loads(tags_count_json), indent=2))

    def action_button_view(self):
        self.txt_box_show.delete(1.0, tk.END)
        tags_count_json = self.view_from_db(self.url.get(), self.db_session)
        self.txt_box_show.insert(tk.END, json.dumps(json.loads(tags_count_json), indent=2))
