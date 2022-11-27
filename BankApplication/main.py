import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="project",
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
    cur.execute("Select branch_id,state,zip from branch natural join address;")
    rec = cur.fetchall()
    l =[]
    for row in rec:
        l.append(int(row[0]))
        print(row[0], ".", row[1], row[2])
    l.sort()
    while True:
        add_id = input("Choose an Home branch:")
        if (int(add_id.strip()) <= len(l) and int(add_id.strip()) > 0):
            return add_id
        else:
            print("invalid")

def choose_ad():
    print()
    print("1.Choose from exisiting address")
    print("2.Create new address")
    print("Click on anything else to return to main screen")
    user=input("Choose an option:")
    if(user.strip()=='1'):
        cur.execute("Select * from address;")
        rec=cur.fetchall()
        l=[]
        for row in rec:
            l.append(int(row[0]))
            print(row[0],".",row[1],row[2],row[3])
        l.sort()
        while True:
            add_id=input("Choose an address id:")
            if(int(add_id.strip())<=len(l) and int(add_id.strip())>0):
                return add_id
            else:
                print("invalid")
    elif(user.strip()=='2'):
        while True:
            try:
                city=input("Enter Name of city:")
                state=input("Enter Name of state")
                zip=input("Enter zip")
                add_id=create_new_id('address')
                cur.execute("Insert into address values ({},'{}','{}','{}');".format(add_id,city,state,zip))
                conn.commit()
                print("New Address succesfully added")
                return add_id
            except(Exception, psycopg2.DatabaseError) as e:
                print("eeror:",e)
                print("try again")
    else:
        return -1
def create_new():
    try:
        print()
        print("Hello There!")
        print("I will guide you to create your own BKS account")
        name=input("Please Enter your name:")
        print("Choose an address")
        add_id=choose_ad()
        if(add_id==-1):
            return -1
        b_id=choose_b()
        c_id=create_new_id("customer")
        password=input("Please enter a pass word to keep your account secure(less than 8 digit):")
        cur.execute("insert into customer values({},'{}','{}','{}','{}');".format(c_id,name,b_id,add_id,password))
        conn.commit()
        print("Your account has been created successfully")
        return c_id
    except(Exception, psycopg2.DatabaseError) as e:
        print("eeror:",e)
        print("Please Try again")

def signin():
    print("SIGN IN")
    uiuuuuuuuuuuuuuuuuuuuu
# this is the function for the customer interface
def cust(id):
    pass

while True:
    print("WELCOME TO BKS BANKING APPLICATION SYSTEM")
    print("Sign in or Sign up to get started or login using the employee credentials")
    print("1.Sign in with existing credentials")
    print("2.Sign up with your information here")
    print("3.Employee Login")
    print("4.Exit the application")
    user_in=input("Enter your option here:")
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


