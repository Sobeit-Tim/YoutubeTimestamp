import pymysql


class DBQuery:
    def __init__(self):
        conn = pymysql.connect(host="localhost", user="root", password="1111", db="ytg", charset="utf8")
        curs = conn.cursor()
        
        self.conn = conn
        self.curs = curs

    def select_score(self):
        curs = self.curs
        
        sql = "select score from comment"
        curs.execute(sql)
        rows = curs.fetchall()

        return rows
    
    def select_comment(self):
        curs = self.curs

        sql = "select * from comment"
        curs.execute(sql)
        rows = curs.fetchall()

        return rows 
    
    def insert_comment(self, score, text):
        conn = self.conn
        curs = self.curs

        sql = f"insert into comment values (NULL, '{score}', '{text}')"
        curs.execute(sql)
        conn.commit()
    
    def close_db(self):
        conn = self.conn
        conn.close()