from dependency_injector import containers, providers
from domain.services.user_service import UserService
from infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from infrastructure.database_pool import DatabasePool


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    Manages the lifecycle and dependencies of services, repositories, and resources.
    """

    # Configures automatic dependency injection wiring for the routers package
    wiring_config = containers.WiringConfiguration(packages=["application.routers"])

    # Database connection pool factory: instance created on demand
    db_pool = providers.Factory(DatabasePool)

    # Singleton instance of the in-memory user repository
    user_repository = providers.Singleton(InMemoryUserRepository)

    # Singleton instance of the user service, injected with the user repository
    user_service = providers.Singleton(UserService, user_repo=user_repository)
