from sqlalchemy.orm import Session
from typing import List, Type
from app.models.models import AgentModel
from app.schemas.agent_schema import Agent, AgentCreate, AgentUpdate


class AgentService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_agents(self) -> list[Type[AgentModel]]:
        return self.db.query(AgentModel).all()

    def get_agent_by_id(self, agent_id: int):
        return self.db.query(AgentModel).filter(agent_id == AgentModel.agent_id).first()

    def get_agent_by_email(self, email: str):
        return self.db.query(AgentModel).filter(email == AgentModel.email).first()

    def create_agent(self, agent_data: AgentCreate):
        db_agent = AgentModel(**agent_data.dict())
        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)
        return db_agent

    def update_agent(self, agent_id: int, agent_data: AgentUpdate):
        db_agent = self.get_agent_by_id(agent_id)
        if db_agent:
            for key, value in agent_data.dict().items():
                setattr(db_agent, key, value)
            self.db.commit()
            self.db.refresh(db_agent)
        return db_agent

    def delete_agent(self, agent_id: int):
        db_agent = self.get_agent_by_id(agent_id)
        if db_agent:
            self.db.delete(db_agent)
            self.db.commit()
        return db_agent

