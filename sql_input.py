import random
import sqlite3

connection_obj=sqlite3.connect("QUESTION.db")
cursor_obj=connection_obj.cursor()


function_name="modulus"
for i in range(1,101):
    a=random.randint(1,20)
    b=random.randint(1,5)
    id=i
    pre_written_code=[f"A={a}"]
    end_written_code=[f"return A"]
    comment=f"use the modulus operator to find A modulus by {b} when A={a}"
    answer=a%b
    conditions=[b,"%"]
    print(comment,answer)
    sql_code=f"""
    INSERT INTO question (id, function_name, comments, pre_written_code, end_written_code, conditions, answer)
    VALUES ("{id}","{function_name}", "{comment}", "{pre_written_code}", "{end_written_code}", "{conditions}", "{answer}");
    """
    cursor_obj.execute(sql_code)
    connection_obj.commit()

