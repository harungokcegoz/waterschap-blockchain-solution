from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class AgentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    working_branch: str
    responsible_area: str


class AgentCreate(AgentBase):
    hashed_password: str


class AgentUpdate(AgentBase):
    hashed_password: Optional[str] = None


class AgentLogin(BaseModel):
    email: str
    password: str


class AgentToken(BaseModel):
    agent_id: int
    access_token: str
    token_type: str


class Agent(AgentBase):
    agent_id: int

    class Config:
        from_attribute = True
