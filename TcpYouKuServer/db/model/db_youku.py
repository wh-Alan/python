# Author: Alan
import pymysql
from conf import settings

def mysql_db(sql,sql_l,action='query_all',num=1):
    '''数据库操作'''
    db_conn = pymysql.connect(
        host=settings.DB_host,
        port=settings.DB_port,
        user=settings.DB_user,
        password=settings.DB_password,
        db=settings.DB_db
    )
    cursor = db_conn.cursor()
    def save():
       try:
           res=cursor.execute(sql,sql_l)
           db_conn.commit()
       except Exception as e:
           print(e)
           res=False
       return res

    def query_one():

        print(sql,sql_l)
        cursor.execute(sql, sql_l)
        res=cursor.fetchall()
        print(11,res)
        return res
    def query_all():
        cursor.execute(sql, sql_l)
        res=cursor.fetchall()
        return res
    def query_many():
        cursor.execute(sql, sql_l)
        res=cursor.fetchmany(num)
        return res
    action_dict={
        'save':save,
        'query_one':query_one,
        'query_all':query_all,
        'query_many':query_many,
    }
    db_conn.close()
    return action_dict[action]()
