from sqlalchemy.orm import Session, joinedload
from typing import List, Type
from app.models.models import RequestModel, MeasureModel, UserModel
from app.schemas.request_schema import Request, RequestCreate, RequestUpdate, ApprovalUpdate, MeasureType

MEASURE_REWARDS = {
    "Rain Barrel": 1,  # 1 token per 10 liters
    "Green Roof": 2  # 2 tokens per square meter
}


class RequestService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_requests(self) -> List[Type[RequestModel]]:
        return self.db.query(RequestModel).all()

    def get_all_requests_with_user_names(self):
        try:
            requests = (
                self.db.query(RequestModel)
                .options(
                    joinedload(RequestModel.user)  # Load the associated user
                    .load_only(UserModel.first_name, UserModel.last_name)  # Only load first_name and last_name
                )
                .all()
            )
            self.db.commit()
            return requests
        except Exception as e:
            self.db.rollback()
            raise e

    def get_requests_by_user_id(self, user_id: int):
        return self.db.query(RequestModel).filter(user_id == RequestModel.user_id).all()

    def get_requests_by_agent_id(self, agent_id: int):
        return self.db.query(RequestModel).filter(agent_id == RequestModel.agent_id).all()

    def get_request_by_id(self, request_id: int):
        return self.db.query(RequestModel).filter(request_id == RequestModel.request_id).first()

    def create_request(self, request_data: RequestCreate):
        measures_data = request_data.measures
        del request_data.measures
        db_request = RequestModel(**request_data.dict())
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)

        for measure_data in measures_data:
            measure_type_enum = MeasureType(measure_data.measure_type)
            db_measure = MeasureModel(
                request_id=db_request.request_id,
                measure_type=measure_type_enum,
                measure_value=measure_data.measure_value
            )
            self.db.add(db_measure)
        self.db.commit()

        return db_request

    def update_request(self, request_id: int, request_data: RequestUpdate):
        db_request = self.get_request_by_id(request_id)
        if db_request:
            for key, value in request_data.dict().items():
                setattr(db_request, key, value)
            self.db.commit()
            self.db.refresh(db_request)
        return db_request

    def delete_request(self, request_id: int):
        db_request = self.get_request_by_id(request_id)
        if db_request:
            self.db.delete(db_request)
            self.db.commit()
        return db_request

    def update_request_status(self, request_id: int, approval_update: ApprovalUpdate):
        db_request = self.get_request_by_id(request_id)
        if db_request:
            db_request.approval_status = approval_update.approval_status
            if hasattr(approval_update, "rejection_reason"):
                db_request.rejection_reason = approval_update.rejection_reason
            if hasattr(approval_update, "date_approved"):
                db_request.date_approved = approval_update.date_approved
            if hasattr(approval_update, "date_rejected"):
                db_request.date_rejected = approval_update.date_rejected
            self.db.commit()
            self.db.refresh(db_request)
        return db_request

    @staticmethod
    def calculate_reward_amount(request: RequestModel) -> int:
        total_reward = 0
        for measure in request.measures:
            measure_type = measure.measure_type
            measure_value = int(measure.measure_value)
            if measure_type in MEASURE_REWARDS:
                reward_per_unit = MEASURE_REWARDS[measure_type]
                total_reward += measure_value // 10 * reward_per_unit
        return total_reward
