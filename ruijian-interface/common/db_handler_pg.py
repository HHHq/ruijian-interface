"""
@Author:hq
@Date 2021/11/3 10:34
"""

"""
通过SSH通道链接pg数据库
"""

from sshtunnel import SSHTunnelForwarder
import psycopg2


class PgDbHandler():
    """
    remote_bind_address:要链接的数据库地址和端口，传入tuple
    ssh_address_or_host:传入tuple
    remote_bind_address:数据库地址,端口
    """

    def __init__(self, ssh_address_or_host, ssh_username, ssh_password, remote_bind_address
                 , database, user, password):
        self.server = SSHTunnelForwarder(ssh_address_or_host=ssh_address_or_host,
                                         ssh_username=ssh_username,
                                         ssh_password=ssh_password,
                                         remote_bind_address=remote_bind_address)
        self.server.start()
        self.conn = psycopg2.connect(host="127.0.0.1",
                                     user=user,
                                     password=password,
                                     port=self.server.local_bind_port,
                                     database=database)

        self.cursor = self.conn.cursor()

    def query(self, db_sql, one=True):

        # 执行语句
        self.cursor.execute(db_sql)
        # 提交实务，更新数据
        self.conn.commit()
        # 查询数据
        if one:
            query_data = self.cursor.fetchone()
            return query_data
        query_data = self.cursor.fetchall()
        return query_data

    def update(self, db_sql1,db_sql2):

        # 执行语句
        self.cursor.execute(db_sql1)
        self.cursor.execute(db_sql2)
        self.conn.commit()

    def close(self):
        # 关闭游标，链接，SSH通道
        self.cursor.close()
        self.conn.close()
        self.server.close()


if __name__ == '__main__':
    db = PgDbHandler(ssh_address_or_host=("mnet.datatub.com", 56000),
                     ssh_username="hequan",
                     ssh_password=r"Dstory@888",
                     remote_bind_address=("192.168.40.57", 9988),
                     database="db_datastory_channel",
                     user="mars",
                     password="YNqdJvz8rj9N7hAh")
    # db_sql1 = "update map_user_sign_area set is_del=1 where name='{}'".format("麦德龙(花都商场店)hq")
    # db_sql2 = "update map_user_sign_area_relation set is_del=1 where sign_id in(select id from map_user_sign_area where name='{}')".\
    #     format("麦德龙(花都商场店)hq")
    # db.update(db_sql1,db_sql2)
    a="select * from map_user_sign_area"
    result=db.query(a,one=False)
    print(result)
    print(len(result))
    a1="select * from map_user_sign_area"
    result1 = db.query(a, one=False)
    print(len(result1))