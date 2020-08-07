from future.moves.tkinter import *
import pymysql
from tkinter import messagebox
from datetime import date
import pandas as pd
from openpyxl import *


class BMI:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Mass Index")
        self.root.geometry('495x430+400+100')  # Default size to open into
        self.root.resizable(0, 0)

        # Header
        title = Label(self.root, text="BODY MASS INDEX", height=2, width=60, bg="#273746", fg="white", bd=5,
                      relief=GROOVE, font=("serif 10 bold")).grid(row=0, column=0, columnspan=3, pady=5)

        # Footer
        self.statusVar = StringVar()
        status = Entry(self.root, textvariable=self.statusVar, bd=10, font="arial 10 bold", relief=GROOVE, width=50, disabledforeground='blue',
                       justify=CENTER, state='disabled').grid(row=14, column=0, columnspan=3, pady=20)

        # **************** All Variables **************** #
        self.idVar = StringVar()
        self.nameVar = StringVar()
        self.ageVar = StringVar()
        self.weightVar = StringVar()
        self.heightVar = StringVar()
        self.genderVar = StringVar()
        self.bmiVar = StringVar()
        self.dateVar = StringVar()

        # **************** Patient Details **************** #
        # Patient ID
        id_lbl = Label(self.root, text="Patient ID").grid(row=1, column=0)
        id_txt = Entry(self.root, text=self.idVar, width=30).grid(row=1, column=1)

        # Patient Name
        name_lbl = Label(self.root, text="Name").grid(row=2, column=0)
        name_txt = Entry(self.root, text=self.nameVar, width=30).grid(row=2, column=1)

        # Patient Age
        age_lbl = Label(self.root, text="Age(yrs)").grid(row=3, column=0)
        age_txt = Entry(self.root, text=self.ageVar, width=30).grid(row=3, column=1)

        # Patient Weight
        weight_lbl = Label(self.root, text="Weight(kg)").grid(row=4, column=0)
        weight_txt = Entry(self.root, text=self.weightVar, width=30).grid(row=4, column=1)

        # Patient Height
        height_lbl = Label(self.root, text="Height(ft)").grid(row=5, column=0)
        height_txt = Entry(self.root, text=self.heightVar, width=30).grid(row=5, column=1)

        # BMI Display
        bmi_lbl = Label(self.root, text="BMI").grid(row=7, column=0)
        bmi_display = Entry(self.root, textvariable=self.bmiVar, width=26, font="arial 10 bold", bd=4, relief=SUNKEN,
                            disabledbackground="black", disabledforeground="cyan", state='disabled').grid(row=7, column=1)

        # Gender Radio Button
        self.select = StringVar()
        self.select.set(1)
        gender_lbl = Label(self.root, text="Gender").grid(row=3, column=2, padx=30, sticky="w")
        gender_btn = Radiobutton(self.root, text="Male", variable=self.select, value=1, command=self.gender).grid(row=4,
                                                                                                                  column=2,
                                                                                                                  padx=30,
                                                                                                                  sticky="w")
        gender_btn = Radiobutton(self.root, text="Female", variable=self.select, value=2, command=self.gender).grid(
            row=5, column=2, padx=30, sticky="w")

        # Date
        today = date.today()
        mydate = today.strftime("%d - %m - %y")
        mydate_lbl = Label(self.root, text=mydate, width=20, bd=5, relief=GROOVE)
        mydate_lbl.grid(row=1, column=2)
        self.dateVar.set(mydate)

        # Blank Line
        blank_line = Label(self.root, text=" ").grid(row=8, column=0)

        # **************** Buttons **************** #
        calculate_button = Button(self.root, text="Calculate", command=self.calculate, width=15, height=1).grid(row=9,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                sticky="e")
        show_button = Button(self.root, text="Show", command=self.show, width=15, height=1).grid(row=10, column=1,
                                                                                                 padx=5, sticky="e")
        clear_button = Button(self.root, text="Clear", command=self.clear, width=15, height=1).grid(row=11, column=1,
                                                                                                    padx=5, sticky="e")
        exit_button = Button(self.root, text="Exit", command=self.exit, width=15, height=1).grid(row=12, column=1,
                                                                                                 padx=5, sticky="e")

        save_button = Button(self.root, text="Save", command=self.save, width=15, height=1).grid(row=9, column=2,
                                                                                                 padx=5, sticky="w")
        update_button = Button(self.root, text="Update", command=self.update, width=15, height=1).grid(row=10, column=2,
                                                                                                       padx=5,
                                                                                                       sticky="w")
        delete_button = Button(self.root, text="Delete", command=self.delete, width=15, height=1).grid(row=11, column=2,
                                                                                                       padx=5,
                                                                                                       sticky="w")
        report_button = Button(self.root, text="Report", command=self.report, width=15, height=1).grid(row=12, column=2,
                                                                                                       padx=5,
                                                                                                       sticky="w")
        self.genderVar.set("Male")

    def gender(self):
        selected_gender = int(str(self.select.get()))
        if selected_gender == 1:
            self.genderVar.set("Male")
        elif selected_gender == 2:
            self.genderVar.set("Female")

    def category(self, bmi):
        result = ""
        if bmi < 18.55:
            result = "You're Under Weight !"
        elif bmi >= 18.55 and bmi < 24.99:
            result = "Normal Weight !"
        elif bmi >= 25.0 and bmi < 29.99:
            result = "You're Over Weight (Warning) !"
        elif bmi >= 30.0 and bmi < 34.99:
            result = "You're at Obesity Level 1 (Dangerous) !"
        elif bmi >= 35.0 and bmi < 39.99:
            result = "You're at Obesity Level 2 (Consult Doctor) !"
        elif bmi >= 40.0:
            result = "You're at Obesity Level 3 (Life Threatening) !"
        return result

    def calculate(self):
        weight = float(self.weightVar.get())
        height_mtr = 0.3048 * float(self.heightVar.get())
        bmi = round((weight / (height_mtr * height_mtr)), 2)
        self.bmiVar.set(bmi)
        self.statusVar.set("" + self.category(bmi))

    def exit(self):
        ask = messagebox.askyesno("Exit", "Are you sure?")
        if ask > 0:
            self.root.destroy()

    def clear(self):
        ask = messagebox.askyesno("Clear!", "Are you sure?")
        if ask > 0:
            self.statusVar.set("")
            self.idVar.set("")
            self.nameVar.set("")
            self.ageVar.set("")
            self.weightVar.set("")
            self.heightVar.set("")
            self.bmiVar.set("")
            self.select.set(1)
        else:
            return

    def save(self):
        if self.idVar.get() == "" or self.nameVar.get() == "" or self.ageVar.get() == "" or self.weightVar.get() == "" or self.heightVar.get() == "":
            messagebox.showerror("Error !", "All fields are required !")
        else:
            con = pymysql.connect(host="localhost", user="root", password="uokcsi2012", database="bmi")
            cur = con.cursor()
            cur.execute("insert into bmi_record values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (self.dateVar.get(),
                         self.idVar.get(),
                         self.nameVar.get(),
                         self.ageVar.get(),
                         self.weightVar.get(),
                         self.heightVar.get(),
                         self.genderVar.get(),
                         self.bmiVar.get(),
                         self.statusVar.get()
                         ))
            con.commit()
            con.close()
            messagebox.showinfo("Success!", "Record has been inserted !")

    def show(self):
        con = pymysql.connect(host="localhost", user="root", password="uokcsi2012", database="bmi")
        cur = con.cursor()
        cur.execute("select * from bmi_record where patient_id=%s", self.idVar.get())
        records = cur.fetchall()
        for row in records:
            self.dateVar.set(row[0]),
            self.idVar.set(row[1]),
            self.nameVar.set(row[2]),
            self.ageVar.set(row[3]),
            self.weightVar.set(row[4]),
            self.heightVar.set(row[5]),
            if (str(row[6]) == "Female"): self.select.set(2),
            self.bmiVar.set(row[7]),
            self.statusVar.set(row[8])

    def update(self):
        ask = messagebox.askyesno("Update!", "Are you sure?")
        if ask > 0:
            con = pymysql.connect(host="localhost", user="root", password="uokcsi2012", database="bmi")
            cur = con.cursor()
            cur.execute(
                "update bmi_record set checkup_date=%s, patient_name=%s, patient_age=%s, patient_weight=%s, patient_height=%s, patient_gender=%s, patient_bmi=%s, patient_status=%s where patient_id=%s",
                (self.dateVar.get(),
                 self.idVar.get(),
                 self.nameVar.get(),
                 self.ageVar.get(),
                 self.weightVar.get(),
                 self.heightVar.get(),
                 self.genderVar.get(),
                 self.bmiVar.get(),
                 self.statusVar.get()
                 ))
            con.commit()
            self.clear()
            con.close()
            messagebox.showinfo("Success!", "Record has been updated !")
        else:
            return

    def delete(self):
        ask = messagebox.askyesno("Delete!", "Are you sure?")
        if ask > 0:
            con = pymysql.connect(host="localhost", user="root", password="uokcsi2012", database="bmi")
            cur = con.cursor()
            cur.execute("delete from bmi_record where patient_id=%s", self.idVar.get())
            con.commit()
            con.close()
            self.clear()
            messagebox.showinfo("Success!", "Record has been deleted !")
        else:
            return

    def report(self):
        ask = messagebox.askyesno("Report!", "Are you sure?")
        if ask > 0:
            dict = {'checkup_date': {}, 'patient_id': {}, 'patient_name': {}, 'patient_age': {}, 'patient_weight': {},
                    'patient_height': {}, 'patient_gender': {}, 'patient_bmi': {}, 'patient_status': {}}
            df = pd.DataFrame(dict)
            con = pymysql.connect(host="localhost", user="root", password="uokcsi2012", database="bmi")
            cur = con.cursor()
            cur.execute("select * from bmi_record")
            records = cur.fetchall()
            for i in range(cur.rowcount):
                df.loc[i] = records[i]
                i += 1
            df.to_excel("E:/dell/Python/Temp/bmi/BMI_REPORT.xlsx")
            con.close()
            messagebox.showinfo("Success", "BMI_REPORT.xlsx is generated !")
        else:
            return


root = Tk()
obj = BMI(root)
root.mainloop()
