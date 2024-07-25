from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    reward_requested = Column(Boolean, default=False)
    wallet_address = Column(String, unique=True, nullable=True)

    requests = relationship("RequestModel", back_populates="user")


class AgentModel(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    working_branch = Column(String)
    responsible_area = Column(String)

    requests = relationship("RequestModel", back_populates="agent")


# The only way I could avoid circular dependency issues between the
# RequestModel and the UserModel was to put them in the same file in this way.
# I couldn't find a better fix to the issue yet, but will keep looking.
# But for the time being, if you want to actually retrieve user_requests,
# you need to leave this class here
# - Christian
class RequestModel(Base):
    __tablename__ = "user_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user_address = Column(String, index=True)
    approval_status = Column(String)
    rejection_reason = Column(String)
    date_requested = Column(TIMESTAMP)
    installation_type = Column(String)
    image_hashes = Column(ARRAY(String))
    agent_id = Column(Integer, ForeignKey("agents.agent_id"))
    date_approved = Column(String)
    date_rejected = Column(String)


    user = relationship("UserModel", back_populates="requests")
    agent = relationship("AgentModel", back_populates="requests")
    measures = relationship("MeasureModel", back_populates="request")


class MeasureModel(Base):
    __tablename__ = "measures"

    measure_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("user_requests.request_id"))
    measure_type = Column(String)
    measure_value = Column(String)

    request = relationship("RequestModel", back_populates="measures")
