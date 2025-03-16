from uuid import UUID
from typing import Protocol
from typing import Optional
from server.ports.credentials import Credentials
from server.ports.tokens import Claims
 
class User(Protocol):
    """
    Represents a principal in the authentication system and serves as the Aggregate Root
    of the authentication bounded context.
    """

    @property
    def id(self) -> UUID:
        """
        A globally unique identifier for an User entity. 

        Returns:
            UUID: The unique ID of the User. 
        """
        
    @property
    def credentials(self) -> Credentials:
        """
        The credentials data access object to authenticate an user.

        Returns:
            Credentials: _description_
        """ 

        
class Users(Protocol):

    def create(self, id: UUID) -> User:
        """
        Creates an user entry in the database and returns the
        `User` aggregate root. 

        Args:
            id (UUID): The unique identifier of the user.

        Returns:
            User: The `User` aggregate root. 
        """

    def get(self, id: UUID) -> Optional[User]:
        """
        Retrieves a `User` using it's unique identifier. 

        Args:
            id (UUID): The unique identifier of the user.

        Returns:
            Optional[User]: The retrieved `User` if any. 
        """

    def read(self, by: str, **kwargs) -> Optional[User]:
        """
        Retrieves a `User` object based on a specified identity attribute. 
        
        Args:
            by (str): The attribute used to search for the user.
            **kwargs: Optional keyword arguments used to refine or modify the query. The supported arguments depend on the implementation of the user retrieval logic and the available fields on the User model.

        Returns:
            Optional[User]: A User object if found, or None if no user matches the query.
        """

    def delete(self, id: UUID) -> None:
        """
        Deletes a user from the database given it's ID.

        Args:
            id (UUID): The user's unique ID.
        """