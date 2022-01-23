from tkinter import *
from tkinter import messagebox
import random
import mysql.connector
import pandas as pd
import datetime
import openpyxl
from openpyxl.styles import Alignment


class Bank:
    def __init__(self):
        # self.transfer()
        self.DB = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="accountholders"
        )
        self.runner = self.DB.cursor()
        self.design_body()

    def submit_details(self):
        if(self.user_name.get() == "" or self.user_id.get() == "" or (self.user_pin.get() == "" or len(self.user_pin.get()) != 4 or self.user_pin.get().isdecimal() == False) or self.initial_amount.get().isdecimal() == False or int(self.initial_amount.get()) < 0):
            messagebox.showerror("Invalid Information", "Please fill the details correctly")
        else:
            account_no = None
            while True:
                account_no = random.randint(10000000,99999999)
                self.runner.execute(f'SELECT * FROM Details WHERE AccountNo = {account_no}')
                if(len(self.runner.fetchall())==0):
                    break
            try:
                self.runner.execute(f'INSERT INTO Details VALUES (\'{self.user_name.get()}\', \'{self.user_id.get()}\', {int(self.user_pin.get())}, {int(self.initial_amount.get())},{account_no});')
                messagebox.showinfo("Success","Your account is created and your Account No. is "+str(account_no))
                self.user_details.destroy()
            except:
                messagebox.showerror("User ID already available", "Please choose another User ID")
            finally:
                self.DB.commit()
    def createAccount(self):
        self.user_details = Tk()
        self.t1 = Label(self.user_details,text="Your Full Name",font=("Times New Roman",15))
        self.t1.grid(row=0,sticky="e")
        self.t2 = Label(self.user_details,text="User ID",font=("Times New Roman",15))
        self.t2.grid(row=1,sticky="e")
        self.t3 = Label(self.user_details,text="Pin",font=("Times New Roman",15))
        self.t3.grid(row=2,sticky="e")
        self.t4 = Label(self.user_details,text="Initial Amount",font=("Times New Roman",15))
        self.t4.grid(row=3,sticky="e")
        self.user_name = Entry(self.user_details,font=("Times New Roman",15))
        self.user_name.grid(row=0,column=1)
        self.user_id = Entry(self.user_details,font=("Times New Roman",15))
        self.user_id.grid(row=1,column=1)
        self.user_pin = Entry(self.user_details,font=("Times New Roman",15))
        self.user_pin.grid(row=2,column=1)
        self.initial_amount = Entry(self.user_details,font=("Times New Roman",15),text="0")
        self.initial_amount.grid(row=3,column=1)
        self.submit_btn = Button(self.user_details,text="Create Account",font=("Times New Roman",15),command=self.submit_details)
        self.submit_btn.grid(row=4,column=1)
        self.user_details.mainloop()
    def creditAmount(self,amount,user_id):
        if(amount.isdecimal() == False):
            messagebox.showerror("Invalid Credit Amount","Please enter a valid credit amount")
        else:
            self.runner.execute(f'UPDATE Details SET Balance = Balance + {int(amount)} WHERE User_ID = \'{user_id}\'')
            self.DB.commit()
            self.credit_window.destroy()
            messagebox.showinfo("Success","Your amount is credited to your account")

    def debitAmount(self,amount,user_id):
        self.runner.execute(f'SELECT Balance FROM Details WHERE User_ID = \'{user_id}\'')
        balance = self.runner.fetchall()[0][0]
        if(amount.isdecimal() == False):
            messagebox.showerror("Invalid Debit Amount","Please enter a valid debit amount")
        elif(int(amount) > balance):
            messagebox.showerror("Insufficient Amount","There is not sufficient money in your account to debit")
        else:
            self.runner.execute(f'UPDATE Details SET Balance = Balance - {int(amount)} WHERE User_ID = \'{user_id}\'')
            self.DB.commit()
            self.debit_window.destroy()
            messagebox.showinfo("Success","Your amount is debited from your account")
    def credit(self,user_id):
        self.credit_window = Tk()
        self.credit_window.geometry('500x400')
        self.credit_window.resizable(False,False)
        heading = Label(self.credit_window,text="Credit Amount To Your Account",font=("Calibry",15,'bold'))
        heading.place(relx=0.20,rely=0.2)
        text = Label(self.credit_window,text="Credit Amount",font=("Times New Roman",17))
        text.place(relx=0.12,rely=0.4)
        self.credit_amount = Entry(self.credit_window,text="0",font=("Times New Roman",17))
        self.credit_amount.place(rely=0.41,relx=0.42)
        btn = Button(self.credit_window,text="Credit",font=("Calibry",15),background='orange',command=lambda: self.creditAmount(self.credit_amount.get(),user_id))
        btn.place(relx=0.4,rely=0.6)
        self.credit_window.mainloop()
    def debit(self,user_id):
        self.debit_window = Tk()
        self.debit_window.geometry('500x400')
        self.debit_window.resizable(False,False)
        heading = Label(self.debit_window,text="Debit Amount From Your Account",font=("Calibry",15,'bold'))
        heading.place(relx=0.20,rely=0.2)
        text = Label(self.debit_window,text="Debit Amount",font=("Times New Roman",17))
        text.place(relx=0.12,rely=0.4)
        self.debit_amount = Entry(self.debit_window,font=("Times New Roman",17),text="0")
        self.debit_amount.place(rely=0.41,relx=0.42)
        btn = Button(self.debit_window,text="Debit",font=("Calibry",15),background='orange',command=lambda: self.debitAmount(self.debit_amount.get(),user_id))
        btn.place(relx=0.4,rely=0.6)
        self.debit_window.mainloop()
    def checkBalance(self,user_id):
        self.runner.execute(f'SELECT Balance FROM Details WHERE User_ID = \'{user_id}\'')
        balance = self.runner.fetchall()[0][0]
        messagebox.showinfo("Account Balance",f'The Balance of your Account is Rs.{balance}')
    def transfer_amount(self,user_id,amount,ac):
        try:
            int(ac)
        except:
            messagebox.showerror("Invalid A/C no.","PLease enter valid account no.")
        else:
            self.runner.execute(f'SELECT * FROM Details WHERE AccountNo = {int(ac)}')
            if(len(self.runner.fetchall()) == 0):
                messagebox.showerror("Error","Account does not exist")
            else:
                self.runner.execute(f'SELECT Balance FROM Details WHERE User_ID = \'{user_id}\'')
                balance = self.runner.fetchall()[0][0]
                if (amount.isdecimal() == False):
                    messagebox.showerror("Invalid Amount","Please enter a valid amount")
                elif (int(amount) > balance):
                    messagebox.showerror("Insufficient Amount","There is not sufficient money in your account to transfer")
                else:
                    self.runner.execute(f'UPDATE Details SET Balance = Balance - {int(amount)} WHERE User_ID = \'{user_id}\'')
                    self.runner.execute(f'UPDATE Details SET Balance = Balance + {int(amount)} WHERE AccountNo = {int(ac)}')
                    self.DB.commit()
                    self.transfer_window.destroy()
                    self.runner.execute(f'SELECT AccountNo FROM Details WHERE User_ID = \'{user_id}\'')
                    from_ac = self.runner.fetchall()[0][0]
                    today = datetime.date.today()
                    time = datetime.datetime.now()
                    df = pd.DataFrame({"From Account":[from_ac],"To Account":[int(ac)],"Amount":[int(amount)],"Date":[today.strftime("%d-%m-%Y")],"Time":[time.strftime("%I h-%M m-%S s")]})
                    read = pd.read_excel('transfer_details.xlsx')
                    read = read.append(df)
                    writer = pd.ExcelWriter('transfer_details.xlsx',engine="xlsxwriter")
                    read.to_excel(writer,index=False,header=True,sheet_name='Sheet1')
                    writer.sheets['Sheet1'].set_column(0,0,12)
                    writer.sheets['Sheet1'].set_column(1,1,12)
                    writer.sheets['Sheet1'].set_column(2,2,10)
                    writer.sheets['Sheet1'].set_column(3,3,9.67)
                    writer.sheets['Sheet1'].set_column(4,4,12.56)
                    writer.save()
                    messagebox.showinfo("Success","Your amount is transferred to the other account")

    def transfer(self,user_id):
        self.transfer_window = Tk()
        self.transfer_window.geometry('500x400')
        self.transfer_window.resizable(False,False)
        heading = Label(self.transfer_window,text="Transfer Amount",font=("Calibry",15,'bold'))
        heading.place(relx=0.35,rely=0.2)
        text = Label(self.transfer_window,text="Account No.",font=("Times New Roman",17))
        text.place(relx=0.15,rely=0.4)
        account_no = Entry(self.transfer_window,font=("Times New Roman",17))
        account_no.place(rely=0.4,relx=0.42)
        text1 = Label(self.transfer_window,text="Amount",font=("Times New Roman",17))
        text1.place(relx=0.23,rely=0.5)
        amount = Entry(self.transfer_window,font=("Times New Roman",17))
        amount.place(rely=0.5,relx=0.42)
        amount.insert(0,"0")
        btn = Button(self.transfer_window,text="Transfer",font=("Calibry",15),background='orange',command=lambda: self.transfer_amount(user_id,amount.get(),account_no.get()))
        btn.place(relx=0.4,rely=0.7)
        self.transfer_window.mainloop()
    def user_dashboard(self):
        self.runner.execute(f'SELECT * FROM Details WHERE User_ID = \'{self.ID.get()}\' AND Pin = \'{self.pin.get()}\'')
        records = self.runner.fetchall()
        if len(records)<=0:
            messagebox.showerror("Invalid Credentials","Invalid User ID or Pin")
        else:
            user_id = self.ID.get()
            self.login_form.destroy()
            self.dashboard = Tk()
            self.dashboard.geometry('700x500')
            self.user_loggedIn = Label(self.dashboard,text=f'User ID : {user_id}',font=("Calibry",15))
            self.user_loggedIn.place(relx=0.4,rely=0.1)
            self.runner.execute(f'SELECT AccountNo FROM Details WHERE User_ID = \'{user_id}\'')
            text = Label(self.dashboard,text="Account No. "+str(self.runner.fetchall()[0][0]),font=("Calibry",15))
            text.place(relx=0.37,rely=0.17)
            self.credit_btn = Button(self.dashboard,text="Credit Amount",font=("Times New Roman",15),background='orange', command=lambda: self.credit(user_id))
            self.debit_btn = Button(self.dashboard,text="Debit Amount",font=("Times New Roman",15),background='orange', command=lambda: self.debit(user_id))
            self.balance_btn = Button(self.dashboard,text="Check Balance",font=("Times New Roman",15),background='light blue',command=lambda: self.checkBalance(user_id))
            self.transfer_btn = Button(self.dashboard,text="Transfer Amount",font=("Times New Roman",15),background='light green',command=lambda: self.transfer(user_id))
            self.logout_btn = Button(self.dashboard,text="Log Out",font=("Times New Roman",15),background='red',foreground='white',command=lambda: self.dashboard.destroy())
            self.credit_btn.place(relx=0.3,rely=0.3)
            self.debit_btn.place(relx=0.5,rely=0.3)
            self.balance_btn.place(relx=0.3,rely=0.4)
            self.transfer_btn.place(relx=0.5,rely=0.4)
            self.logout_btn.place(relx=0.44,rely=0.5)
            self.dashboard.mainloop()

    def login(self):
        self.login_form = Tk()
        self.text1 = Label(self.login_form,text="User ID",font=("Times New Roman",15))
        self.text1.grid(row=0,sticky="e")
        self.text2 = Label(self.login_form,text="Pin",font=("Times New Roman",15))
        self.text2.grid(row=1,sticky="e")
        self.ID = Entry(self.login_form,font=("Times New Roman",15))
        self.ID.grid(row=0,column=1)
        self.pin = Entry(self.login_form,font=("Times New Roman",15))
        self.pin.grid(row=1,column=1)
        self.login = Button(self.login_form,text="Login",font=("Times New Roman",15),command=self.user_dashboard)
        self.login.grid(row=4,column=1)
        self.login_form.mainloop()
    def design_body(self):
        self.root = Tk()
        self.root.geometry('1000x400')
        self.heading = Label(self.root,text="WELCOME TO OUR ONLINE BANKING SYSTEM",font=("Calibry",30))
        self.heading.pack()
        self.btn1 = Button(self.root,text="Create Account",font=("Times New Roman",20),background='light blue',command=self.createAccount)
        self.btn1.place(relx=0.3,rely=0.7)
        self.btn2 = Button(self.root,text="Login",font=("Times New Roman",20),background='light blue',command=self.login)
        self.btn2.place(relx=0.6,rely=0.7)
        self.root.mainloop()

bank = Bank()