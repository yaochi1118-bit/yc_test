import mysql.connector
from mysql.connector import Error
import json
import os

# ========== 配置文件路径设置 ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def load_mysql_config():
    """从配置文件加载MySQL连接配置"""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config


def connect_mysql():
    """连接本地MySQL数据库"""
    # ========== 加载配置 ==========
    config = load_mysql_config()
    database_name = config.get("database")
    
    try:
        connection = mysql.connector.connect(
            host=config.get("host", "localhost"),
            port=config.get("port", 3306),
            user=config.get("user"),
            password=config.get("password"),
            database=database_name
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
            
            # 统计每个表的数据条数
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\n表名                      数据条数")
            print("-" * 35)
            total_count = 0
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`;")
                count = cursor.fetchone()[0]
                total_count += count
                print(f"{table_name:<24} {count}")
            print("-" * 35)
            print(f"总计: {total_count}")
            
            return connection
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    conn = connect_mysql()
