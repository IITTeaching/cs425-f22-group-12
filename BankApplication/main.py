import psycopg2
from os import system, name

conn = psycopg2.connect(
    host="localhost",
    database="Bank",
    user="postgres",
    password="")
cur=conn.cursor()
def ex():
    try:
        cur.execute("insert into m values(2,'bye');")
        print("it worked")
        cur.close()
        conn.commit()
    except(Exception,psycopg2.DatabaseError) as e:
        print(e)
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
    l = []
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
        return c_id
    except(Exception, psycopg2.DatabaseError) as e:
        print("error:", e)
        print("Please Try again")
# this is the function for the customer interface


def cust(c_id):
    # retrieve all costumer info from costumer table based on the id provided.
    cur.execute("SELECT * FROM customer WHERE customer_id = {};".format(c_id))
    rec = cur.fetchall()
    info = rec.split()
    cname = info[1]
    branch = info[2]
    address = info[3]

    print("Account Type: ")
    choose_acc_type(c_id)


    pass
def choose_acc_type(c_id):
    print()
    print(" 1.Checking account")
    print(" 2.Saving account")
    print(" Press any other key to return to main screen")

    account_type = input("\nPlease enter the account type you want to create: ")
    if (account_type.strip() == '1'):
        while True:
            try:
                clear()
                logo()
                acc_type = "Checking"
                balance = 0
                add_id = create_new_id('account')
                cur.execute("Insert into account values ({},'{}','{}','{}');".format(add_id, acc_type, balance, c_id))
                conn.commit()
                print("New checking account successfully created!")
                return add_id
            except(Exception, psycopg2.DatabaseError) as e:
                print("error:", e)
                print("try again")

    elif (account_type.strip() == '2'):
        while True:
            try:
                clear()
                logo()
                acc_type = "Saving"
                balance = 0
                add_id = create_new_id('account')
                cur.execute("Insert into account values ({},'{}','{}','{}');".format(add_id, acc_type, balance, c_id))
                conn.commit()
                print("New saving account successfully created!")
                return add_id
            except(Exception, psycopg2.DatabaseError) as e:
                print("error:", e)
                print("try again")
    else:
        return -1


def transaction():
    pass


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
        _ = system('clear')


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
        break
    elif(user_in.strip()=='2'):
        id=create_new()
        if(id==-1):
            pass
        else:
            cust()
    elif(user_in.strip()=='3'):
        break
    elif(user_in.strip()=='4'):
        print("Please come again!")
        exit()
    else:
        print("Invalid option")

conn.close()
print("Connection closed")


