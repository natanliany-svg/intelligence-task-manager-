
from database.db_connection import DB_connection 

if __name__ == "__main__":
    print("Starting system initialization...")
    

    db_mang = DB_connection()
    db_mang.create_datbase()
    db_mang.create_tabels()
    
    print("The data and tables are working successfully")

