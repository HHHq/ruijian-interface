import pymysql

"""
链接mysql
"""
class DbHandler:
    # 初始化一个链接，游标
    def __init__(self, database, host, user, password, port):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    port=port,
                                    database=database,
                                    )
        self.cursor = self.conn.cursor()

    def query(self, db_sql, one=True):
        # 提交实务，更新数据
        self.conn.commit()
        # 执行查询语句
        self.cursor.execute(db_sql)
        # 查询数据
        if one:
            query_data = self.cursor.fetchone()
            return query_data
        query_data = self.cursor.fetchall()
        return query_data

    def close(self):
        # 关闭游标，链接
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = DbHandler(host='111.230.187.251',
                   user='root',
                   password='Mysql4zy',
                   port=58220,
                   database="db_datastory_authority"
                   )

    db_sql = "SELECT user_email from t_auth_authorizable_role "
    query_data = db.query(db_sql,one=True)


