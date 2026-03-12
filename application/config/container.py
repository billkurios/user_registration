from dependency_injector import containers, providers
from domain.services.user_service import UserService
from infrastructure.repositories.database_user_repository import (
    DatabaseUserRepository,
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

    # Singleton instance of the database user repository
    user_repository = providers.Singleton(DatabaseUserRepository, db_pool=db_pool)

    # Singleton instance of the user service, injected with the user repository
    user_service = providers.Singleton(UserService, user_repo=user_repository)
