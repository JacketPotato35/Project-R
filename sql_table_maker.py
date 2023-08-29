import sqlite3
def clear():
    connection_obj = sqlite3.connect('QUESTION.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("""DELETE FROM question;""")
    connection_obj.commit()

ans=input("clear or create, 1/2 ")
if ans=="1":
    clear()
else:
    connection_obj = sqlite3.connect('QUESTION.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS QUESTION")
    table = """ CREATE TABLE question (
                id INT NOT NULL,
                function_name VARCHAR(64) NOT NULL,
                comments VARCHAR(64),
                pre_written_code CHARRARRAY,
                end_written_code CHARRARRAY,
                conditions CHARRARRAY,
                answer VARCHAR(64) NOT NULL
            ); """
    
    cursor_obj.execute(table)
    print("Table is Ready")
    connection_obj.close()