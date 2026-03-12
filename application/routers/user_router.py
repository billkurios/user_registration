import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from domain.services.user_service import UserService
from domain.schemas.user import User
from application.config.container import Container
from dependency_injector.wiring import inject, Provide


logger = logging.getLogger(__name__)

user_router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={
        200: {"description": "OK"},
        204: {"description": "No content"},
        400: {"description": "Erreur sur les paramètres en entrée"},
        422: {"description": "Erreur métier lors du traitement de la donnée"},
        500: {"description": "Erreur interne"},
        502: {"description": "Erreur du service fournissant les données"},
    }
)


class UserRegisterPayload(BaseModel):
    email: EmailStr
    name: str
    password: str


# Dependency injection would be handled by container

@user_router.post("/register", response_model=User, response_model_exclude_none=False)
@inject
async def register_user(
    payload: UserRegisterPayload, user_service: UserService = Depends(Provide[Container.user_service])
) -> User:
    try:
        logger.debug("POST /user/register called", extra={"email": payload.email, "name": payload.name})
        user = await user_service.register_user(
            payload.email, payload.name, payload.password
        )
        logger.info("POST /user/register succeeded", extra={"email": user.email, "user_id": user.id})
        return user
    except ValueError as e:
        logger.warning(f"POST /user/register failed validation {payload}", extra={"email": payload.email, "error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))
