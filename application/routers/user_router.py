from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from domain.services.user_service import UserService
from domain.schemas.user import User
from application.config.container import Container
from dependency_injector.wiring import inject, Provide

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


class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str


# Dependency injection would be handled by container

@user_router.post("/register", response_model=User, response_model_exclude_none=False)
@inject
async def register_user(
    request: UserCreateRequest, user_service: UserService = Depends(Provide[Container.user_service])
) -> User:
    try:
        user = await user_service.register_user(
            request.email, request.name, request.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
