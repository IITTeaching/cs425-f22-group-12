import decimal

import psycopg2
from os import system, name
from decimal import Decimal

conn = psycopg2.connect(
    host="localhost",
    database="Bank",
    user="postgres",
    password="")
cur=conn.cursor()
def create_new_id(table_name):
    l=[]
    cur.execute("Select * from {};".format(table_name,))
    rec=cur.fetchall()
    for row in rec:
        l.append(int(row[0]))
    l.sort()
    if(len(l)==0):
        return 1
    return str(l[len(l)-1]+1)


def choose_b():
    clear()
    logo()
    print("\n Branches: ")
    cur.execute("Select branch_id,state,zip from branch natural join address;")
    rec = cur.fetchall()
    l =[]
    for row in rec:
        l.append(int(row[0]))
        print(" ",row[0], ".", row[1], row[2])
    l.sort()
    while True:
        add_id = input("\nChoose a Home branch: ")
        if (int(add_id.strip()) <= len(l) and int(add_id.strip()) > 0):
            return add_id
        else:
            print("invalid")

def choose_ad():
    print()
    print(" 1.Choose from exisiting address")
    print(" 2.Create new address")
    print(" Press any other key to return to main screen")
    user=input("\nChoose an option: ")
    if(user.strip()=='1'):
        cur.execute("Select * from address;")
        rec=cur.fetchall()
        l=[]

        clear()
        logo()
        print("\n Addresses: ")
        for row in rec:
            l.append(int(row[0]))
            print(" ",row[0],".",row[1],row[2],row[3])
        l.sort()
        while True:
            add_id=input("\nChoose an address id: ")
            if(int(add_id.strip())<=len(l) and int(add_id.strip())>0):
                return add_id
            else:
                print("invalid")
    elif(user.strip()=='2'):
        while True:
            try:
                clear()
                logo()
                city=input("\n Enter Name of city: ")
                state=input(" Enter Name of state: ")
                zip=input(" Enter zip: ")
                add_id=create_new_id('address')
                cur.execute("Insert into address values ({},'{}','{}','{}');".format(add_id,city,state,zip))
                conn.commit()
                print("New Address successfully added!")
                return add_id
            except(Exception, psycopg2.DatabaseError) as e:
                print("eeror:",e)
                print("try again")
    else:
        return -1
def create_new():
    try:
        clear()
        logo()

        print()
        print("Hello There!")
        print("I will guide you to create your own BKS account")
        name=input("\nPlease Enter your name: ")

        clear()
        logo()
        print("\nChoose an address")
        add_id=choose_ad()
        if(add_id==-1):
            return -1
        b_id=choose_b()
        c_id=create_new_id("customer")
        clear()
        logo()
        password=input("\nPlease enter a password to keep your account secure(less than 8 digit): ")
        cur.execute("insert into customer values({},'{}','{}','{}','{}');".format(c_id,name,b_id,add_id,password))
        conn.commit()
        clear()
        logo()
        print("\nCongratulations! your account has been created successfully.")
        print("Your c_id is ",c_id)
        return c_id
        # Need to have a pause here so the user can see their ID before moving to the next screen.
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("Please Try again")

def signin():
    clear()
    logo()
    while(True):
        print()
        print("SIGN IN")
        print()
        id=input(" Enter you ID no: ")
        pas=input(" Enter your Password: ")
        cur.execute("Select * from customer where customer_id='{}' and password='{}'".format(id.strip(),pas))
        rec=cur.fetchone()
        if(rec):
            return id.strip()
        else:
            clear()
            logo()
            print("Invalid ID or PassWord , Please Try again")
            print()
# this is the function for the customer interface

def show_accounts(c_id):
    cur.execute("SELECT * FROM account WHERE customer_id = '{}';".format(c_id))
    rec = cur.fetchall()
    l = []
    print()
    print("  ID.   Type       Balance")
    for row in rec:
        l.append(int(row[0]))
        if (row[1] == 'C'):
            print(" ", row[0], ".  ", "Checking  ", row[2])
        elif (row[1] == 'S'):
            print(" ", row[0], ".  ", "Saving    ", row[2])
    l.sort()
    return l;

def cust(c_id):
    while True:
        clear()
        logo()
        cur.execute("Select name from customer where customer_id='{}'".format(c_id))
        rec=cur.fetchone()
        print()
        print(" Welcome Back",rec[0])
        print()
        print("Choose from the options below to manage or create accounts")
        print(" 1.Create account")
        print(" 2.Deposit money into an account")
        print(" 3.Withdraw money from an account")
        print(" 4.Transfer money between accounts")
        print(" 5.Transfer money to an external account")
        print(" 6.Log out")
        print()
        choose=input("Choose an option here: ")
        # CREATING A NEW ACCOUNT
        if(choose.strip()=='1'):
            print()
            print("Account Type: ")
            choose_acc_type(c_id)

        # DEPOSIT
        elif(choose.strip()=='2'):
            l=show_accounts(c_id)
            while True:
                acc_id = input("\nChoose an account id: ")
                if (int(acc_id.strip()) in l):
                    print()
                    amount = input("Please choose deposit amount: ")
                    print()
                    if (decimal.Decimal(amount.strip()) <= 0):
                        print("Amount to be deposited is less than or equals to $0")
                        print(("Returning to home screen"))
                        break
                    description = input("Please write a short description: ")
                    deposit(amount, acc_id, c_id, description)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break

        # WITHDRAW
        elif(choose.strip()=='3'):
            l=show_accounts(c_id)
            while True:
                acc_id = input("\nChoose an account id: ")
                if (int(acc_id.strip()) in l):
                    print()
                    amount = input("Please choose withdrawal amount: ")
                    print()
                    if(check_balance(amount,acc_id)==-1):
                        print("Amount to be withdrawn greater than account balance")
                        print(("Returning to home screen"))
                        break
                    description = input("Please write a short description: ")
                    withdraw(amount, acc_id, c_id, description)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break
            pass

        # INTERNAL TRANSFER
        elif(choose.strip() == '4'):
            while True:
                l = show_accounts(c_id)
                acc_from_id = input("\nChoose the id of the account you want to transfer the money from: ")
                cur.execute("SELECT * FROM account;")
                rec2 = cur.fetchall()
                l2 = []
                print()
                print("To accounts: ")
                print("  ID.   Type")
                for row in rec2:
                    l2.append(int(row[0]))
                    if (row[1] == 'C'):
                        print(" ", row[0], ".  ", "Checking")
                    elif (row[1] == 'S'):
                        print(" ", row[0], ".  ", "Saving")
                l2.sort()
                acc_to_id = input("\nChoose the id of the account you want to transfer the money to: ")
                if (int(acc_from_id.strip()) in l and int(acc_to_id.strip()) in l2):
                    print()
                    amount = input("Please choose transfer amount: ")
                    print()
                    if (check_balance(amount, acc_from_id)):
                        print("Amount to be withdrawn greater than account balance")
                        print(("Returning to home screen"))
                        break
                    description = input("Please write a short description: ")
                    loc_transfer(acc_from_id, acc_to_id, description, c_id, amount)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break

            pass

        # EXTERNAL TRANSFER
        elif (choose.strip() == '5'):
            cur.execute("SELECT * FROM account WHERE customer_id = '{}';".format(c_id))
            rec = cur.fetchall()
            l = []
            print()
            print("From accounts: ")
            print("  ID.   Type       Balance")
            for row in rec:
                l.append(int(row[0]))
                if (row[1] == 'C'):
                    print(" ", row[0], ".  ", "Checking  ", row[2])
                elif (row[1] == 'S'):
                    print(" ", row[0], ".  ", "Saving    ", row[2])
            l.sort()

            while True:
                acc_from_id = input("\nChoose the id of the account you want to transfer the money from: ")
                if (int(acc_from_id.strip()) in l):
                    print()
                    bank = input("Please enter which bank you want to transfer funds to: ")
                    print()
                    account_number = input("Please enter the account number (12 Digits): ")
                    print()
                    routing_number = input("Please enter the routing number (9 Digits): ")
                    print()
                    amount = input("Please choose transfer amount: ")
                    print()
                    if (check_balance(amount, acc_from_id)):
                        print("Transfer amount is greater than account balance")
                        print(("Returning to home screen"))
                        break
                    description = input("Please write a short description: ")
                    ext_transfer(acc_from_id, c_id, bank, account_number, routing_number, amount, description)
                    break
                else:
                    print("invalid")

            pass

        # LOG OUT
        elif(choose.strip() == '6'):
            print()
            print("You have been signed out")
            print()
            return
        else:
            print("Choose a valid option")

def choose_acc_type(c_id):
    print()
    print(" 1.Checking account")
    print(" 2.Saving account")
    print(" Press any other key to return to main screen")

    account_type = input("\nPlease enter the account type you want to create: ")
    if (account_type.strip() == '1'):
        try:
            clear()
            logo()
            acc_type = "C"
            balance = 0
            add_id = create_new_id('account')
            cur.execute("Insert into account values ({},'{}',{},{});".format(add_id, acc_type, balance, c_id))
            conn.commit()
            print("New checking account successfully created!with Id: ",add_id)
        except(Exception, psycopg2.DatabaseError) as e:
            print("error:", e)
            print("try again")

    elif (account_type.strip() == '2'):
        try:
            clear()
            logo()
            acc_type = "S"
            balance = 0
            add_id = create_new_id('account')
            cur.execute("Insert into account values ({},'{}',{},{});".format(add_id, acc_type, balance, c_id))
            conn.commit()
            print("New saving account successfully created! with Id: ",add_id)
        except(Exception, psycopg2.DatabaseError) as e:
            print("error:", e)
            print("try again")
    else:
        return

def check_balance(amount,ac_id):
    cur.execute("Select Balance from account where account_id='{}'".format(ac_id))
    rec=cur.fetchone()
    if(decimal.Decimal(amount.strip())>decimal.Decimal(rec[0])):
        return -1
    return 0

def deposit(amount, acc_id, c_id, description):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_id))
        rec = cur.fetchone()
        t_type = 'Deposit'
        old_amount = rec[2]
        new_amount = old_amount + Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, acc_id))
        new_trans(t_type, amount, description,c_id,'NULL',acc_id,acc_id)
        conn.commit()
        print("Amount deposited successfully!")
        pass
        # Need to have a pause here so the user can see their ID before moving to the next screen.
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def withdraw(amount, acc_id, c_id, description):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_id))
        rec = cur.fetchone()
        t_type = 'Withdrawl'
        old_amount = rec[2]
        new_amount = old_amount - Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, acc_id))
        new_trans(t_type, amount, description, c_id, 'NULL',acc_id,acc_id)
        conn.commit()
        print("Amount withdrawn successfully!")
        pass
        # Need to have a pause here so the user can see their ID before moving to the next screen.
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def loc_transfer(acc_from_id, acc_to_id, description, c_id, amount):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_from_id))
        rec = cur.fetchone()
        t_type = 'Transfer'
        from_acc_old_amount = rec[2]
        from_acc_new_amount = from_acc_old_amount - Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(from_acc_new_amount, acc_from_id))
        conn.commit()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_to_id))
        rec2 = cur.fetchone()
        to_acc_old_amount = rec2[2]
        to_acc_new_amount = to_acc_old_amount + Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(to_acc_new_amount, acc_to_id))
        new_trans(t_type, amount, description, c_id, 'NULL',acc_from_id,acc_to_id,'T')
        conn.commit()
        print("Amount Transferred successfully!")
        pass
        # Need to have a pause here so the user can see success message before moving to the next screen.
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def ext_transfer(acc_from_id, c_id, bank, account_number, routing_number, amount, description):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_from_id))
        rec = cur.fetchone()
        t_type = 'ExtTransfer'
        from_acc_old_amount = rec[2]
        from_acc_new_amount = from_acc_old_amount - Decimal(amount.strip('"'))

        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(from_acc_new_amount, acc_from_id))
        new_ext_transfer_transaction(t_type, amount, description, c_id, 'NULL', acc_from_id, bank, account_number, routing_number)
        conn.commit()
        print("Amount Transferred successfully!")
        pass
        # Need to have a pause here so the user can see success message before moving to the next screen.
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def new_trans(t_type, amount, description, c_id, e_id,account_from_id,account_to_id,flag='T'):
    t_id = create_new_id("transactions")
    cur.execute("Insert into transactions values ('{}','{}',{},'{}','{}');".format(t_id, t_type, amount, description, c_id, e_id))
    if(flag=='T'):
        cur.execute("Insert into to_from values('{}','{}','{}');".format(t_id,account_from_id,account_to_id))
    else:
        pass
    conn.commit()


def new_transfer_transaction(t_type, amount, description, c_id, e_id, acc_from_id, acc_to_id):
    t_id = create_new_id("transactions")
    cur.execute("INSERT INTO transactions VALUES ('{}','{}',{},'{}','{}');".format(t_id, t_type, amount, description, c_id, e_id))
    cur.execute("INSERT INTO to_from VALUES('{}','{}','{}')".format(t_id, acc_from_id, acc_to_id))
    conn.commit()


def new_ext_transfer_transaction(t_type, amount, description, c_id, e_id, acc_from_id, bank, account_number, routing_number):
    t_id = create_new_id("transactions")
    cur.execute(
        "INSERT INTO transactions VALUES ('{}','{}',{},'{}','{}');".format(t_id, t_type, amount, description, c_id,
                                                                           e_id))
    cur.execute("INSERT INTO to_from_ext VALUES('{}','{}','{}','{}','{}')".format(t_id, acc_from_id, bank, account_number, routing_number))
    conn.commit()



def logo():
    # Logo
    print()
    print("__/\\\\\\\\\\\\\\\\\\\\\\\\\____/\\\\\________/\\\\\_____/\\\\\\\\\\\\\\\\\\\\\___        ")
    print(" _\/\\\\\/////////\\\\\_\/\\\\\_____/\\\\\//____/\\\\\/////////\\\\\_       ")
    print("  _\/\\\\\_______\/\\\\\_\/\\\\\__/\\\\\//______\//\\\\\______\///__      ")
    print("   _\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\__\/\\\\\\\\\\\\//\\\\\_______\////\\\\\_________     ")
    print("    _\/\\\\\/////////\\\\\_\/\\\\\//_\//\\\\\_________\////\\\\\______    ")
    print("     _\/\\\\\_______\/\\\\\_\/\\\\\____\//\\\\\___________\////\\\\\___   ")
    print("      _\/\\\\\_______\/\\\\\_\/\\\\\_____\//\\\\\___/\\\\\______\//\\\\\__  ")
    print("       _\/\\\\\\\\\\\\\\\\\\\\\\\\\/__\/\\\\\______\//\\\\\_\///\\\\\\\\\\\\\\\\\\\\\/___ ")
    print("        _\/////////////____\///________\///____\///////////_____")


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = 1
        system('clear')


while True:

    logo()
    print("\nWELCOME TO BKS BANKING APPLICATION SYSTEM")
    print("\n Customers: ")
    print("    Sign in or Sign up to get started.")
    print(" Employees: ")
    print("    Login using your employee credentials.")
    print("\n 1. Customer sign in with existing credentials")
    print(" 2. Customer sign up")
    print(" 3. Employee Login")
    print(" 4. Exit the application")
    user_in=input("\nEnter your option here: ")
    if(user_in.strip()=='1'):
        id=signin()
        cust(id)
    elif(user_in.strip()=='2'):
        id=create_new()
        if(id==-1):
            pass
        else:
            cust(id)
    elif(user_in.strip()=='3'):
        break
    elif(user_in.strip()=='4'):
        print("Please come again!")
        exit()
    else:
        print("Invalid option")

conn.close()
print("Connection closed")

# add curr balance
# add intrest function