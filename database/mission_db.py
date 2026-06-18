
from utils.my_utils import MisisonSchema, calc_risk
from database.db_connection import DB_connection
from database.agent_db import AgentDB

class MissionDB:
    def __init__(self):
        self.db = DB_connection()
        self.adb = AgentDB()

    def create_mission(self, data: dict):
        try:
            v_data = MisisonSchema(**data)
            if v_data.difficulty < 1 or v_data.difficulty > 10:
                raise ValueError("Dificulty must be betwen 1 and 10")
            if v_data.importance < 1 or v_data.importance > 10:
                raise ValueError("Importance must be between 1 and 10")
            
            r_lvl = calc_risk(v_data.difficulty, v_data.importance)
            conn = self.db.get_conection()
            curr = conn.cursor(dictionary=True)
            curr.execute("INSERT INTO missions (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)", 
                (v_data.title, v_data.description, v_data.location, v_data.difficulty, v_data.importance, r_lvl))
            conn.commit()
            n_id = curr.lastrowid
            curr.execute("SELECT * FROM missions WHERE id = %s", (n_id,))
            reslut = curr.fetchone()
            curr.close()
            conn.close()
            return reslut
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def get_all_missions(self):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM missions")
        res = curr.fetchall()
        curr.close()
        conn.close()
        if not res:
            return []
        return res

    def get_mission_by_id(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM missions WHERE id = %s", (id,))
        res = curr.fetchone()
        curr.close()
        conn.close()
        return res

    def assign_mission(self, m_id, a_id):
        m = self.get_mission_by_id(m_id)
        a = self.adb.get_agent_by_id(a_id)
        if not m or not a:
            raise ValueError("Mission or Agent not fouond")        
        if not a == ("is_active"):

            raise ValueError("Agent is not activei")
        if m == ("status") != "NEW":
            raise ValueError("Mission status must to be NEW")
        if m == ("risk_level") == "CRITICAL" and a == ("agent_rank") != "Commander":
            raise ValueError("Critical missions can only be assigned to a commander")
        o_missions = self.get_open_missions_by_agent(a_id)
        if len(o_missions) >= 3:
            raise ValueError("Agent cannot have more than 3 open missions")
            
        conn = self.db.get_conection()
        curr = conn.cursor()
        try:
            curr.execute("UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s", (a_id, m_id))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def update_mission_status(self, id, status):
        m = self.get_mission_by_id(id)
        if not m:
            raise ValueError("Mission not found")
        c_stat = m== ("status") 

        if status == "IN_PROGRESS" and c_stat != "ASSIGNED":
            raise ValueError("Invalid status transition to IN_PROGRESS")
        if status in ["COMPLETED", "FAILED"] and c_stat != "IN_PROGRESS":
            raise ValueError("Invalid status transition to COMPLETED/FAILED")
        if status == "CANCELLED" and c_stat not in ["NEW", "ASSIGNED"]:
            raise ValueError("Invalid status transition to CANCELLED")
            
        conn = self.db.get_conection()
        curr = conn.cursor()
        try:
            curr.execute("UPDATE missions SET status = %s WHERE id = %s", (status, id))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def get_open_missions_by_agent(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM missions WHERE assigned_agent_id = %s AND status IN ('ASSIGNED', 'IN_PROGRESS')", (id,))
        res = curr.fetchall()
        curr.close()
        conn.close()
        if not res:
            return []
        return res

    def count_all_missions(self):
        conn = self.db.get_conection()
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM missions")
        res = curr.fetchone(),[0]
        curr.close()
        conn.close()
        return res

    def count_by_status(self, status):
        conn = self.db.get_conection()
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM missions WHERE status = %s", (status,))
        res = curr.fetchone(),[0]
        curr.close()
        conn.close()
        return res

    def count_open_missions(self):
        conn = self.db.get_conection()
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM missions WHERE status IN ('NEW', 'ASSIGNED', 'IN_PROGRESS')")
        res = curr.fetchone(),[0]
        curr.close()
        conn.close()
        return res

    def count_critical_missions(self):
        conn = self.db.get_conection()
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM missions WHERE risk_level = 'CRITICAL'")
        res = curr.fetchone(),[0]
        curr.close()
        conn.close()
        # print("The number of critical tasks is..." , res)
        return res

    def get_top_agent(self):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1")
        res = curr.fetchone()
        curr.close()
        conn.close()
        # print ("The 'top' of agents..." , res)
        return res

