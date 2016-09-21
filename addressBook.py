#!/usr/bin/python
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

    def changeName(self, name):
        self.name = name

    def changeEmail(self, email):
        self.email = email

    def changePhone(self, phone):
        self.phone = phone


class AddressBook:
    def __init__(self, parent, title):
        self.parent = parent

        self.parent.title(title)

        self.parent.protocol("WM_DELETE_WINDOW", self.onExit)

        self.initialization()
        self.bind()
        self.setListbox()

        self.lbxNames.focus_set()

    def bind(self):
        self.lbxNames.bind('<ButtonRelease-1>', self.onClickLB)
        self.lbxNames.bind('<KeyRelease>', self.onClickLB)

    def whichSelected(self):
        return int(self.lbxNames.curselection()[0])

    def onClickLB(self, event=None):
        self.setData()

    def setData(self):
        self.nameVar.set(self.lstAddresses[self.whichSelected()].name)
        self.emailVar.set(self.lstAddresses[self.whichSelected()].email)
        self.phoneVar.set(self.lstAddresses[self.whichSelected()].phone)

    #populates listbox with all the names
    def setListbox(self):
        self.lbxNames.delete(0, END)
        for dat in range(len(self.lstAddresses)):
            self.lbxNames.insert(END, self.lstAddresses[dat].name)
        self.lbxNames.selection_set(0) #selected index in listbox

    def initialization(self):
        mainFrame = Frame(self.parent)
        mainFrame.pack(fill=BOTH, expand=YES)

        self.nameVar = StringVar()
        self.emailVar = StringVar()
        self.phoneVar = StringVar()

        self.statusBar = Label(mainFrame, text="Felon -2016-", relief=SUNKEN, bd=1).pack(side=BOTTOM, fill=X)

        frame1 = Frame(mainFrame, bd=10)
        frame1.pack(fill=BOTH, expand=YES, side=LEFT)

        scroll = ttk.Scrollbar(frame1, orient=VERTICAL)
        self.lbxNames = Listbox(frame1, width=30, yscrollcommand=scroll.set)

        self.lbxNames.pack(fill=Y, side=LEFT)
        scroll.config(command=self.lbxNames.yview)
        scroll.pack(side=LEFT, fill=Y)

        frame2 = Frame(mainFrame, bd=10)
        frame2.pack(fill=BOTH, expand=YES, side=RIGHT)

        frame3 = Frame(frame2)
        frame3.pack(side=TOP, expand=YES)

        Label(frame3, text='Full Name').grid(row=0, column=0, sticky=W)
        self.entName = Entry(frame3, textvariable=self.nameVar, width=30)
        self.entName.grid(row=0, column=1)

        Label(frame3, text='Email').grid(row=1, column=0, sticky=W)
        self.entEmail = Entry(frame3, textvariable=self.emailVar, width=30)
        self.entEmail.grid(row=1, column=1)

        Label(frame3, text='Phone').grid(row=2, column=0, sticky=W)
        self.entPhone = Entry(frame3, textvariable=self.phoneVar, width=30)
        self.entPhone.grid(row=2, column=1)

        frame4 = Frame(frame2)
        frame4.pack(side=BOTTOM, expand=YES)

        self.btnNew = ttk.Button(frame4, text='New', command=self.onNew, width=5).pack(side=LEFT) #first element
        self.btnAdd = ttk.Button(frame4, text='Add', command=self.onAdd, width=5).pack(side=LEFT) #step backward
        self.btnMod = ttk.Button(frame4, text='Mod', command=self.onMod, width=5).pack(side=LEFT)  #step forward
        self.btnDel = ttk.Button(frame4, text='Del', command=self.onDel, width=5).pack(side=LEFT) #last element

        self.lstAddresses = self.loadAddress()

    def onNew(self, event=None):
        self.entName.delete(0, END)
        self.entEmail.delete(0, END)
        self.entPhone.delete(0, END)

    def onAdd(self, event=None):
        address = Address(self.nameVar.get(), self.emailVar.get(), self.phoneVar.get())
        self.lstAddresses.append(address)
        self.setListbox()
        self.saveAddress()

    def onMod(self, event=None):
        self.lstAddresses[self.whichSelected()].name = self.nameVar.get()
        self.lstAddresses[self.whichSelected()].email = self.emailVar.get()
        self.lstAddresses[self.whichSelected()].phone = self.phoneVar.get()
        self.setListbox()
        self.modifyAddress()

    def onDel(self, event=None):
        del self.lstAddresses[self.whichSelected()]
        self.setListbox()
        self.onNew()
        self.deleteAddress()

    def saveAddress(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lstAddresses, outfile)
        tkinter.messagebox.showinfo("Address Saved", "A new address have been saved")
        outfile.close()

    def modifyAddress(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lstAddresses, outfile)
        tkinter.messagebox.showinfo("Address Changed", "The changes have been saved")
        outfile.close()

    def deleteAddress(self):
            outfile = open("address.dat", "wb")
            pickle.dump(self.lstAddresses, outfile)
            tkinter.messagebox.showinfo("Address Deleted", "The address has been deleted")
            outfile.close()

    def loadAddress(self):
        if not os.path.isfile("address.dat"):
            return []  # Return an empty list
        try:
            infile = open("address.dat", "rb")
            lstAddresses = pickle.load(infile)
        except EOFError:
            lstAddresses = []
        infile.close()
        return lstAddresses

    def onExit(self, event=None):
        self.parent.destroy()

if __name__ == '__main__':
    root = Tk()

    application = AddressBook(root, "Demo Application - Objects in Python")

    root.mainloop()