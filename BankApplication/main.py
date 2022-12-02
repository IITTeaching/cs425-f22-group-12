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
                print()
                print("New Address successfully added!")
                print()
                paused_clear()
                print()
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
        print()
        print("\nCongratulations! your account has been created successfully.")
        print()
        print("Your Customer ID is: ",c_id)
        print()
        print("Please take note of this ID as you will need it for future logins.")
        print()
        paused_clear()
        print()
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
    cur.execute("SELECT * FROM account WHERE customer_id = '{}' AND status = 'Active';".format(c_id))
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
        print(" 6.Show accounts")
        print(" 7.Show transactions")
        print(" 8.Delete account")
        print(" 9.Log out")
        print()
        choose=input("Choose an option here: ")
        # CREATING A NEW ACCOUNT
        if(choose.strip()=='1'):
            clear()
            logo()
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
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    deposit(amount, acc_id,description,c_id)
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
                        paused_clear()
                        break
                    elif (decimal.Decimal(amount) > 0):
                        print("Amount to be withdrawn cannot be $0")
                        paused_clear()
                        break
                    else:
                        description = input("Please write a short description: ")
                        withdraw(amount, acc_id,description,c_id)
                        break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break
            pass

        # INTERNAL TRANSFER
        elif(choose.strip() == '4'):
            clear()
            logo()
            print()
            print("Same bank transfer: ")
            print()
            print(" 1.Transfer funds between own accounts at the same bank")
            print(" 2.Transfer funds between different accounts at the same bank")
            print()
            transfer_type = input("Please choose an option: ")
            if (transfer_type.strip() == "1"):
                while True:
                    l = show_accounts(c_id)
                    acc_from_id = input("\nChoose the id of the account you want to transfer the money from: ")
                    l2 = show_accounts(c_id)
                    acc_to_id = input("\nChoose the id of the account you want to transfer the money to: ")
                    if (int(acc_from_id.strip()) in l and int(acc_to_id.strip()) in l2):
                        print()
                        amount = input("Please choose transfer amount: ")
                        print()
                        if (check_balance(amount, acc_from_id)):
                            print("Amount to be withdrawn greater than account balance")
                            paused_clear()
                            break
                        description = input("Please write a short description: ")
                        loc_transfer(acc_from_id, acc_to_id, description,amount,c_id)
                        break
                    else:
                        print("Invalid Id's have been entered, returning to main screen")
                        break

                pass
            elif (transfer_type.strip() == "2"):
                while True:
                    l = show_accounts(c_id)
                    acc_from_id = input("\nChoose the ID of the account you want to transfer the money from: ")
                    cur.execute("SELECT * FROM account;")
                    rec = cur.fetchall()
                    l2 = []
                    for row in rec:
                        l2.append(int(row[0]))
                    l2.sort()
                    acc_to_id = input("\nEnter the ID of the account you want to transfer the money to: ")
                    if (int(acc_from_id.strip()) in l and int(acc_to_id.strip()) in l2):
                        print()
                        amount = input("Please choose transfer amount: ")
                        print()
                        if (check_balance(amount, acc_from_id)):
                            print("Amount to be withdrawn greater than account balance")
                            paused_clear()
                            break
                        description = input("Please write a short description: ")
                        loc_transfer(acc_from_id, acc_to_id, description, amount, c_id)
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
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    ext_transfer(acc_from_id, bank, account_number, routing_number, amount, description,c_id)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break

            pass

        # VIEW ACCOUNTS
        elif(choose.strip() == '6'):
            print()
            show_accounts(c_id)
            print()
            paused_clear()
            pass

        # SHOW TRANSACTIONS
        elif (choose.strip() == '7'):
            pass

        # CLOSE ACCOUNT
        elif (choose.strip() == '8'):
            clear()
            logo()
            print()
            print("Delete Account:")
            print()
            print("Please make sure you transfer the remaining funds out of the account before closing it.")
            print()
            l = show_accounts(c_id)
            print()
            account_to_delete = input("Please choose the ID of the account you want to close: ")
            cur.execute("Select Balance from account where account_id='{}'".format(account_to_delete))
            rec = cur.fetchone()
            balance = rec[0]
            if (int(account_to_delete.strip()) in l and decimal.Decimal(balance) == 0):
                cur.execute("UPDATE account SET Status='{}' WHERE account_id='{}'".format('Closed', account_to_delete))
                conn.commit()
                clear()
                logo()
                print()
                print("Account has been deleted successfully!")
                paused_clear()
                pass
            else:
                clear()
                logo()
                print()
                print("Cannot delete account with non zero balance!")
                paused_clear()
                pass

        # LOG OUT
        elif (choose.strip() == '9'):
            print()
            print("You have been signed out")
            print()
            paused_clear()
            return

        else:
            print("Choose a valid option")
            break

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
            cur.execute("Insert into account values ({},'{}',{},{},'Active');".format(add_id, acc_type, balance, c_id))
            conn.commit()
            print()
            print("New checking account successfully created with ID: ",add_id)
            print()
            paused_clear()
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
            cur.execute("Insert into account values ({},'{}',{},{}, 'Active');".format(add_id, acc_type, balance, c_id))
            conn.commit()
            print()
            print("New saving account successfully created with ID: ",add_id)
            print()
            paused_clear()
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

def deposit(amount, acc_id,description,c_id='NULL',e_id='NULL'):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_id))
        rec = cur.fetchone()
        t_type = 'Deposit'
        old_amount = rec[2]
        new_amount = old_amount + Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, acc_id))
        new_trans(t_type, amount, description,c_id,e_id,acc_id,acc_id,new_amount)
        conn.commit()
        print()
        print("Amount deposited successfully!")
        paused_clear()
        pass
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def withdraw(amount, acc_id, description,c_id='NULL',e_id='NULL'):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_id))
        rec = cur.fetchone()
        t_type = 'Withdrawl'
        old_amount = rec[2]
        new_amount = old_amount - Decimal(amount.strip('"'))
        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, acc_id))
        new_trans(t_type, amount, description, c_id,e_id,acc_id,acc_id,new_amount)
        conn.commit()
        print()
        print("Amount withdrawn successfully!")
        print()
        paused_clear()
        pass
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def loc_transfer(acc_from_id, acc_to_id, description,amount,c_id='NULL',e_id='NULL'):
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
        new_trans(t_type, amount, description, c_id,e_id,acc_from_id,acc_to_id,from_acc_new_amount)
        conn.commit()
        print()
        print("Amount Transferred successfully!")
        print()
        paused_clear()
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def ext_transfer(acc_from_id,bank, account_number, routing_number, amount, description,c_id='NULL',e_id='NULL'):
    try:
        clear()
        logo()
        cur.execute("SELECT * FROM account WHERE account_id = '{}';".format(acc_from_id))
        rec = cur.fetchone()
        t_type = 'ExtTransfer'
        from_acc_old_amount = rec[2]
        from_acc_new_amount = from_acc_old_amount - Decimal(amount.strip('"'))

        cur.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(from_acc_new_amount, acc_from_id))
        new_ext_transfer_transaction(t_type, amount, description, c_id,e_id, acc_from_id, bank, account_number, routing_number,from_acc_new_amount)
        conn.commit()
        print()
        print("Amount Transferred successfully!")
        print()
        paused_clear()
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("try again")


def new_trans(t_type, amount, description, c_id, e_id,account_from_id,account_to_id,currbalance,flag='T'):
    t_id = create_new_id("transactions")
    cur.execute("Insert into transactions values ('{}','{}',{},'{}','{}','{}','{}');".format(t_id, t_type, amount, description, c_id, e_id,currbalance))
    if(flag=='T'):
        cur.execute("Insert into to_from values('{}','{}','{}');".format(t_id,account_from_id,account_to_id))
    else:
        pass
    conn.commit()


def new_transfer_transaction(t_type, amount, description, c_id, e_id, acc_from_id, acc_to_id,currbalance):
    t_id = create_new_id("transactions")
    cur.execute("INSERT INTO transactions VALUES ('{}','{}',{},'{}','{}');".format(t_id, t_type, amount, description, c_id, e_id,currbalance))
    cur.execute("INSERT INTO to_from VALUES('{}','{}','{}')".format(t_id, acc_from_id, acc_to_id))
    conn.commit()


def new_ext_transfer_transaction(t_type, amount, description, c_id, e_id, acc_from_id, bank, account_number, routing_number,currbalance):
    t_id = create_new_id("transactions")
    cur.execute(
        "INSERT INTO transactions VALUES ('{}','{}',{},'{}','{}','{}',{});".format(t_id, t_type, amount, description, c_id,
                                                                           e_id,currbalance))
    cur.execute("INSERT INTO to_from_ext VALUES('{}','{}','{}','{}','{}')".format(t_id, acc_from_id, bank, account_number, routing_number))
    conn.commit()



def logo():
    # Logo
    print()
    print("__/\\\\\\\\\\\\\\\\\\\\\\\\\____/\\\\\________/\\\\\_____/\\\\\\\\\\\\\\\\\\\\\___        ")
    print("__\/\\\\\/////////\\\\\_\/\\\\\_____/\\\\\//____/\\\\\/////////\\\\\_       ")
    print("___\/\\\\\_______\/\\\\\_\/\\\\\__/\\\\\//______\//\\\\\______\///__      ")
    print("____\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\__\/\\\\\\\\\\\\//\\\\\_______\////\\\\\_________     ")
    print("_____\/\\\\\/////////\\\\\_\/\\\\\//_\//\\\\\_________\////\\\\\______    ")
    print("______\/\\\\\_______\/\\\\\_\/\\\\\____\//\\\\\___________\////\\\\\___   ")
    print("_______\/\\\\\_______\/\\\\\_\/\\\\\_____\//\\\\\___/\\\\\______\//\\\\\__  ")
    print("________\/\\\\\\\\\\\\\\\\\\\\\\\\\/__\/\\\\\______\//\\\\\_\///\\\\\\\\\\\\\\\\\\\\\/___ ")
    print("_________\/////////////____\///________\///____\///////////_____")


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = 1
        system('clear')


def paused_clear():
    while True:
        trigger = input("Please press (y) to continue...")
        if (trigger.strip() == "y"):
            # for windows
            if name == 'nt':
                _ = system('cls')
                break

            # for mac and linux(here, os.name is 'posix')
            else:
                _ = 1
                system('clear')
                break
        else:
            print("Invalid option")
            print()
            paused_clear()
            pass


def emp_signin():
    clear()
    logo()
    while (True):
        print()
        print("EMPLOYEE SIGN IN")
        print()
        id = input(" Enter you ID no: ")
        pas = input(" Enter your Password: ")
        cur.execute("Select * from employee where employee_id='{}' and password='{}'".format(id.strip(), pas))
        rec = cur.fetchone()
        if (rec):
            return id.strip()
        else:
            clear()
            logo()
            print("Invalid ID or PassWord , Please Try again")
            print()

def choose_any_account():
    cur.execute("SELECT account_id,type,balance,c.name FROM account as a,customer as c where a.account_id=c.customer_id;")
    rec = cur.fetchall()
    l = []
    print()
    print("  ID.   Type       Balance")
    for row in rec:
        l.append(int(row[0]))
        if (row[1] == 'C'):
            print(" ", row[0], ".  ", "Checking  ", row[2]," Customer:",row[3])
        elif (row[1] == 'S'):
            print(" ", row[0], ".  ", "Saving    ", row[2]," Customer:",row[3])
    l.sort()
    return l;

def emp(e_id):
    cur.execute("Select name,position from employee where employee_id='{}'".format(e_id))
    rec = cur.fetchone()
    manager = False
    if (rec[1] == "Manager"):
        manager = True
    while True:
        clear()
        logo()
        print()
        print(" Welcome Back",rec[0],"   Position:",rec[1])
        print()
        print("Choose from the options below to manage or create accounts")
        print(" 1.Execute deposit from any account")
        print(" 2.Execute withdrawal from any account")
        print(" 3.Execute transfer between any two accounts")
        print(" 4.Execute external transfer between accounts and external account")
        print(" 5.View statement for an account(MANAGER ONLY)")
        print(" 6.View pending transactions for an account(MANAGER ONLY)")
        print(" 7.View account Analytics")
        print(" 8.Log out")
        print()
        choose=input("Choose an option here: ")
        if(choose.strip()=='1'):
            print()
            l=choose_any_account()
            while True:
                acc_id = input("\nChoose an account id: ")
                if (int(acc_id.strip()) in l):
                    print()
                    amount = input("Please choose deposit amount: ")
                    print()
                    if (decimal.Decimal(amount.strip()) <= 0):
                        print("Amount to be deposited is less than or equals to $0")
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    deposit(amount, acc_id,description,e_id=e_id)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    print()
                    paused_clear()
                    break
        elif(choose.strip()=='2'):
            l=choose_any_account()
            while True:
                acc_id = input("\nChoose an account id: ")
                if (int(acc_id.strip()) in l):
                    print()
                    amount = input("Please choose withdrawal amount: ")
                    print()
                    if(decimal.Decimal(amount)>=0 and check_balance(amount,acc_id)==-1):
                        print("Amount to be withdrawn greater than account balance")
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    withdraw(amount, acc_id,description,e_id=e_id)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break
        elif (choose.strip() == '3'):
            while True:
                l = choose_any_account()
                acc_from_id = input("\nChoose the id of the account you want to transfer the money from: ")
                l2 = choose_any_account()
                acc_to_id = input("\nChoose the id of the account you want to transfer the money to: ")
                if (int(acc_from_id.strip()) in l and int(acc_to_id.strip()) in l2):
                    print()
                    amount = input("Please choose transfer amount: ")
                    print()
                    if (decimal.Decimal(amount.strip())>=0 and check_balance(amount, acc_from_id)):
                        print("Amount to be withdrawn greater than account balance")
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    loc_transfer(acc_from_id, acc_to_id, description,amount,e_id=e_id)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break

        elif (choose.strip() == '4'):
            l=choose_any_account()
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
                        paused_clear()
                        break
                    description = input("Please write a short description: ")
                    ext_transfer(acc_from_id, bank, account_number, routing_number, amount, description,e_id=e_id)
                    break
                else:
                    print("Invalid Id's have been entered, returning to main screen")
                    break
        elif (choose.strip() == '5'):
            pass
        elif (choose.strip() == '6'):
            pass
        elif(choose.strip()=='7'):
            pass
        elif (choose.strip() == '8'):
            print("LOGGING OUT...")
            break
        else:
            print("Invalid option")
            print()
            paused_clear()

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
        id=emp_signin()
        emp(id)
    elif(user_in.strip()=='4'):
        print("Please come again!")
        exit()
    else:
        print("Invalid option")
        print()
        paused_clear()

conn.close()
print("Connection closed")

## delete account option
## check if account balance is 0 before deleting the account