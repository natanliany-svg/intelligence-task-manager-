from fastapi import FastAPI
from database.db_connection import DB_connection 
import uvicorn
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router
app = FastAPI()
db = DB_connection()


# cre_mission = create_mission()

db.create_tabels()

app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)






if __name__ == "__main__":
    uvicorn.run("main:app" , host= "127.0.0.1" , port= 3306, reload=True)

    

    db_mang = DB_connection()
    db_mang.create_datbase()
    db_mang.create_tabels()
    
    print("The data and tables are working successfully")

