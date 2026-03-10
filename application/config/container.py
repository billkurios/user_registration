from dependency_injector import containers, providers
from domain.services.user_service import UserService
from infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["application.routers"])

    user_repository = providers.Singleton(InMemoryUserRepository)
    user_service = providers.Singleton(UserService, user_repo=user_repository)
