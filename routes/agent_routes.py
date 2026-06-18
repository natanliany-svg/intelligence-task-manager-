
from fastapi import APIRouter

from database.agent_db import AgentDB
from logs.my_logger import logger

router = APIRouter(prefix="/agents")

agent_db = AgentDB()

@router.post("")

def create_agent(data: dict):
    try:
        logger.info("post /agents caled")
        logger.info("runing sql to create agent")
        res = agent_db.create_agent(data)
        
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"faild to create: {res.get('message')}")
            return res
        logger.info("agent created succesfuly")
        
        return res
    except Exception as e:
        logger.error(f"error in db: {e}")
        return {"status" : "error", "message": f"error: {e}"}


@router.get("")
def get_all_agents():
    try:
        logger.info("get /agents caled")
        logger.info("feching agents from db")
        res = agent_db.get_all_agents()
        logger.info("got all agnets")
        return res
    except Exception as e:
        logger.error(f"error geting agents: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/{id}")
def get_agent(id: int):
    try:
        logger.info(f"get agent {id} caled")
        logger.info("looking for agent in db")
        res = agent_db.get_agent_by_id(id)
        logger.info("agent data feched")
        return res
    except Exception as e:
        logger.error(f"error get agent: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}")
def update_agent(id: int, data: dict):
    try:
        logger.info(f"update agent {id}")
        logger.info("updating agent details")
        res = agent_db.update_agent(id, data)
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"error update: {res.get('message')}")
            return res
        logger.info("agent updated fine")
        return res
    except Exception as e:
        logger.error(f"update error: {e}")
        return {"status": "error", "message": str(e)}

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    try:
        logger.info(f"deactivate agent {id}")
        logger.info("runing deactivate sql")
        res = agent_db.deactivate_agent(id)
        if type(res) == dict and res.get("status") == "error":
            logger.error(f"cant deactivate: {res.get('message')}")
            return res
        logger.info("agent deactivated")
        return res
    except Exception as e:
        logger.error(f"deactivate error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/{id}/performance")
def get_performance(id: int):
    try:
        logger.info(f"get preformance for {id}")
        logger.info("calc preformance in db")
        res = agent_db.get_agent_performance(id)
        logger.info("preformance calc done")
        return res
    except Exception as e:
        logger.error(f"error preformance: {e}")
        # print("the p")
        return {"status": "error", "message": str(e)}




    
    
