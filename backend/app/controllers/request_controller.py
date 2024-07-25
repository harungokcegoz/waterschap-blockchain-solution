from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.db.postgres import SessionLocal
from app.schemas.agent_schema import Agent
from app.schemas.request_schema import Request, RequestDTO, RequestCreate, RequestUpdate, ApprovalUpdate
from app.schemas.user_schema import User
from app.services.request_service import RequestService
from app.services.auth_service import AuthService
from app.services.agent_service import AgentService
from app.services.blockchain_service import mint_erc20_token
from app.services.user_service import UserService

router = APIRouter()
request_service = RequestService(db=SessionLocal())
agent_service = AgentService(db=SessionLocal())
user_service = UserService(db=SessionLocal())
auth_service = AuthService(db=SessionLocal())


@router.get("/requests/", response_model=List[RequestDTO])
async def get_requests():
    """Get all user requests with user's first and last name."""
    requests = request_service.get_all_requests_with_user_names()
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found")
    return requests


@router.get("/users/{user_id}/requests", response_model=List[RequestDTO])
async def get_requests_by_user_id(
        user_id: int,
        current_user: User = Depends(auth_service.get_current_active_user)
):
    """Get user requests with user's first and last name by user_id."""
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these requests")

    requests = request_service.get_requests_by_user_id(user_id)
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found")
    return requests


@router.get("/agents/{agent_id}/requests", response_model=List[RequestDTO])
async def get_requests_by_agent_id(
        agent_id: int,
        current_agent: Agent = Depends(auth_service.get_current_active_agent)
):
    """Get user requests with user's first and last name by agent_id."""
    if current_agent.agent_id != agent_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these requests")

    requests = request_service.get_requests_by_agent_id(agent_id)
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found")
    return requests


@router.get("/user/requests/{request_id}", response_model=RequestDTO)
async def get_request_detail_user(
        request_id: int,
        current_user: User = Depends(auth_service.get_current_active_user)
):
    """Get a user request by ID."""
    request = request_service.get_request_by_id(request_id)
    if current_user.user_id != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.get("/agent/requests/{request_id}", response_model=RequestDTO)
async def get_request_detail_agent(
        request_id: int,
        current_agent: Agent = Depends(auth_service.get_current_active_agent)
):
    """Get a user request by ID."""
    request = request_service.get_request_by_id(request_id)
    if current_agent.agent_id != request.agent_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.post("/requests/", response_model=RequestDTO)
async def create_request(
        request: RequestCreate,
        current_user: User = Depends(auth_service.get_current_active_user)
):
    """Create a new user request."""
    if current_user.user_id != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create a new request")

    created_request = request_service.create_request(request)
    if not created_request:
        raise HTTPException(status_code=500, detail="Error adding request to the database")
    return created_request


@router.put("/requests/{request_id}", response_model=Request)
async def update_request(request_id: int, request: RequestUpdate):
    """Update an existing user request."""
    updated_request = request_service.update_request(request_id, request)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated_request


@router.patch("/requests/{request_id}", response_model=Request)
async def update_approval_status(request_id: int, approval_update: ApprovalUpdate):
    """Update the approval status of a request."""
    updated_request = request_service.update_request_status(request_id, approval_update)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if approval_update.approval_status == 'Approved':
        request = request_service.get_request_by_id(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        reward_amount = request_service.calculate_reward_amount(request)

        user_info = user_service.get_user_by_id(updated_request.user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")

        user_wallet_address = getattr(user_info, 'wallet_address', 'Wallet address not found')
        mint_response = mint_erc20_token(user_wallet_address, str(reward_amount))

        if 'error' in mint_response:
            raise HTTPException(status_code=400, detail=mint_response)
    return updated_request


@router.delete("/requests/{request_id}", response_model=Request)
async def delete_request(request_id: int):
    """Delete a user request."""
    deleted_request = request_service.delete_request(request_id)
    if not deleted_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return deleted_request
