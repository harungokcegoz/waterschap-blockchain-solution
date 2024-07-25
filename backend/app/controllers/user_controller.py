from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Union
from starlette import status

from app.db.postgres import SessionLocal
from app.schemas.agent_schema import AgentLogin, AgentToken, Agent, AgentCreate
from app.schemas.user_schema import User, UserCreate, UserUpdate, EmailRequest, UserWalletUpdate, BlockchainDTO, \
    UserWithBalance, UserToken, TokenData
from app.services.agent_service import AgentService
from app.services.auth_service import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.user_service import UserService
from app.services.blockchain_service import get_erc20_balance

router = APIRouter()
user_service = UserService(db=SessionLocal())
agent_service = AgentService(db=SessionLocal())
auth_service = AuthService(db=SessionLocal())


@router.get("/users/", response_model=List[User])
async def get_users():
    """Get all users."""
    users = user_service.get_all_users()
    return users


@router.get("/users/{user_id}", response_model=UserWithBalance)
async def get_user(
        user_id: int,
        current_user: User = Depends(auth_service.get_current_active_user)
):
    """Get a user by ID."""
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view user info")
    user_data = user_service.get_user_by_id(user_id)
    blockchain_info = get_erc20_balance(user_data.wallet_address)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    user_data.blockchain_info = BlockchainDTO(balance=blockchain_info)
    return user_data


# TODO find a better approach for this endpoint that doesn't compromise security
@router.post("/users/get-by-email", response_model=Union[User, dict])
async def get_user_by_email(email_request: EmailRequest):
    """Get a user by email."""
    user = user_service.get_user_by_email(email_request.email)
    if not user:
        return {"found": False}
        # raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/address", response_model=str)
async def get_user_address(user_id: int):
    """Get the address of a user by ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.address


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user."""
    created_user = user_service.create_user(user)
    if not created_user:
        raise HTTPException(status_code=500, detail="Error adding user to the database")
    return created_user


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    """Update an existing user."""
    updated_user = user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.patch("/users/{user_id}/wallet", response_model=User)
async def update_user_wallet(
        user_id: int,
        userWallet: UserWalletUpdate,
        current_user: User = Depends(auth_service.get_current_active_user)
):
    """Update the wallet address of an existing user."""
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update field")
    updated_user = user_service.update_user_wallet(user_id, userWallet)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    """Delete a user."""
    deleted_user = user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user


# endpoint used to log in and receive a JWT access token
@router.post("/login", response_model=AgentToken)
async def login_for_access_token(agent_login: AgentLogin):
    agent = auth_service.authenticate_agent(agent_login.email, agent_login.password)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": str(agent.agent_id)}, expires_delta=access_token_expires
    )
    response = AgentToken(agent_id=agent.agent_id, access_token=access_token, token_type="bearer")
    return response


@router.post("/web3login", response_model=UserToken)
async def web3login_for_access_token(token_data: TokenData):
    user = auth_service.authenticate_user(token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    response = UserToken(access_token=access_token, token_type="bearer")
    return response


@router.post("/agent", response_model=Agent)
async def create_agent(agent: AgentCreate):
    """Create a new agent."""
    agent.hashed_password = auth_service.get_password_hash(agent.hashed_password)
    created_agent = agent_service.create_agent(agent)
    if not created_agent:
        raise HTTPException(status_code=500, detail="Error adding agent to the database")
    return created_agent
