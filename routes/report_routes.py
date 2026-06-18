
from fastapi import APIRouter
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from logs.my_logger import logger

router = APIRouter(prefix="/reports")
agent_db = AgentDB()
mission_db = MissionDB()

@router.get("/summary")
def get_summary():
    try:
        logger.info("get reports summary")
        logger.info("runing multipe sql counts")
        res = {
            "active_agents_count": agent_db.count_active_agents(),
            "total_missions": mission_db.count_all_missions(),
            "open_missions": mission_db.count_open_missions(),
            "completed_missions": mission_db.count_by_status("COMPLETED"),
            "failed_missions": mission_db.count_by_status("FAILED"),
            "critical_missions": mission_db.count_critical_missions()
        }
        logger.info("summary done")
        return res
    except Exception as e:
        logger.error(f"summary error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/missions-by-status")
def get_missions_by_status():
    try:
        logger.info("get missons by status report")
        logger.info("counting misson statuses")
        res = {
            "open": mission_db.count_open_missions(),
            "in_progress": mission_db.count_by_status("IN_PROGRESS"),
            "completed": mission_db.count_by_status("COMPLETED"),
            "failed": mission_db.count_by_status("FAILED"),
            "canceled": mission_db.count_by_status("CANCELLED")
        }
        logger.info("status report done")
        return res
    except Exception as e:
        logger.error(f"status report error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/top-agent")
def top_agent():
    try:
        logger.info("get top agent report")
        logger.info("feching top agent from db")
        res = mission_db.get_top_agent()
        logger.info("top agent feched")
        return res
    except Exception as e:
        logger.error(f"top agent error: {e}")
        return {"status": "error", "message": str(e)}




