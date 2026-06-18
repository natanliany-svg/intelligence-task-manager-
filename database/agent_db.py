
from utils.my_utils import AgnetSchema
from database.db_connection import DB_connection

class AgentDB:
    def __init__(self):
        self.db = DB_connection()

    def create_agent(self, data: dict):
        try:
            valid_data = AgnetSchema(**data)
            if valid_data.agent_rank not in ["Junior", "Senior", "Commander"]:
                raise ValueError("Invalid agent rank")
            
            conn = self.db.get_conection()
            curr = conn.cursor(dictionary=True)
            curr.execute("INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)", 
                (valid_data.name, valid_data.specialty, valid_data.agent_rank))
            conn.commit()
            n_id = curr.lastrowid
            curr.execute("SELECT * FROM agents WHERE id = %s", (n_id,))
            reslut = curr.fetchone()
            curr.close()
            conn.close()
            return reslut
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def get_all_agents(self):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM agents")
        res = curr.fetchall()
        curr.close()
        conn.close()
        if not res:
            return []
        return res

    def get_agent_by_id(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor(dictionary=True)
        curr.execute("SELECT * FROM agents WHERE id = %s", (id,))
        res = curr.fetchone()
        curr.close()
        conn.close()
        return res

    def update_agent(self, id, data):
        conn = self.db.get_conection()
        curr = conn.cursor()
        cols = []
        vals = []
        for k, v in data.items():
            if k != "id":
                cols.append(f"{k} = %s")
                vals.append(v)
        if not cols:
            raise ValueError("No dynamic update columns provided")
        vals.append(id)
        try:
            curr.execute(f"UPDATE agents SET {', '.join(cols)} WHERE id = %s", tuple(vals))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def deactivate_agent(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor()
        try:
            curr.execute("UPDATE agents SET is_active = FALSE WHERE id = %s", (id,))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def increment_completed(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor()
        try:
            curr.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (id,))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def increment_failed(self, id):
        conn = self.db.get_conection()
        curr = conn.cursor()
        try:
            curr.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s", (id,))
            conn.commit()
            curr.close()
            conn.close()
            return {"status": "success", "message": "Action completed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

    def get_agent_performance(self, id):
        ag = self.get_agent_by_id(id)
        if not ag:
            return None
        comp = ag,["completed_missions"] 
        fail = ag,["failed_missions"] 
        tot = comp + fail 
        
        if len(tot) > 0:
            rate  = (len(comp) / len(tot) * 100) 
        else:
            rate = 0.0 
        
        return {"completed": comp, "failed": fail, "total": tot, "success_rate": rate}

    def count_active_agents(self):
        conn = self.db.get_conection()
        curr = conn.cursor()
        curr.execute("SELECT COUNT(*) FROM agents WHERE is_active = TRUE")
        cnt = curr.fetchone(),[0] 
        conn.close()
        return cnt


