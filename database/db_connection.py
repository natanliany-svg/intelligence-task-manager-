
import mysql.connector

class DB_connection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.pwd = "1234"

    def get_conection(self, use_db=True):
        db = "Intelligence_db" if use_db else None
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            database=db
        )

    def create_datbase(self):
        conn = self.get_conection(use_db=False)
        curr = conn.cursor()
        curr.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        conn.commit()
        curr.close()
        conn.close()

    def create_tabels(self):
        conn = self.get_conection()
        curr = conn.cursor()
        
        curr.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            specialty VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank VARCHAR(50)
        )
        """)

        curr.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            location VARCHAR(255),
            difficulty INT,
            importance INT,
            status VARCHAR(50) DEFAULT 'NEW',
            risk_level VARCHAR(50),
            assigned_agent_id INT NULL
        )
        """)
        conn.commit()
        curr.close()
        conn.close()
        
        
        
        
        
        
        