
from fastapi import APIRouter
from database.mission_db import MissionDB
from logs.my_logger import logger

router = APIRouter(prefix="/missions")
mission_db = MissionDB()

@router.post("")
def create_mission(data: dict):
    try:
        logger.info("post /missons caled")
        logger.info("saving new misson to db")
        res = mission_db.create_mission(data)
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"create misson fail: {res.get('message')}")
            return res
        logger.info("misson created succesfuly")
        return res
    except Exception as e:
        logger.error(f"error misson: {e}")
        return {"status": "error", "message": str(e)}

@router.get("")
def get_all_missions():
    try:
        logger.info("get /missons caled")
        logger.info("feching missons")
        res = mission_db.get_all_missions()
        logger.info("feched all missons")
        return res
    except Exception as e:
        logger.error(f"get missons error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/{id}")
def get_mission(id: int):
    try:
        logger.info(f"get misson {id}")
        logger.info("feching one misson")
        res = mission_db.get_mission_by_id(id)
        logger.info("got the misson")
        return res
    except Exception as e:
        logger.error(f"get misson error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    try:
        logger.info(f"asign misson {id} to agent {agent_id}")
        logger.info("checking rules and updating db")
        res = mission_db.assign_mission(id, agent_id)
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"asign faild: {res.get('message')}")
            return res
        logger.info("misson asigned ok")
        return res
    except Exception as e:
        logger.error(f"asign error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/start")
def start_mission(id: int):
    try:
        logger.info(f"start misson {id}")
        logger.info("change status to IN_PROGRESS")
        res = mission_db.update_mission_status(id, "IN_PROGRESS")
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"start faild: {res.get('message')}")
            return res
        logger.info("misson started")
        return res
    except Exception as e:
        logger.error(f"start error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/complete")
def complete_mission(id: int):
    try:
        logger.info(f"complete misson {id}")
        logger.info("change status to COMPLETED")
        res = mission_db.update_mission_status(id, "COMPLETED")
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"complete fail: {res.get('message')}")
            return res
        logger.info("misson completed")
        return res
    except Exception as e:
        logger.error(f"complete error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/fail")
def fail_mission(id: int):
    try:
        logger.info(f"fail misson {id}")
        logger.info("change status to FAILED")
        res = mission_db.update_mission_status(id, "FAILED")
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"fail updating: {res.get('message')}")
            return res
        logger.info("misson faild update")
        return res
    except Exception as e:
        logger.error(f"fail status error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    try:
        logger.info(f"cancel misson {id}")
        logger.info("change status to CANCELLED")
        res = mission_db.update_mission_status(id, "CANCELLED")
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"cancel fail: {res.get('message')}")
            return res
        logger.info("misson canceled")
        return res
    except Exception as e:
        logger.error(f"cancel error: {e}")
        return {"status": "error", "message": str(e)}
