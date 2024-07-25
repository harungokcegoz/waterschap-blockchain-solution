from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class MeasureType(str, Enum):
    RAIN_BARREL = "Rain Barrel"
    GREEN_ROOF = "Green Roof"


class Measure(BaseModel):
    measure_type: MeasureType
    measure_value: str


class RequestBase(BaseModel):
    user_id: int
    user_address: str
    approval_status: str
    rejection_reason: Optional[str]
    date_requested: datetime
    installation_type: str
    image_hashes: List[str]
    agent_id: int
    date_approved: Optional[str]
    date_rejected: Optional[str]


# User Data Transfer Object
class UserDTO(BaseModel):
    first_name: str
    last_name: str


# Request Data Transfer Object
class RequestDTO(RequestBase):
    request_id: int
    user: UserDTO
    measures: List[Measure]


class RequestCreate(RequestBase):
    measures: List[Measure]


class RequestUpdate(RequestBase):
    pass


class ApprovalUpdate(BaseModel):
    approval_status: str
    rejection_reason: Optional[str] = None
    date_approved: Optional[str] = None
    date_rejected: Optional[str] = None


class MintRequest(BaseModel):
    user_wallet_address: str
    reward_amount: str


class Request(RequestBase):
    request_id: int

    class Config:
        from_attribute = True
