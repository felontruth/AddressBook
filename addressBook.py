import pickle
import os.path
from tkinter import *
import tkinter.messagebox
from tkinter import ttk


class Address:
    """__init__() function as the class constructor"""

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


class AddressBook:
    def __init__(self, parent, title):
        self.parent = parent

        self.parent.title(title)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.initialization()
        self.bind()
        self.set_listbox()

        self.lbx_names.focus_set()

    def bind(self):
        self.lbx_names.bind('<ButtonRelease-1>', self.on_click_lb)
        self.lbx_names.bind('<KeyRelease>', self.on_click_lb)

    def which_selected(self):
        return int(self.lbx_names.curselection()[0])

    def on_click_lb(self, event=None):
        self.set_data()

    def set_data(self):
        self.name_var.set(self.lst_addresses[self.which_selected()].name)
        self.email_var.set(self.lst_addresses[self.which_selected()].email)
        self.phone_var.set(self.lst_addresses[self.which_selected()].phone)

    #populates listbox with all the names
    def set_listbox(self):
        self.lbx_names.delete(0, END)
        for dat in range(len(self.lst_addresses)):
            self.lbx_names.insert(END, self.lst_addresses[dat].name)
        self.lbx_names.selection_set(0) #selected index in listbox

    def initialization(self):
        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=YES)

        self.name_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()

        self.status_bar = Label(main_frame, text="Felon -2016-", relief=SUNKEN, bd=1).pack(side=BOTTOM, fill=X)

        frame1 = Frame(main_frame, bd=10)
        frame1.pack(fill=BOTH, expand=YES, side=LEFT)

        scroll = ttk.Scrollbar(frame1, orient=VERTICAL)
        self.lbx_names = Listbox(frame1, width=30, yscrollcommand=scroll.set)

        self.lbx_names.pack(fill=Y, side=LEFT)
        scroll.config(command=self.lbx_names.yview)
        scroll.pack(side=LEFT, fill=Y)

        frame2 = Frame(main_frame, bd=10)
        frame2.pack(fill=BOTH, expand=YES, side=RIGHT)

        frame3 = Frame(frame2)
        frame3.pack(side=TOP, expand=YES)

        Label(frame3, text='Full Name').grid(row=0, column=0, sticky=W)
        self.ent_name = Entry(frame3, textvariable=self.name_var, width=30)
        self.ent_name.grid(row=0, column=1)

        Label(frame3, text='Email').grid(row=1, column=0, sticky=W)
        self.ent_email = Entry(frame3, textvariable=self.email_var, width=30)
        self.ent_email.grid(row=1, column=1)

        Label(frame3, text='Phone').grid(row=2, column=0, sticky=W)
        self.ent_phone = Entry(frame3, textvariable=self.phone_var, width=30)
        self.ent_phone.grid(row=2, column=1)

        frame4 = Frame(frame2)
        frame4.pack(side=BOTTOM, expand=YES)

        self.btn_new = ttk.Button(frame4, text='New', command=self.on_new, width=5)
        self.btn_new.pack(side=LEFT)
        self.btn_add = ttk.Button(frame4, text='Add', command=self.on_add, width=5)
        self.btn_add.pack(side=LEFT)
        self.btn_mod = ttk.Button(frame4, text='Mod', command=self.on_mod, width=5)
        self.btn_mod.pack(side=LEFT)
        self.btn_del = ttk.Button(frame4, text='Del', command=self.on_del, width=5)
        self.btn_del.pack(side=LEFT)

        self.lst_addresses = self.load_address()

    def on_new(self, event=None):
        self.ent_name.delete(0, END)
        self.ent_email.delete(0, END)
        self.ent_phone.delete(0, END)

    def on_add(self, event=None):
        address = Address(self.name_var.get(), self.email_var.get(), self.phone_var.get())
        self.lst_addresses.append(address)
        self.set_listbox()
        self.save_address()

    def on_mod(self, event=None):
        self.lst_addresses[self.which_selected()].name = self.name_var.get()
        self.lst_addresses[self.which_selected()].email = self.email_var.get()
        self.lst_addresses[self.which_selected()].phone = self.phone_var.get()
        self.set_listbox()
        self.modify_address()

    def on_del(self, event=None):
        del self.lst_addresses[self.which_selected()]
        self.set_listbox()
        self.on_new()
        self.delete_address()

    def save_address(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lst_addresses, outfile)
        tkinter.messagebox.showinfo("Address Saved", "A new address have been saved")
        outfile.close()

    def modify_address(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lst_addresses, outfile)
        tkinter.messagebox.showinfo("Address Changed", "The changes have been saved")
        outfile.close()

    def delete_address(self):
            outfile = open("address.dat", "wb")
            pickle.dump(self.lst_addresses, outfile)
            tkinter.messagebox.showinfo("Address Deleted", "The address has been deleted")
            outfile.close()

    def load_address(self):
        if not os.path.isfile("address.dat"):
            return []  # Return an empty list
        try:
            infile = open("address.dat", "rb")
            lst_addresses = pickle.load(infile)
        except EOFError:
            lst_addresses = []
        infile.close()
        return lst_addresses

    def on_exit(self, event=None):
        self.parent.destroy()

if __name__ == '__main__':
    root = Tk()

    application = AddressBook(root, "Demo Application - Objects in Python")

    root.mainloop()