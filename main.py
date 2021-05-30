import os
import sqlite3

connection = sqlite3.connect("FreshFields.db")
cursor = connection.cursor()

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

global welcome, mainpage, clogin, flogin, wlogin, farmer_dashboard, customer_register,article,cust_dashboard

def statistics():
    welcome.destroy()
    global stats
    stats = Tk()
    stats.geometry("1199x700+150+100")
    stats.title("Statistics Window")
    stats.resizable(False, False)
    bg = ImageTk.PhotoImage(file=r"photos/background.jpg")
    bg_image = Label(stats, image=bg).place(x=0, y=0, relwidth=1, relheight=1)


    def demand_products():
        df = pd.read_sql_query(
            "SELECT produce_name,COUNT(DISTINCT customer_email) AS 'Number of Unique Consumers' FROM customer_history GROUP BY produce_name",
            connection)
        df.set_index("produce_name", inplace=True)
        root = Tk()
        root.geometry("1000x900")
        figure1 = plt.Figure(figsize=(10, 7), dpi=120)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
        df.plot(kind='bar', legend=True, ax=ax1, fontsize=7)
        ax1.set_title('Demand of Products (x-> product name, y->No of consumers)')
        root.mainloop()


    def supply_products():
        df1 = pd.read_sql_query(
            "SELECT produce_name,COUNT(DISTINCT farmer_email) AS 'Number of Unique Farmers' FROM farmer_product GROUP BY produce_name",
            connection)
        df1.set_index("produce_name", inplace=True)
        root = Tk()
        root.geometry("1000x900")
        figure1 = plt.Figure(figsize=(10, 7), dpi=120)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
        df1.plot(kind='bar', legend=True, ax=ax1, fontsize=7)
        plt.xticks(fontsize=100)
        ax1.set_title('Supply of Products (x-> produce name, y->No of farmers)')
        root.mainloop()

    def VvsP_Purchased():
        root = Tk()
        root.geometry("200x200")

        cursor.execute('SELECT DISTINCT produce_name FROM customer_history')
        categorylist = cursor.fetchall()

        def prodpicked(e):
            df2 = pd.read_sql_query(
                'SELECT variety_name,SUM(quantity) AS " " FROM customer_history WHERE produce_name=? GROUP BY variety_name ',
                connection, params=(produce_menu.get(),))
            df2.set_index("variety_name", inplace=True)
            root = Tk()
            root.geometry("700x600")
            figure1 = plt.Figure(figsize=(9, 10), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, root)
            bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
            df2.plot(kind='pie', legend=False, subplots=True, ax=ax1, autopct='%1.1f%%', startangle=15, shadow=True)
            ax1.set_title('Variety of Crop Sold')

        labl = Label(root, text="Select Crop", font=("Berlin Sans FB Demi", 15, "bold")).pack()
        produce_menu = ttk.Combobox(root, value=categorylist)
        produce_menu.pack()

        produce_menu.bind("<<ComboboxSelected>>", prodpicked)
        root.mainloop()

    # input from farmer -> all variety of banana
    # then buy the banans from a customer

    def VvsP_Inventory():
        root = Tk()
        root.geometry("200x200")

        def prodpicked(e):
            df3 = pd.read_sql_query(
                'SELECT variety_name,SUM(quantity) AS " " FROM farmer_product WHERE produce_name=? GROUP BY variety_name ',
                connection, params=(produce_menu.get(),))
            print(df3)
            df3.set_index("variety_name", inplace=True)
            root = Tk()
            root.geometry("700x600")
            figure1 = plt.Figure(figsize=(9, 10), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, root)
            bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
            df3.plot(kind='pie', legend=False, subplots=True, ax=ax1, autopct='%1.1f%%', startangle=15, shadow=True)
            ax1.set_title('Variety of Crops Available')

        cursor.execute('SELECT DISTINCT produce_name FROM farmer_product')
        categorylist = cursor.fetchall()
        labell = Label(root, text="Select Crop", font=("Berlin Sans FB Demi", 15, "bold")).pack()
        produce_menu = ttk.Combobox(root, value=categorylist)
        produce_menu.pack()
        produce_menu.bind("<<ComboboxSelected>>", prodpicked)
        root.mainloop()


    def districtVSfarmer():
        df3 = pd.read_sql_query(
            'SELECT district_name,COUNT(farmer_email) AS "Number of farmers" FROM farmer INNER JOIN district ON farmer.district_id=district.district_id GROUP BY farmer.district_id ORDER BY "Number of farmers" ',
            connection)
        df3.set_index("district_name", inplace=True)
        root = Tk()
        root.geometry("1000x700")
        figure1 = plt.Figure(figsize=(10, 10), dpi=120)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
        df3.tail(10).plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('District Wise Distribution of Farmers')
        root.mainloop()


    def districtVSworker():
        df3 = pd.read_sql_query(
            'SELECT district_name,COUNT(worker_email) AS "Number of workers" FROM worker INNER JOIN district ON worker.district_id=district.district_id GROUP BY worker.district_id ORDER BY "Number of workers" ',
            connection)
        df3.set_index("district_name", inplace=True)
        root = Tk()
        root.geometry("1000x700")
        figure1 = plt.Figure(figsize=(10, 10), dpi=120)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
        df3.tail(10).plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('District Wise Distribution of Workers')


    def CustomerTypeDistribution():
        df4 = pd.read_sql_query(
            'SELECT customer_type, COUNT(customer_type) as " " FROM customer GROUP BY customer_type ', connection)
        df4.set_index("customer_type", inplace=True)
        root = Tk()
        root.geometry("1000x700")
        my_colors = ['lightblue', 'lightsteelblue', 'silver']
        my_explode = (0, 0.1, 0)
        figure1 = plt.Figure(figsize=(9, 10), dpi=120)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
        df4.plot(kind='pie', legend=False, subplots=True, ax=ax1, autopct='%1.1f%%', startangle=15, shadow=True,
                 colors=my_colors, explode=my_explode)
        ax1.set_title('Customer Type Distribution')
        root.mainloop()

    def back():
        stats.destroy()
        welcome_page()


    titlec = Label(stats, text="Dashboard Statistics", pady=10, bg="black",
                   font=("Berlin Sans FB Demi", 30, "bold"),
                   fg="white").pack()
    photo = ImageTk.PhotoImage(file=r"photos/stats.png")
    back1 = Button(stats, cursor="hand2", command=demand_products, text="Demand of Products", fg="black", image=photo,
                  compound=TOP, bd=5,
                  bg="white", font=("times new roman", 15)).place(x=70, y=130, width=220, height=200)
    back2 = Button(stats, cursor="hand2", command=supply_products, text="Supply of Products", fg="black", image=photo, bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=350, y=130, width=220, height=200)
    back3 = Button(stats, cursor="hand2", command=VvsP_Purchased, text="Variety of Crops Sold", fg="black", image=photo,
                  bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=630, y=130, width=220, height=200)
    back4 = Button(stats, cursor="hand2", command=VvsP_Inventory, text="Variety of Crops Available", fg="black", image=photo,
                  bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=910, y=130, width=220, height=200)
    back5 = Button(stats, cursor="hand2", command=districtVSfarmer, text="District Vs Farmers", fg="black", image=photo,
                  bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=200, y=400, width=220, height=200)
    back6 = Button(stats, cursor="hand2", command=districtVSworker, text="District Vs Workers", fg="black", image=photo,
                  bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=500, y=400, width=220, height=200)
    back7 = Button(stats, cursor="hand2", command=CustomerTypeDistribution, text="Customer Type Distribution", fg="black",
                  image=photo, bd=5,
                  compound=TOP,
                  bg="white", font=("times new roman", 15)).place(x=800, y=400, width=220, height=200)
    back8 = Button(stats, cursor="hand2", command=back, text="Back",
                   fg="black", bd=5,
                   compound=TOP,
                   bg="white", font=("times new roman", 15)).place(x=0, y=650, width=100, height=50)

    stats.mainloop()

def welcome_page():
    global welcome
    welcome = Tk()
    welcome.geometry("1199x700+150+100")
    welcome.title("Welcome Page")
    welcome.resizable(False, False)

    # === BB Image ======
    bg = ImageTk.PhotoImage(file=r"photos/FF1.png")
    bg_image = Label(welcome, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    GetStarted_Button = Button(welcome, cursor="hand2", text="Get Started", bg="black", bd=0, fg="white",
                               command=lambda: main_page(), pady=5, padx=5, relief=RAISED,
                               font=("times new roman", 25)).place(x=400, y=260,height=50,width=180)
    stats = Button(welcome, cursor="hand2", text="Statistics", bg="black", bd=0, fg="white",
                               command=lambda: statistics(), pady=5, padx=5, relief=RAISED,
                               font=("times new roman", 25)).place(x=650, y=260,height=50,width=180)

    welcome.mainloop()


def main_page():
    welcome.destroy()
    global mainpage
    mainpage = Tk()
    mainpage.geometry("1199x600+150+100")
    mainpage.title("Main Page")
    mainpage.resizable(False, False)
    # === BB Image ======
    bg = ImageTk.PhotoImage(file=r"photos/background.jpg")
    bg_image = Label(mainpage, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # ====Customer Frame======
    Frame_customer = Frame(mainpage, bg="white")
    Frame_customer.place(x=200, y=200, height=200, width=200)
    titlec = Label(Frame_customer, text="Customer", font=("Berlin Sans FB Demi", 20, "bold"), bg="white",
                   fg="black", ).place(x=40, y=10)
    Loginc_Button = Button(Frame_customer, text="Login", cursor="hand2", command=lambda: customer_login(mainpage),
                           bg="gray", bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=25,
                                                                                                    y=60,
                                                                                                    width=150,
                                                                                                    height=40)
    Registerc_Button = Button(Frame_customer, text="Registration", fg="white", cursor="hand2", bd=0,
                              command=lambda: customer_register(mainpage),
                              bg="gray", font=("times new roman", 15, "bold")).place(x=10, y=120, width=180,
                                                                                     height=40)

    # ====Farmer Frame======
    Frame_Farmer = Frame(mainpage, bg="white")
    Frame_Farmer.place(x=500, y=200, height=200, width=200)
    titlef = Label(Frame_Farmer, text="Farmer", font=("Berlin Sans FB Demi", 20, "bold"), bg="white",

                   fg="black", ).place(x=55, y=10)
    Loginf_Button = Button(Frame_Farmer, text="Login", cursor="hand2", bg="gray",
                           command=lambda: farmer_login(mainpage),
                           bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=25, y=60, width=150,
                                                                                         height=40)
    Registerf_Button = Button(Frame_Farmer, text="Registration", fg="white", cursor="hand2", bd=0, bg="gray",
                              command=lambda: farmer_register(mainpage),
                              font=("times new roman", 15, "bold")).place(x=10, y=120, width=180, height=40)

    # ====Worker Frame======
    Frame_Worker = Frame(mainpage, bg="white")
    Frame_Worker.place(x=800, y=200, height=200, width=200)
    titlew = Label(Frame_Worker, text="Worker", font=("Berlin Sans FB Demi", 20, "bold"), bg="white",
                   fg="black", ).place(x=55, y=10)
    Loginw_Button = Button(Frame_Worker, text="Login", cursor="hand2", bg="gray",
                           command=lambda: worker_login(mainpage),
                           bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=25, y=60, width=150,
                                                                                         height=40)
    Registerw_Button = Button(Frame_Worker, text="Registration", fg="white", cursor="hand2", bd=0, bg="gray",
                              command=lambda: worker_register(mainpage),
                              font=("times new roman", 15, "bold")).place(x=10, y=120, width=180, height=40)
    mainpage.mainloop()

def article():

    article = Tk()
    article.title("Articles")
    article.geometry("1350x700+0+0")
    article.configure(bg="white")

    def selected(self):
        global content
        global publish_date
        title_selected = my_combo.get()
        cursor.execute("SELECT article_description, publish_date FROM article WHERE title='{}'".format(title_selected))
        for j in cursor.fetchall():
            content = j[0]
            publish_date = j[1]

        text_area.configure(state='normal')
        text_area.delete('1.0', END)
        text_area.insert(INSERT, content)
        text_area.configure(state='disabled')
        date_label.config(text="Published on: {}".format(publish_date))

    def return_title_list():
        temp = ["Select Article"]
        cursor.execute("SELECT title from article")
        for i in cursor.fetchall():
            for title in i:
                temp.append(title)
        return temp

    titles = return_title_list()

    my_combo = ttk.Combobox(article, value=titles, width=50,
                            font=("times new roman", 18, "bold"), justify="center",
                            state="readonly")
    my_combo.current(0)
    my_combo.bind("<<ComboboxSelected>>", selected)
    my_combo.pack(pady=20)
    from tkinter import scrolledtext
    text_area = scrolledtext.ScrolledText(article, font=("times new roman", 15),
                                          wrap=WORD,
                                          width=100,
                                          height=20,
                                          bg="white",
                                          padx=10,
                                          pady=10
                                          )
    text_area.pack(pady=20)
    date_label = Label(article, justify="right", bg="lightgray",
                       font=("times new roman", 16, "bold") )
    date_label.place(x=900, y=560)
    article.mainloop()
# a = article()





def customer_login(mainpage):
    mainpage.destroy()
    global clogin
    clogin = Tk()
    clogin.title("Login System")
    clogin.geometry("1199x600+100+50")
    clogin.resizable(False, False)
    # === BB Image ======
    bg = ImageTk.PhotoImage(file=r"photos/background.jpg")
    bg_image = Label(clogin, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # ====Login Frame======
    Frame_login = Frame(clogin, bg="white")
    Frame_login.place(x=150, y=150, height=340, width=500)

    title = Label(Frame_login, text="Login Here", font=("Berlin Sans FB Demi", 35, "bold"), fg="#d77337",
                  bg="white").place(x=120, y=30)
    desc = Label(Frame_login, text="Customer Login Area", font=("Goudy old style", 15, "bold"), fg="#d25d17",
                 bg="white").place(x=145, y=100)

    lbl_username = Label(Frame_login, text="Email Id", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=160)
    user_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    user_entry.place(x=150, y=160, width=250, height=35)

    lbl_password = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=220)
    pass_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show='*')
    pass_entry.place(x=150, y=220, width=250, height=35)

    # forget_Button = Button(Frame_login, cursor="hand2", text="Forget Password?", bg="white", bd=0, fg="#d77337",
    #                        font=("times new roman", 15)).place(x=40, y=280)
    login_Button = Button(clogin, cursor="hand2",
                          command=lambda: login_verify_customer(user_entry.get(), pass_entry.get()), text="Login",
                          fg="white",
                          bg="#d77337", font=("times new roman", 20)).place(x=300, y=470, width=180, height=40)
    clogin.mainloop()


def customer_register(mainpage):
    mainpage.destroy()
    global customer_register
    customer_register = Tk()
    customer_register.title("Customer Registration")
    customer_register.geometry("1350x700+0+0")

    # Function to execute when register button is pressed
    def register():

        # Function to empty the field of its contents
        def delete_data(entry_field):
            entry_field.delete(0, "end")

        # Function to restrict certain fields to integer
        def is_number(entry_field):
            try:
                int(entry_field.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
                delete_data(entry_field)
        def is_email(entry_field):
            try:
                if "@" and "." not in entry_field:
                    raise Exception
            except:
                messagebox.showerror("Invalid email", "Enter Valid Email")
                delete_data(entry_field)


        is_number(entry_contact)
        is_number(entry_pincode)
        is_email(entry_email.get())



        cursor.execute('SELECT city_id,district_id from city WHERE city_name=?', (city_menu.get(),))
        for i in cursor.fetchall():
            city = i[0]
            district = i[1]
            print(city)
            print(district)

        cursor.execute("INSERT OR IGNORE INTO customer VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (entry_name.get(),
                        int(entry_contact.get()),
                        entry_email.get(),
                        entry_password.get(),
                        int(district),
                        int(city),
                        int(entry_pincode.get()),
                        cmb_cust_type.get(),
                        entry_address.get("1.0", END)
                        )
                       )

        delete_data(entry_name)
        delete_data(entry_contact)
        delete_data(entry_email)
        delete_data(entry_password)
        # delete_data(district_name_cmb)
        # delete_data(city_name_cmb)
        delete_data(entry_pincode)
        delete_data(cmb_cust_type)
        entry_address.delete("1.0", "end")

        connection.commit()

    # Bg
    bg = ImageTk.PhotoImage(file=r"photos/wood_mainpage.jpg")
    bg_image = Label(customer_register, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # Left Image
    left = ImageTk.PhotoImage(file=r"photos/food-sunset-love-field.jpg")
    left_img = Label(customer_register, image=left).place(x=80, y=100, width=400, height=500)

    # The main background frame
    main_frame = Frame(customer_register, bg="white")
    main_frame.place(x=480, y=100, width=700, height=500)

    # The title of the Page
    title = Label(main_frame,
                  text="Customer Register",
                  font=("times new roman", 20, "bold"),
                  bg="white",
                  fg="black")
    title.place(x=50, y=30)

    # Column 1 Row 1
    cust_name = Label(main_frame,
                      text="Customer Name",
                      font=("times new roman", 15, "bold"),
                      bg="white",
                      fg="gray")
    cust_name.place(x=50, y=100)

    entry_name = Entry(main_frame,
                       font=("times new roman", 15),
                       borderwidth=2,
                       bg="lightgray")
    entry_name.place(x=50, y=130, width=250)

    # Column 2 Row 1
    contact_no = Label(main_frame,
                       text="Contact Number",
                       font=("times new roman", 15, "bold"),
                       bg="white",
                       fg="gray")
    contact_no.place(x=370, y=100)

    entry_contact = Entry(main_frame,
                          font=("times new roman", 15),
                          borderwidth=2,
                          bg="lightgray")
    entry_contact.place(x=370, y=130, width=250)

    # Column 1 Row 2
    email = Label(main_frame,
                  text="Email Id",
                  font=("times new roman", 15, "bold"),
                  bg="white",
                  fg="gray")
    email.place(x=50, y=160)

    entry_email = Entry(main_frame,
                        font=("times new roman", 15),
                        borderwidth=2,
                        bg="lightgray")
    entry_email.place(x=50, y=190, width=250)

    # Column 2 Row 2
    password = Label(main_frame,
                     text="Password",
                     font=("times new roman", 15, "bold"),
                     bg="white",
                     fg="gray")
    password.place(x=370, y=160)

    entry_password = Entry(main_frame,
                           font=("times new roman", 15),
                           borderwidth=2,
                           bg="lightgray",
                           show='*')
    entry_password.place(x=370, y=190, width=250)

    def customer_district(e):
        x = district_menu.get()
        cursor.execute(
            'SELECT city_name FROM city INNER JOIN district ON city.district_id=district.district_id WHERE district_name=?',
            (x,))
        citylist = cursor.fetchall()
        city_menu.config(value=citylist)

    cursor.execute('SELECT district_name FROM district')
    distlist = cursor.fetchall()

    district_id = Label(main_frame, text="District", font=("times new roman", 15, "bold"), bg="white",
                        fg="gray").place(x=50, y=220)
    district_menu = ttk.Combobox(main_frame, value=distlist, state="readonly")
    district_menu.place(x=50, y=250, width=250)

    city_id = Label(main_frame, text="City Id", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    city_id.place(x=370, y=220)
    city_menu = ttk.Combobox(main_frame, state="readonly")
    city_menu.place(x=370, y=250, width=250)

    district_menu.bind("<<ComboboxSelected>>", customer_district)

    # Column 1 Row 4
    pincode = Label(main_frame, text="Pincode", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    pincode.place(x=50, y=280)
    entry_pincode = Entry(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_pincode.place(x=50, y=310, width=250)

    # Column 2 Row 4
    cust_type = Label(main_frame, text="Customer Type", font=("times new roman", 15, "bold"), bg="white",
                      fg="gray")
    cust_type.place(x=370, y=280)

    cmb_cust_type = ttk.Combobox(main_frame, state="readonly", font=("times new roman", 13), justify="center")
    cmb_cust_type["values"] = ("Select", "Wholeseller", "Consumer", "Retailer")
    cmb_cust_type.place(x=370, y=310, width=250)
    cmb_cust_type.current(0)

    # Column 1 Row 5
    address = Label(main_frame, text="Address", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    address.place(x=50, y=340)
    entry_address = Text(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_address.place(x=50, y=370, width=250, height=80)

    # Submit Button
    register_butt = Button(main_frame, text="Register", bd=2, font=("times new roman", 15), cursor="hand2",
                           command=register, justify="center", bg="white", borderwidth=3)
    register_butt.place(x=430, y=390, width=120)

    # Login Button
    login_butt = Button(customer_register, text="Login", bd=2, font=("times new roman", 15), cursor="hand2",
                        command=lambda: customer_login(customer_register),
                        justify="center", bg="white", borderwidth=3)
    login_butt.place(x=220, y=500, width=120)

    customer_register.mainloop()


def farmer_register(mainpage):
    mainpage.destroy()
    farmer_register = Tk()
    farmer_register.title("Farmer Registration")
    farmer_register.geometry("1350x700+0+0")

    # Function to execute when register button is pressed
    def register():

        # Function to empty the field of its contents
        def delete_data(entry_field):
            entry_field.delete(0, "end")

        # Function to restrict certain fields to integer
        def is_number(entry_field):
            try:
                int(entry_field.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
                delete_data(entry_field)
        def is_email(entry_field):
            try:
                if "@" and "." not in entry_field:
                    raise Exception
            except:
                messagebox.showerror("Invalid email", "Enter Valid Email")
                delete_data(entry_field)

        is_email(entry_email.get())

        cursor.execute('SELECT city_id,district_id from city WHERE city_name=?', (city_menu.get(),))
        for i in cursor.fetchall():
            city = i[0]
            district = i[1]
            print(city)
            print(district)

        is_number(entry_contact)

        cursor.execute("INSERT OR IGNORE INTO farmer VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (entry_name.get(),
                        entry_password.get(),
                        entry_email.get(),
                        int(entry_contact.get()),
                        int(district),
                        int(city),
                        entry_ifsc_code.get(),
                        entry_acc_no.get(),
                        entry_address.get("1.0", END)
                        )
                       )

        delete_data(entry_name)
        delete_data(entry_contact)
        delete_data(entry_email)
        delete_data(entry_password)
        delete_data(entry_ifsc_code)
        delete_data(entry_acc_no)
        entry_address.delete("1.0", "end")

        connection.commit()

    # Bg
    bg = ImageTk.PhotoImage(file=r"photos/wood_mainpage.jpg")
    bg_image = Label(farmer_register, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # Left Image
    left = ImageTk.PhotoImage(file=r"photos/food-sunset-love-field.jpg")
    left_img = Label(farmer_register, image=left).place(x=80, y=100, width=400, height=500)

    # The main background frame
    main_frame = Frame(farmer_register, bg="white")
    main_frame.place(x=480, y=100, width=700, height=500)

    # The title of the Page
    title = Label(main_frame,
                  text="Farmer Register",
                  font=("times new roman", 20, "bold"),
                  bg="white",
                  fg="black")
    title.place(x=50, y=30)

    # Column 1 Row 1
    farmer_name = Label(main_frame,
                        text="Farmer Name",
                        font=("times new roman", 15, "bold"),
                        bg="white",
                        fg="gray")
    farmer_name.place(x=50, y=100)

    entry_name = Entry(main_frame,
                       font=("times new roman", 15),
                       borderwidth=2,
                       bg="lightgray")
    entry_name.place(x=50, y=130, width=250)

    # Column 2 Row 1
    contact_no = Label(main_frame,
                       text="Contact Number",
                       font=("times new roman", 15, "bold"),
                       bg="white",
                       fg="gray")
    contact_no.place(x=370, y=100)

    entry_contact = Entry(main_frame,
                          font=("times new roman", 15),
                          borderwidth=2,
                          bg="lightgray")
    entry_contact.place(x=370, y=130, width=250)

    # Column 1 Row 2
    email = Label(main_frame,
                  text="Email Id",
                  font=("times new roman", 15, "bold"),
                  bg="white",
                  fg="gray")
    email.place(x=50, y=160)

    entry_email = Entry(main_frame,
                        font=("times new roman", 15),
                        borderwidth=2,
                        bg="lightgray")
    entry_email.place(x=50, y=190, width=250)

    # Column 2 Row 2
    password = Label(main_frame,
                     text="Password",
                     font=("times new roman", 15, "bold"),
                     bg="white",
                     fg="gray")
    password.place(x=370, y=160)

    entry_password = Entry(main_frame,
                           font=("times new roman", 15),
                           borderwidth=2,
                           bg="lightgray",
                           show='*')
    entry_password.place(x=370, y=190, width=250)

    # Column 1 Row 3
    def customer_district(e):
        x = district_menu.get()
        cursor.execute(
            'SELECT city_name FROM city INNER JOIN district ON city.district_id=district.district_id WHERE district_name=?',
            (x,))
        citylist = cursor.fetchall()
        city_menu.config(value=citylist)

    cursor.execute('SELECT district_name FROM district')
    distlist = cursor.fetchall()

    district_id = Label(main_frame, text="District", font=("times new roman", 15, "bold"), bg="white",
                        fg="gray").place(x=50, y=220)
    district_menu = ttk.Combobox(main_frame, state="readonly", value=distlist)
    district_menu.place(x=50, y=250, width=250)

    city_id = Label(main_frame, text="City Id", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    city_id.place(x=370, y=220)
    city_menu = ttk.Combobox(main_frame, state="readonly")
    city_menu.place(x=370, y=250, width=250)

    district_menu.bind("<<ComboboxSelected>>", customer_district)

    # Column 1 Row 4
    ifsc_code = Label(main_frame, text="IFSC Code", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    ifsc_code.place(x=50, y=280)
    entry_ifsc_code = Entry(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_ifsc_code.place(x=50, y=310, width=250)

    # Column 2 Row 4
    acc_no = Label(main_frame, text="Account Number", font=("times new roman", 15, "bold"), bg="white",
                   fg="gray")
    acc_no.place(x=370, y=280)
    entry_acc_no = Entry(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_acc_no.place(x=370, y=310, width=250)

    # Column 1 Row 5
    address = Label(main_frame, text="Address", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    address.place(x=50, y=340)
    entry_address = Text(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_address.place(x=50, y=370, width=250, height=80)

    # Submit Button
    register_butt = Button(main_frame, text="Register", bd=2, font=("times new roman", 15), cursor="hand2",
                           command=register, justify="center", bg="white", borderwidth=3)
    register_butt.place(x=430, y=390, width=120)

    # Login Button
    login_butt = Button(farmer_register, text="Login", bd=2, font=("times new roman", 15), cursor="hand2",
                        command=lambda: farmer_login(farmer_register),
                        justify="center", bg="white", borderwidth=3)
    login_butt.place(x=220, y=500, width=120)

    farmer_register.mainloop()


def farmer_login(mainpage):
    mainpage.destroy()
    global flogin
    flogin = Tk()
    flogin.title("Login System")
    flogin.geometry("1199x600+100+50")
    flogin.resizable(False, False)
    # === BB Image ======
    bg = ImageTk.PhotoImage(file=r"photos/background.jpg")
    bg_image = Label(flogin, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # ====Login Frame======
    Frame_login = Frame(flogin, bg="white")
    Frame_login.place(x=150, y=150, height=340, width=500)

    title = Label(Frame_login, text="Login Here", font=("Berlin Sans FB Demi", 35, "bold"), fg="#d77337",
                  bg="white").place(x=120, y=30)
    desc = Label(Frame_login, text="Farmer Login Area", font=("Goudy old style", 15, "bold"), fg="#d25d17",
                 bg="white").place(x=145, y=100)

    lbl_username = Label(Frame_login, text="Email Id", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=160)
    user_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    user_entry.place(x=150, y=160, width=250, height=35)

    lbl_password = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=220)
    pass_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show='*')
    pass_entry.place(x=150, y=220, width=250, height=35)

    # forget_Button = Button(Frame_login, cursor="hand2", text="Forget Password?", bg="white", bd=0, fg="#d77337",
    #                        font=("times new roman", 15)).place(x=40, y=280)
    login_Button = Button(flogin, cursor="hand2",
                          command=lambda: login_verify_farmer(user_entry.get(), pass_entry.get()), text="Login",
                          fg="white",
                          bg="#d77337", font=("times new roman", 20)).place(x=300, y=470, width=180, height=40)
    flogin.mainloop()


def worker_register(mainpage):
    mainpage.destroy()
    worker_register = Tk()
    var = IntVar()
    worker_register.title("Worker Registration")
    worker_register.geometry("1350x700+0+0")

    # Function to execute when register button is pressed
    def register():
        global district_id
        global city_id

        # Function to empty the field of its contents
        def delete_data(entry_field):
            entry_field.delete(0, "end")

        # Function to restrict certain fields to integer
        def is_number(entry_field):
            try:
                int(entry_field.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
                delete_data(entry_field)
        def is_email(entry_field):
            try:
                if "@" and "." not in entry_field:
                    raise Exception
            except:
                messagebox.showerror("Invalid email", "Enter Valid Email")
                delete_data(entry_field)

        is_email(entry_email.get())

        is_number(entry_contact)
        is_number(entry_exp_sal)
        cursor.execute('SELECT city_id,district_id from city WHERE city_name=?', (city_menu.get(),))
        for i in cursor.fetchall():
            city = i[0]
            district = i[1]

        cursor.execute("INSERT OR IGNORE INTO worker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (entry_name.get(),
                        int(entry_contact.get()),
                        entry_email.get(),
                        entry_password.get(),
                        int(district),
                        int(city),
                        int(entry_exp_sal.get()),
                        var.get(),  # status
                        entry_profile.get(),
                        entry_address.get("1.0", END),
                        " ",
                        )
                       )

        delete_data(entry_name)
        delete_data(entry_contact)
        delete_data(entry_email)
        delete_data(entry_password)
        delete_data(entry_exp_sal)
        delete_data(entry_profile)
        entry_address.delete("1.0", "end")

        connection.commit()

    # Bg
    bg = ImageTk.PhotoImage(file=r"photos/wood_mainpage.jpg")
    bg_image = Label(worker_register, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # Left Image
    left = ImageTk.PhotoImage(file=r"photos/food-sunset-love-field.jpg")
    left_img = Label(worker_register, image=left).place(x=80, y=100, width=400, height=500)

    # The main background frame
    main_frame = Frame(worker_register, bg="white")
    main_frame.place(x=480, y=100, width=700, height=500)

    # The title of the Page
    title = Label(main_frame,
                  text="Worker Register",
                  font=("times new roman", 20, "bold"),
                  bg="white",
                  fg="black")
    title.place(x=50, y=30)

    # Column 1 Row 1
    worker_name = Label(main_frame,
                        text="Worker Name",
                        font=("times new roman", 15, "bold"),
                        bg="white",
                        fg="gray")
    worker_name.place(x=50, y=100)

    entry_name = Entry(main_frame,
                       font=("times new roman", 15),
                       borderwidth=2,
                       bg="lightgray")
    entry_name.place(x=50, y=130, width=250)

    # Column 2 Row 1
    contact_no = Label(main_frame,
                       text="Contact Number",
                       font=("times new roman", 15, "bold"),
                       bg="white",
                       fg="gray")
    contact_no.place(x=370, y=100)

    entry_contact = Entry(main_frame,
                          font=("times new roman", 15),
                          borderwidth=2,
                          bg="lightgray")
    entry_contact.place(x=370, y=130, width=250)

    # Column 1 Row 2
    email = Label(main_frame,
                  text="Email Id",
                  font=("times new roman", 15, "bold"),
                  bg="white",
                  fg="gray")
    email.place(x=50, y=160)

    entry_email = Entry(main_frame,
                        font=("times new roman", 15),
                        borderwidth=2,
                        bg="lightgray")
    entry_email.place(x=50, y=190, width=250)

    # Column 2 Row 2
    password = Label(main_frame,
                     text="Password",
                     font=("times new roman", 15, "bold"),
                     bg="white",
                     fg="gray")
    password.place(x=370, y=160)

    entry_password = Entry(main_frame,
                           font=("times new roman", 15),
                           borderwidth=2,
                           bg="lightgray",
                           show='*')
    entry_password.place(x=370, y=190, width=250)

    def customer_district(e):
        x = district_menu.get()
        cursor.execute(
            'SELECT city_name FROM city INNER JOIN district ON city.district_id=district.district_id WHERE district_name=?',
            (x,))
        citylist = cursor.fetchall()
        city_menu.config(value=citylist)

    cursor.execute('SELECT district_name FROM district')
    distlist = cursor.fetchall()

    district_id = Label(main_frame, text="District", font=("times new roman", 15, "bold"), bg="white",
                        fg="gray").place(x=50, y=220)
    district_menu = ttk.Combobox(main_frame, state="readonly", value=distlist)
    district_menu.place(x=50, y=250, width=250)

    city_id = Label(main_frame, text="City Id", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    city_id.place(x=370, y=220)
    city_menu = ttk.Combobox(main_frame, state="readonly")
    city_menu.place(x=370, y=250, width=250)

    district_menu.bind("<<ComboboxSelected>>", customer_district)

    # Column 1 Row 4
    exp_sal = Label(main_frame, text="Exp. Salary", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    exp_sal.place(x=50, y=280)
    entry_exp_sal = Entry(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_exp_sal.place(x=50, y=310, width=250)

    # Column 2 Row 4
    worker_status = Label(main_frame, text="Worker Status", font=("times new roman", 15, "bold"), bg="white",
                          fg="gray")
    worker_status.place(x=370, y=285)
    rb1 = Radiobutton(main_frame, text="Available", font=("times new roman", 15, "bold"), variable=var, value=0,
                      bg="white", fg="gray", selectcolor="white")
    rb2 = Radiobutton(main_frame, text="Busy", font=("times new roman", 15, "bold"), variable=var, value=1,
                      bg="white", fg="gray", selectcolor="white")
    rb1.place(x=370, y=330, anchor='w', width=100)
    rb2.place(x=500, y=330, anchor='w', width=80)

    # Column 1 Row 5
    address = Label(main_frame, text="Address", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    address.place(x=50, y=340)
    entry_address = Text(main_frame, font=("times new roman", 15), borderwidth=2, bg="lightgray")
    entry_address.place(x=50, y=370, width=250, height=80)

    # Column 1 Row 5
    profile = Label(main_frame, text="Work Profile", font=("times new roman", 15, "bold"), bg="white", fg="gray")
    profile.place(x=370, y=350)
    entry_profile = Entry(main_frame, font=("times new roman", 15), bg="lightgray")
    entry_profile.place(x=370, y=380, width=250)

    # Submit Button
    register_butt = Button(main_frame, text="Register", bd=2, font=("times new roman", 15), cursor="hand2",
                           command=register, justify="center", bg="white", borderwidth=3)
    register_butt.place(x=430, y=450, width=120)

    # Login Button
    login_butt = Button(worker_register, text="Login", bd=2, font=("times new roman", 15), cursor="hand2",
                        command=lambda: worker_login(worker_register),
                        justify="center", bg="white", borderwidth=3)
    login_butt.place(x=220, y=500, width=120)

    worker_register.mainloop()


def worker_login(mainpage):
    global wlogin
    mainpage.destroy()
    wlogin = Tk()
    wlogin.title("Login System")
    wlogin.geometry("1199x600+100+50")
    wlogin.resizable(False, False)
    # === BB Image ======
    bg = ImageTk.PhotoImage(file=r"photos/background.jpg")
    bg_image = Label(wlogin, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # ====Login Frame======
    Frame_login = Frame(wlogin, bg="white")
    Frame_login.place(x=150, y=150, height=340, width=500)

    title = Label(Frame_login, text="Login Here", font=("Berlin Sans FB Demi", 35, "bold"), fg="#d77337",
                  bg="white").place(x=120, y=30)
    desc = Label(Frame_login, text="Worker Login Area", font=("Goudy old style", 15, "bold"), fg="#d25d17",
                 bg="white").place(x=145, y=100)

    lbl_username = Label(Frame_login, text="Email Id", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=160)
    user_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    user_entry.place(x=150, y=160, width=250, height=35)

    lbl_password = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=40, y=220)
    pass_entry = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show='*')
    pass_entry.place(x=150, y=220, width=250, height=35)

    # forget_Button = Button(Frame_login, cursor="hand2", text="Forget Password?", bg="white", bd=0, fg="#d77337",
    #                        font=("times new roman", 15)).place(x=40, y=280)
    login_Button = Button(wlogin, cursor="hand2",
                          command=lambda: login_verify_worker(user_entry.get(), pass_entry.get()), text="Login",
                          fg="white",
                          bg="#d77337", font=("times new roman", 20)).place(x=300, y=470, width=180, height=40)
    wlogin.mainloop()


def login_verify_customer(username1, password1):
    if (password1 == "" or username1 == ""):
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor.execute('SELECT * from customer WHERE customer_email=? AND customer_password=?', (username1, password1))
        for i in cursor:
            if username1 in i and password1 in i:
                messagebox.showinfo("Welcome", "Login Successful,\nWelcome")
                customer_dashboard(clogin, username1,article,welcome_page)
                return
        messagebox.showerror("Error", "please enter correct values")


def login_verify_farmer(username1, password1):
    if (password1 == "" or username1 == ""):
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor.execute('SELECT * from farmer WHERE farmer_email=? AND farmer_password=?', (username1, password1))
        for i in cursor:
            if username1 in i and password1 in i:
                messagebox.showinfo("Welcome", "Login Successful,\nWelcome")
                farmer_dashboard(flogin, username1,article,welcome_page)
                return
        messagebox.showerror("Error", "please enter correct values")


def login_verify_worker(username1, password1):
    if (password1 == "" or username1 == ""):
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor.execute('SELECT * from worker WHERE worker_email=? AND worker_password=?', (username1, password1))
        for i in cursor:
            if username1 in i and password1 in i:
                messagebox.showinfo("Welcome", "Login Successful,\nWelcome")
                worker_dashboard(wlogin, username1,article,welcome_page)
                return
        messagebox.showerror("Error", "please enter correct values")




def farmer_dashboard(flogin,username,article,welcome):
    flogin.destroy()
    global farmer_dashboard
    farmer_dashboard = Tk()
    farmer_dashboard.title("XYZ")

    farmer_dashboard.geometry("1199x700+100+50")
    farmer_dashboard.resizable(False, False)

    bg = ImageTk.PhotoImage(file=r"photos/farmer dashboard.png")
    bg_image = Label(farmer_dashboard, image=bg).place(x=0, y=0, relheight=1, relwidth=1)

    def produce_for_sale():
        produceonline = Tk()
        produceonline.geometry("999x500+100+50")

        titlec = Label(produceonline, text="Products present in inventory", pady=10,
                       font=("Berlin Sans FB Demi", 30, "bold"),
                       fg="black").pack()

        display = ttk.Treeview(produceonline, selectmode='extended')
        display['columns'] = ("Produce_name", "variety_name", "quantity")

        style = ttk.Style(produceonline)
        style.configure('Treeview', rowheight=40)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("Produce_name", text="Product_name")
        display.heading("variety_name", text="variety_name")
        display.heading("quantity", text="quantity")

        for record in display.get_children():
            display.delete(record)
        count = 0

        cursor.execute('SELECT produce_name,variety_name,quantity FROM farmer_product WHERE farmer_email=?',
                       (username,))
        for row in cursor.fetchall():
            display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2]))
            count += 1
        display.pack()

    def hired_workers():
        hiredowrkers = Tk()
        hiredowrkers.geometry("999x500+100+50")

        titlec = Label(hiredowrkers, text="Workers Hired By You", pady=10,
                       font=("Berlin Sans FB Demi", 30, "bold"),
                       fg="black").pack()

        display = ttk.Treeview(hiredowrkers, selectmode='extended')
        display['columns'] = ("worker_name", "worker_contact_number","worker_profile","worker_email")

        style = ttk.Style(hiredowrkers)
        style.configure('Treeview', rowheight=40)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("worker_name", text="worker_name")
        display.heading("worker_contact_number", text="worker_contact_number")
        display.heading("worker_profile", text="worker_profile")
        display.heading("worker_email", text="worker_email")

        for record in display.get_children():
            display.delete(record)
        count = 0

        cursor.execute('SELECT worker_name,worker_contact_number,worker_profile,worker.worker_email FROM farmer_worker INNER JOIN worker ON farmer_worker.worker_email=worker.worker_email WHERE farmer_email=?',
                       (username,))
        for row in cursor.fetchall():
            display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2], row[3]))
            count += 1
        display.pack()

    def farmer_upload():
        # farmer_dashboard.destroy()
        farmupload_window = Tk()
        farmupload_window.geometry("700x500+100+50")
        # bg = ImageTk.PhotoImage(file=r"back.png")
        # bg_image = Label(farmupload_window, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        category = StringVar()
        product = StringVar()
        variety = StringVar()

        def insertcrop():
            def delete_data(entry_field):
                entry_field.delete(0, "end")


            try:
                float(quantity.get())
                float(price.get())

                cursor.execute(
                    'INSERT INTO farmer_product(category_name, produce_name,variety_name ,quantity ,product_price , farmer_email ) VALUES (?,?,?,?,?,?)',
                    (
                    Category_menu.get(), produce_menu.get(), variety_menu.get(), quantity.get(), price.get(), username))
                connection.commit()
                messagebox.showinfo("Success", "Product inserted into inventory")
                farmupload_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
                delete_data(quantity)
                delete_data(price)
                return

            # is_number(quantity)
            # is_number(price)
            # print(quantity.get())
            # print(price.get())


        def farmer_upload_category(e):
            produce_menu.set("")
            variety_menu.set("")
            x = Category_menu.get()
            cursor.execute(
                'SELECT produce_name FROM produce INNER JOIN category ON produce.category_id=category.category_id WHERE category_name=?',
                (x,))
            producelist = cursor.fetchall()
            produce_menu.config(value=producelist)


        def farmer_upload_produce(e):
            variety_menu.set("")
            cursor.execute(
                'SELECT variety_name FROM variety INNER JOIN produce ON produce.produce_id=variety.produce_id WHERE produce_name=?',
                (produce_menu.get(),))
            varietylist = cursor.fetchall()
            variety_menu.config(value=varietylist)

        def farmer_upload_variety(e):

            insert_button = Button(farmupload_window, text="Insert the crop", command=insertcrop, cursor="hand2",
                                   bg="orange", bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=150,
                                                                                                                  y=400,
                                                                                                                  width=150,
                                                                                                                  height=40)


        back = Button(farmupload_window, text="Back", command=lambda: farmupload_window.destroy(), cursor="hand2",
                      bg="orange", bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=350,
                                                                                                     y=400,
                                                                                                     width=150,
                                                                                                     height=40)
        cursor.execute('SELECT category_name FROM category WHERE category_type="Produce"')
        categorylist = cursor.fetchall()

        titlec = Label(farmupload_window, text="Input Product Information",pady=15, font=("Berlin Sans FB Demi", 30, "bold"),
                       fg="black" ).pack()
        l4 = Label(farmupload_window, text="select category",font=("Berlin Sans FB Demi", 15, "bold")).pack()
        Category_menu = ttk.Combobox(farmupload_window, state="readonly", value=categorylist)
        Category_menu.pack()

        l5 = Label(farmupload_window, text="select produce",font=("Berlin Sans FB Demi", 15, "bold")).pack()
        produce_menu = ttk.Combobox(farmupload_window, state="readonly")
        produce_menu.pack()

        l6 = Label(farmupload_window, text="select variety",font=("Berlin Sans FB Demi", 15, "bold")).pack()
        variety_menu = ttk.Combobox(farmupload_window, state="readonly")
        variety_menu.pack()

        produce_menu.bind("<<ComboboxSelected>>", farmer_upload_produce)
        Category_menu.bind("<<ComboboxSelected>>", farmer_upload_category)
        variety_menu.bind("<<ComboboxSelected>>", farmer_upload_variety)

        quantity = Entry(farmupload_window)
        price = Entry(farmupload_window)
        l2 = Label(farmupload_window, text="Enter Quantity", font=("Berlin Sans FB Demi", 15, "bold")).pack()

        quantity.pack()
        l3 = Label(farmupload_window, text="Enter rate per unit quantity",
                   font=("Berlin Sans FB Demi", 15, "bold")).pack()

        price.pack()

    def farmer_hire():
        # farmer_dashboard.destroy()
        farmhirewindow = Tk()
        farmhirewindow.geometry("1199x600+100+50")

        def workers_display(e):
            for record in display.get_children():
                display.delete(record)
            count = 0
            x = city_menu.get()
            cursor.execute(
                'SELECT worker_name,worker_contact_number,worker_profile,expected_salary,worker_email FROM worker INNER JOIN city ON worker.city_id=city.city_id WHERE worker_status=0 AND city_name=?',
                (city_menu.get(),))
            for row in cursor.fetchall():
                display.insert(parent='', index='end', iid=count, text="",
                               values=(row[0], row[1], row[2], row[3], row[4]))
                count += 1
            # if count==0:
            #     Label(farmhirewindow, text="No worker Found", pady=15,
            #           font=("Berlin Sans FB Demi",10, "bold"),
            #           fg="black").place(x=700,y=550,height=40,width=50)


        def insert_worker():
            selected = display.item(display.focus(), 'values')
            cursor.execute('UPDATE worker set worker_status=1 where worker_email=?', (selected[4],))
            worker_email = selected[4]
            cursor.execute('INSERT INTO farmer_worker VALUES (?,?)', (worker_email, username,))
            connection.commit()
            messagebox.showinfo("success","Worker Hired Successfully!")
            farmhirewindow.destroy()

        def biodata_worker(e):
            # selected = display.item(display.focus(), 'values')
            # cursor.execute('SELECT worker_biodata FROM worker where worker_email=?', (selected[4],))
            # x = cursor.fetchall()
            # msg.config(text=x)
            hire = Button(farmhirewindow, cursor="hand2", text="Hire Worker", fg="white", bg="orange",pady=5,
                          command=insert_worker,
                          font=("times new roman", 20)).pack()

        def hire_district(e):
            city_menu.set("")
            x = district_menu.get()
            cursor.execute(
                'SELECT city_name FROM city INNER JOIN district ON city.district_id=district.district_id WHERE district_name=?',
                (x,))
            citylist = cursor.fetchall()
            city_menu.config(value=citylist)

        cursor.execute('SELECT district_name FROM district')
        distlist = cursor.fetchall()

        titlec = Label(farmhirewindow, text="Select Worker to be Hired", pady=15,
                       font=("Berlin Sans FB Demi", 30, "bold"),
                       fg="black").pack()

        display = ttk.Treeview(farmhirewindow, selectmode='extended')
        display['columns'] = (
            "worker_name", "worker_contact_number", "worker_profile", "expected_salary", "worker_email")

        district_id = Label(farmhirewindow, text="Select District", font=("Berlin Sans FB Demi", 15, "bold"),
                            fg="gray").pack()
        district_menu = ttk.Combobox(farmhirewindow, state="readonly", value=distlist)
        district_menu.pack()

        city_id = Label(farmhirewindow, text="Select City", font=("Berlin Sans FB Demi", 15, "bold"), fg="gray")
        city_id.pack()
        city_menu = ttk.Combobox(farmhirewindow, state="readonly")
        city_menu.pack()

        district_menu.bind("<<ComboboxSelected>>", hire_district)
        city_menu.bind("<<ComboboxSelected>>", workers_display)
        display.bind("<ButtonRelease-1>", biodata_worker)
        # msg = Message(farmhirewindow, text="")
        # msg.pack()

        style = ttk.Style(farmhirewindow)
        style.configure('Treeview', rowheight=40)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("worker_name", text="worker_name")
        display.heading("worker_contact_number", text="worker_contact_number")
        display.heading("worker_profile", text="worker_profile")
        display.heading("expected_salary", text="expected_salary")
        display.heading("worker_email", text="worker_email")

        display.pack()



    def farmer_kit():
        # farmer_dashboard.destroy()
        farmerkit = Tk()
        farmerkit.geometry("1099x600+100+50")
        category = StringVar()

        def addcart():
            selected = display.item(display.focus(), 'values')
            totalprice = float(quantity.get()) * float(selected[2])
            print(totalprice)
            cursor.execute('INSERT INTO farmer_cart VALUES (?,?,?,?)',
                           (selected[0], quantity.get(), totalprice, username))
            connection.commit()
            messagebox.showinfo("success!", "item succesfully inserted")
            quantity.delete(0, END)
            farmerkit.destroy()

        def catpicked(e):
            for record in display.get_children():
                display.delete(record)
            count = 0

            x = Category_menu.get()

            cursor.execute(
                'SELECT selling_product_name,kit_quantity_type,kit_price FROM farmer_kit INNER JOIN category ON farmer_kit.category_id=category.category_id WHERE category.category_name=?',
                (x,))
            for row in cursor.fetchall():
                display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2]))
                count += 1

        titlec = Label(farmerkit, text="Select the item you wish to buy", pady=10,
                       font=("Berlin Sans FB Demi", 30, "bold"),
                       fg="black" ).pack()

        cursor.execute('SELECT category_name FROM category WHERE category_type="SellingProduct"')
        categorylist = cursor.fetchall()
        l4 = Label(farmerkit, text="select category",pady=10,
                       font=("Berlin Sans FB Demi", 15, "bold")).pack()
        Category_menu = ttk.Combobox(farmerkit, state="readonly", value=categorylist)
        Category_menu.pack()

        display = ttk.Treeview(farmerkit, selectmode='extended')
        display['columns'] = ("Product_name", "Quantity_type", "cost")

        style = ttk.Style(farmerkit)
        style.configure('Treeview', rowheight=40)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("Product_name", text="Product_name")
        display.heading("Quantity_type", text="Quantity_type")
        display.heading("cost", text="cost")

        display.pack()
        msg = Message(farmerkit, text="")
        msg.pack()
        l6 = Label(farmerkit, text="Enter Quantity ",pady=0,
                       font=("Berlin Sans FB Demi",15, "bold"))
        l6.pack()
        quantity = Entry(farmerkit)
        quantity.pack()
        buybutton = Button(farmerkit, text="Add to cart", command=addcart, cursor="hand2", bg="orange", bd=0,
                           fg="white", font=("times new roman", 15, "bold")).place(x=475,
                                                                                   y=450,
                                                                                   width=150,
                                                                                   height=40)
        Category_menu.bind("<<ComboboxSelected>>", catpicked)

        back = Button(farmerkit, text="Back", command=lambda: farmerkit.destroy(), cursor="hand2",
                      bg="orange", bd=0, fg="white", font=("times new roman", 15, "bold")).place(x=475,
                                                                                                     y=500,
                                                                                                     width=150,
                                                                                                     height=40)

    def farmer_cart():

        def buy_now():
            cursor.execute('DELETE FROM farmer_cart WHERE farmer_email=?', (username,))
            connection.commit()
            messagebox.showinfo("payment successful", "Succesfully Bought the items")
            farmercart.destroy()
            # return to dashboard here

        # farmer_dashboard.destroy()
        farmercart = Tk()
        farmercart.geometry("1199x500+100+50")
        titlec = Label(farmercart, text="These are the items you have selected", pady=10,
                       font=("Berlin Sans FB Demi", 25, "bold"),
                       fg="black").pack()

        display = ttk.Treeview(farmercart, selectmode='extended')
        display['columns'] = ("Product_name", "Quantity", "cost")

        style = ttk.Style(farmercart)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("Product_name", text="Product_name")
        display.heading("Quantity", text="Quantity")
        display.heading("cost", text="cost")

        for record in display.get_children():
            display.delete(record)

        count = 0
        cursor.execute('SELECT produce_name,quantity,total_price FROM farmer_cart WHERE farmer_email=?', (username,))
        for row in cursor.fetchall():
            display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2]))
            count += 1

        display.pack()

        totalcostlabel = Label(farmercart, text="Your total bill amount is ",pady=5,
                       font=("Berlin Sans FB Demi",15, "bold")).pack()
        cursor.execute('SELECT SUM(total_price) from farmer_cart')
        x = cursor.fetchall()
        totalcostlabel2 = Label(farmercart, text=x,pady=5,
                       font=("Berlin Sans FB Demi",15, "bold"))
        totalcostlabel2.pack()

        buynow = Button(farmercart, cursor="hand2", command=buy_now, text="buy now", fg="white", bg="#d77337",
                        font=("times new roman", 20))
        buynow.pack()

    photo1 = ImageTk.PhotoImage(file=r"photos/farmers-market-icon.png")
    photo2 = ImageTk.PhotoImage(file=r"photos/kit.png")
    photo3 = ImageTk.PhotoImage(file=r"photos/cart.png")
    photo4 = ImageTk.PhotoImage(file=r"photos/worker.png")
    photo5 = ImageTk.PhotoImage(file=r"photos/article.jpg")
    photo6 = ImageTk.PhotoImage(file=r"photos/statistics.png")
    photo7 = ImageTk.PhotoImage(file=r"photos/back.png")
    market_upload = Button(farmer_dashboard, cursor="hand2", text=" Market", command=farmer_upload, fg="black",
                           bg="white",image=photo1,compound=LEFT,pady=5,
                           font=("times new roman", 20)).place(x=320, y=10, width=190, height=50)
    kit_buy = Button(farmer_dashboard, cursor="hand2", text="  Kit", fg="black", bg="white",image=photo2,compound=LEFT,pady=10, command=farmer_kit,
                     font=("times new roman", 20)).place(x=510, y=10, width=190, height=50)
    cart = Button(farmer_dashboard, cursor="hand2", text="   Cart", fg="black", bg="white",image=photo3,compound=LEFT,pady=10, command=farmer_cart,
                  font=("times new roman", 20)).place(x=700, y=10, width=190, height=50)
    hire = Button(farmer_dashboard, cursor="hand2", text="   Hire", fg="black",bg="white",image=photo4,compound=LEFT,pady=10,command=farmer_hire,
                  font=("times new roman", 20)).place(x=890, y=10, width=190, height=50)
    article = Button(farmer_dashboard, cursor="hand2", text="Article", fg="black", bg="white", image=photo5, compound=LEFT,command=article,
                  pady=10,
                  font=("times new roman", 20)).place(x=130, y=10, width=190, height=50)
    history = Button(farmer_dashboard, cursor="hand2", text="My Crops", fg="black", bg="white",command=produce_for_sale,
                     font=("times new roman", 20)).place(x=410, y=550, width=190, height=50)
    history1 = Button(farmer_dashboard, cursor="hand2", text="Hired Workers", fg="black", bg="white",
                     command=hired_workers,
                     font=("times new roman", 20)).place(x=620, y=550, width=190, height=50)
    def logout():
        farmer_dashboard.destroy()
        welcome()

    back = Button(farmer_dashboard, cursor="hand2", command=logout, text="Log Out", fg="black",image=photo7,compound=LEFT,
                         bg="white",font=("times new roman", 20)).place(x=0, y=660, width=160, height=40)
    farmer_dashboard.mainloop()


def worker_dashboard(wlogin, username,article,welcome):
    wlogin.destroy()

    worker_dashboard = Tk()
    worker_dashboard.title("XYZ")

    worker_dashboard.geometry("1199x700+100+50")
    worker_dashboard.resizable(False, False)

    def bio():
        def insert_bio():
            cursor.execute('UPDATE worker set worker_biodata=? where worker_email=?',
                           (entry_bio.get("1.0", END), username))
            connection.commit()
            bio_window.destroy()

        bio_window = Tk()
        bio_window.geometry("600x400+100+50")
        bio = Label(bio_window, text="Enter Bio Data", font=("times new roman", 25, "bold"), bg="lightgray", fg="black")
        bio.place(x=200, y=10)
        entry_bio = Text(bio_window, font=("times new roman", 15), borderwidth=2, bg="lightgray")
        entry_bio.place(x=125, y=70, width=350, height=180)
        submit = Button(bio_window, cursor="hand2", text="Submit", fg="black", bg="white", command=insert_bio,
                        font=("times new roman", 20)).place(x=200, y=280, width=190, height=50)

    def status():
        status_window = Tk()
        status_window.geometry("500x300+100+50")
        cursor.execute('SELECT worker_status from worker where worker_email=?', (username,))
        status = cursor.fetchall()
        status = status[0][0]
        print(status)
        v = ""

        def exit():
            status_window.destroy()

        if status == 1:
            cursor.execute(
                'SELECT farmer_name,farmer_contact_number from farmer_worker INNER JOIN farmer ON farmer.farmer_email=farmer_worker.farmer_email WHERE worker_email =?',
                (username,))
            for i in cursor.fetchall():
                v = "Hired!" + "\n\n" + "Farmer Name :" + i[0] + "\n" + "Farmer Contact Number:" + i[1]
        else:
            v = "Not Hired Yet"
        info_label = Label(status_window, text=v, font=("times new roman", 15, "bold"), fg="black").place(
            x=130, y=10)
        submit = Button(status_window, cursor="hand2", text="OK", fg="black", bg="white", command=exit,
                        font=("times new roman", 20)).place(x=160, y=180, width=190, height=50)

    bg = ImageTk.PhotoImage(file=r"photos/worker dashboard.png")
    bg_image = Label(worker_dashboard, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    photo5 = ImageTk.PhotoImage(file=r"photos/article.jpg")
    photo6 = ImageTk.PhotoImage(file=r"photos/statistics.png")
    photo7 = ImageTk.PhotoImage(file=r"photos/back.png")
    BioData = Button(worker_dashboard, cursor="hand2", text="Enter Bio Data", fg="black", bg="white", command=bio,
                     font=("times new roman", 20)).place(x=350, y=500, width=190, height=50)
    Status = Button(worker_dashboard, cursor="hand2", text="Check Status", fg="black", bg="white", command=status,
                    font=("times new roman", 20)).place(x=650, y=500, width=190, height=50)
    article = Button(worker_dashboard, cursor="hand2", text="  Article", fg="black", bg="white",
                     image=photo5, compound=LEFT, command=article,
                     pady=10, font=("times new roman", 20)).place(x=520, y=40, width=190, height=50)

    def logout():
        worker_dashboard.destroy()
        welcome()

    back = Button(worker_dashboard, cursor="hand2", command=logout, text="Log Out", fg="black",image=photo7,compound=LEFT,
                         bg="white",font=("times new roman", 20)).place(x=0, y=660, width=160, height=40)

    worker_dashboard.mainloop()



def customer_dashboard(clogin,username,article,welcome):

    clogin.destroy()
    global cust_dashboard
    cust_dashboard = Tk()
    cust_dashboard.title("XYZ")

    cust_dashboard.geometry("1199x700+100+50")
    cust_dashboard.resizable(False, False)

    bg = ImageTk.PhotoImage(file=r"photos/customer dashboard .png")
    bg_image = Label(cust_dashboard, image=bg).place(x=0, y=0, relheight=1, relwidth=1)

    def cust_buy():

        custbuy = Tk()
        custbuy.title("Farmer's Market")

        custbuy.geometry("999x700+100+50")
        custbuy.resizable(False, False)

        def customer_addcart():
            selected = display.item(display.focus(), 'values')
            if (float(quantity.get()) > float(selected[2])):
                messagebox.showerror("error", "Enter quantity within availibility")
                quantity.delete(0, END)
            else:
                totalprice = float(quantity.get()) * float(selected[1])
                left = float(selected[2]) - float(quantity.get())
                cursor.execute('INSERT INTO customer_cart VALUES (?,?,?,?,?)',
                               (produce_menu.get(), variety_menu.get(), quantity.get(), totalprice, username))
                connection.commit()
                cursor.execute('UPDATE farmer_product SET quantity=? WHERE product_id=?',
                               (float(left), selected[0],))
                connection.commit()
                cursor.execute('DELETE FROM farmer_product WHERE quantity=0.0')
                connection.commit()
                messagebox.showinfo("success!", "item succesfully inserted")
                quantity.delete(0, END)
                custbuy.destroy()

        def catpicked(e):
            produce_menu.set("")
            variety_menu.set("")
            x = Category_menu.get()
            cursor.execute('SELECT DISTINCT produce_name FROM farmer_product WHERE category_name=?', (x,))
            producelist = cursor.fetchall()
            produce_menu.config(value=producelist)

        def prodpicked(e):
            variety_menu.set("")
            cursor.execute('SELECT DISTINCT variety_name FROM farmer_product WHERE produce_name=?',
                           (produce_menu.get(),))
            varietylist = cursor.fetchall()
            variety_menu.config(value=varietylist)

        def varpicked(e):
            cursor.execute('SELECT product_id,product_price,quantity FROM farmer_product WHERE produce_name=? AND variety_name=?',
                (produce_menu.get(), variety_menu.get()))

            for record in display.get_children():
                display.delete(record)
            count = 0

            for row in cursor.fetchall():
                display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2]))
                count += 1

            # cursor.execute('INSERT INTO custcart VALUES (?,?,?,?,?,?)',(category_menu.get(),produce_menu.get(),variety_menu.get(),quantity.get(),price.get(),FarmerID))

        cursor.execute('SELECT DISTINCT category_name FROM farmer_product')
        categorylist = cursor.fetchall()

        titlec = Label(custbuy, text="Select the item you wish to buy", pady=10,font=("Berlin Sans FB Demi", 30, "bold"),fg="black" ).pack()

        l4 = Label(custbuy, text="select category",pady=10,font=("Berlin Sans FB Demi", 15, "bold")).pack()
        Category_menu = ttk.Combobox(custbuy, state="readonly", value=categorylist)
        Category_menu.pack()

        l5 = Label(custbuy, text="select produce",pady=10,font=("Berlin Sans FB Demi", 15, "bold")).pack()
        produce_menu = ttk.Combobox(custbuy, state="readonly")
        produce_menu.pack()

        l6 = Label(custbuy, text="select variety",pady=10,font=("Berlin Sans FB Demi", 15, "bold")).pack()
        variety_menu = ttk.Combobox(custbuy, state="readonly")
        variety_menu.pack()

        display = ttk.Treeview(custbuy, selectmode='extended')
        display['columns'] = ("Product ID", "price", "quantity")

        style = ttk.Style(custbuy)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("Product ID", text="Product ID")
        display.heading("price", text="price")
        display.heading("quantity", text="quantity")
        display.pack()

        l6 = Label(custbuy, text="Enter Quantity ",pady=10,font=("Berlin Sans FB Demi", 15, "bold"))
        l6.pack()
        quantity = Entry(custbuy)
        quantity.pack()
        buybutton = Button(custbuy, text="Add to cart", command=customer_addcart, cursor="hand2", bg="orange",
                           bd=3,pady=5,
                           fg="white", font=("times new roman", 15, "bold")).place(x=439,y=600)
        produce_menu.bind("<<ComboboxSelected>>", prodpicked)
        Category_menu.bind("<<ComboboxSelected>>", catpicked)
        variety_menu.bind("<<ComboboxSelected>>", varpicked)

    def customer_cart():

        def buy_now():
            cursor.execute('SELECT * FROM customer_cart WHERE customer_email=?', (username,))
            for q in cursor.fetchall():
                cursor.execute('INSERT INTO customer_history VALUES (?,?,?,?,?)', (q[0], q[1], q[2], q[3], q[4],))
            connection.commit()
            cursor.execute('DELETE FROM customer_cart WHERE customer_email=?', (username,))
            connection.commit()
            messagebox.showinfo(title="payment successful", message="Succesfully Bought the items")
            customercart.destroy()

        customercart = Tk()
        customercart.geometry("1199x500+100+50")

        display = ttk.Treeview(customercart, selectmode='extended')
        display['columns'] = ("Produce_name", "variety_name", "Quantity", "cost")

        style = ttk.Style(customercart)
        style.theme_use('clam')

        display.column("#0", width=0, stretch=NO)
        display.heading("Produce_name", text="Produce_name")
        display.heading("variety_name", text="variety_name")
        display.heading("Quantity", text="Quantity")
        display.heading("cost", text="cost")

        totalcostlabel = Label(customercart, text="Your total bill amount is ", pady=5,font=("Berlin Sans FB Demi", 18, "bold")).pack()


        for record in display.get_children():
            display.delete(record)

        count = 0
        cursor.execute('SELECT produce_name,variety_name,quantity,cost FROM customer_cart where customer_email=?',
                       (username,))
        for row in cursor.fetchall():
            display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2], row[3]))
            count += 1

        display.pack()
        totalcostlabel = Label(customercart, text="Your total bill amount is ", pady=5,font=("Berlin Sans FB Demi", 15, "bold")).pack()
        cursor.execute('SELECT SUM(cost) from customer_cart')
        x = cursor.fetchall()
        totalcostlabel2 = Label(customercart, text=x, pady=5,font=("Berlin Sans FB Demi", 15, "bold")).pack()

        buynow = Button(customercart, cursor="hand2", command=buy_now, text="buy now", fg="white", bg="#d77337",font=("times new roman", 20))
        buynow.pack()

    def customer_history():
        customerhistory = Tk()
        customerhistory.geometry("1199x500+100+50")

        display = ttk.Treeview(customerhistory, selectmode='extended')
        display['columns'] = ("Produce_name", "variety_name", "Quantity", "cost")

        style = ttk.Style(customerhistory)
        style.theme_use('clam')

        titlec = Label(customerhistory, text="History of items you have previously purchased", pady=10,
                       font=("Berlin Sans FB Demi", 25, "bold"),
                       fg="black").pack()

        display.column("#0", width=0, stretch=NO)
        display.heading("Produce_name", text="Produce_name")
        display.heading("variety_name", text="variety_name")
        display.heading("Quantity", text="Quantity")
        display.heading("cost", text="cost")

        for record in display.get_children():
            display.delete(record)

        count = 0
        cursor.execute(
            'SELECT produce_name,variety_name,quantity,cost FROM customer_history where customer_email=?',
            (username,))
        for row in cursor.fetchall():
            display.insert(parent='', index='end', iid=count, text="", values=(row[0], row[1], row[2], row[3]))
            count += 1

        def back():
            customerhistory.destroy()

        display.pack()
        buynow = Button(customerhistory, cursor="hand2", command=back, text="Back", fg="white", bg="orange",
                        font=("times new roman", 20)).place(x=510,y=380,width=180,height=40)

    def logout():
        cust_dashboard.destroy()
        welcome()

    photo1 = ImageTk.PhotoImage(file=r"photos/farmers-market-icon.png")
    photo3 = ImageTk.PhotoImage(file=r"photos/cart.png")
    photo5 = ImageTk.PhotoImage(file=r"photos/article.jpg")
    photo6 = ImageTk.PhotoImage(file=r"photos/statistics.png")
    photo7 = ImageTk.PhotoImage(file=r"photos/back.png")


    customer_buy = Button(cust_dashboard, cursor="hand2", text="  Market", command=cust_buy, fg="black",
                          bg="white", image=photo1, compound=LEFT, pady=20, font=("times new roman", 20)).place(x=510, y=20, width=190, height=50)

    cart = Button(cust_dashboard, cursor="hand2", command=customer_cart, text="  Cart", fg="black", bg="white",image=photo3, compound=LEFT,
                  pady=10,font=("times new roman", 20)).place(x=700, y=20, width=190, height=50)

    article = Button(cust_dashboard, cursor="hand2",  text="  Article", fg="black", bg="white",
                  image=photo5, compound=LEFT,command=article,
                  pady=10, font=("times new roman", 20)).place(x=320, y=20, width=190, height=50)


    past_orders = Button(cust_dashboard, cursor="hand2", command=customer_history, text="Order History", fg="black",
                         bg="white",
                         font=("times new roman", 20)).place(x=490, y=550, width=190, height=50)


    back = Button(cust_dashboard, cursor="hand2", command=logout, text="Log Out", fg="black",image=photo7,compound=LEFT,
                         bg="white",font=("times new roman", 20)).place(x=0, y=650, width=180, height=50)



    cust_dashboard.mainloop()


welcome_page()
