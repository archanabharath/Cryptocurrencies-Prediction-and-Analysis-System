import sqlite3

def create_table():

    conn.execute("DROP TABLE USERLOGIN")
    create_query = "CREATE TABLE USERLOGIN " \
                   "(" \
                   "UID INT NOT NULL UNIQUE," \
                   "U_FNAME TEXT NOT NULL," \
                   "U_LNAME TEXT NOT NULL," \
                   "U_EMAIL TEXT NOT NULL," \
                   "U_PHONE TEXT NOT NULL," \
                   "U_USERNAME TEXT NOT NULL," \
                   "U_PIN TEXT NOT NULL" \
                   ");"

    execute_query(create_query)

    conn.commit()


def insert_into_table(register_list):

    cursor_c1 = conn.execute("SELECT * FROM USERLOGIN").fetchall()
    if cursor_c1.__len__() > 0 :
        last_row_id = cursor_c1[cursor_c1.__len__() - 1][0]
        uid = last_row_id + 1
    else:
        uid = 1

    userpin = str(register_list[5])

    insert_query = "INSERT INTO USERLOGIN (UID,U_FNAME,U_LNAME,U_EMAIL,U_PHONE,U_USERNAME,U_PIN) VALUES ("+str(uid)+',"'+register_list[0]+'","'\
                       +register_list[1]+'","'+\
                        register_list[2]+'","'+\
                        register_list[3]+'","'+\
                        register_list[4]+'","'+\
                        userpin+'");'



    execute_query(insert_query)

    conn.commit()


def get_pin_to_match(gui_username,gui_pin):

    read_query = "SELECT U_PIN FROM USERLOGIN WHERE U_USERNAME = "+'"' + str(gui_username)+'"'

    if gui_pin == conn.execute(read_query).fetchone()[0]:
        return True


def check_username(gui_username):

    u_read_query = "SELECT U_PIN FROM USERLOGIN WHERE U_USERNAME = "+'"' + str(gui_username)+'"'

    user_nm = conn.execute(u_read_query).fetchone()

    if user_nm is not None:
        return True


def execute_query(query):

    try:
        conn.execute(query)

    except sqlite3.Error as er:
        print(er)

def read_table():

    read_query = "SELECT * FROM USERLOGIN"
    cursor1 = conn.execute(read_query).fetchone()
    print(cursor1)
    #return cursor1

# Open database connection

conn = sqlite3.connect('users.db')
print("Opened database successfully");

#create_table()
#insert_into_table()
#read_table()




