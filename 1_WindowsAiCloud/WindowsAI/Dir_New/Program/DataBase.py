import mysql.connector


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def create_table(self):
        self.connect()
        # id 自增变量，记录统计任务条数
        # task_name 任务名称，如关闭用户帐户控制
        # task_defines 任务定义，如文件名，路径
        # keyword 关键字，即这个页面中关键匹配文字
        # action 需要执行的操作，给一个输出控制即可，通过函数具象化操作，如 输入下_输入下_输入下（依靠下划线分割）
        # finish 是否是最后一步操作，1表示是，0表示否(字符串)
        # 注意最后一个是没有逗号的
        #  task_defines TEXT, 后期考虑
        create_table_query = """
        CREATE TABLE tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_name TEXT,
            keyword TEXT,
            action TEXT
        )
        """
        self.cursor.execute(create_table_query)
        self.disconnect()

    def insert(self, task_name, keyword, action):
        self.connect()
        insert_query = "INSERT INTO tasks (task_name, keyword, action) VALUES (%s, %s, %s)"
        self.cursor.execute(insert_query, (task_name, keyword, action))
        self.connection.commit()
        self.disconnect()

    def query_all_tasks(self):
        self.connect()
        query = "SELECT * FROM tasks"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.disconnect()
        return result

    def drop_table(self, table_name):
        self.connect()
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(drop_table_query)
        self.connection.commit()
        self.disconnect()

    def find_tasks_by_task(self, task):
        self.connect()
        # 先进行通用检索 通用检测
        search_query_pre = "SELECT * FROM tasks WHERE task_name = '通用检测'"
        self.cursor.execute(search_query_pre)
        result_pre = self.cursor.fetchall()
        search_query = "SELECT * FROM tasks WHERE task_name = %s"
        self.cursor.execute(search_query, (task,))
        result = self.cursor.fetchall()
        self.disconnect()
        result_pre.extend(result)
        return result_pre
