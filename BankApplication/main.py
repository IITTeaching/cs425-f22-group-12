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
    finally:
        if conn is not None:
            conn.close()
            print("Connection closed")


