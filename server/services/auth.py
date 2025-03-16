from uuid import uuid4
from server.ports.users import Users
from server.ports.credentials import Secret
from server.ports.claims import Authority
from server.ports.tokens import Token, Tokens

class Unauthorized(Exception):
    """
    Exception raised when authentication fails, indicating the user is unauthorized due to 
    invalid credentials.
    """

class Auth:
    """
    Handles authentication, authorization and registration in a single place.

    While authentication and authorization are distinct concepts, this service combines them for simplicity
    as this server is intended for personal use only and is not meant to be deployed publicly. 
    """ 
    def __init__(self, users: Users, authority: Authority, tokens: Tokens):
        self.users = users
        self.authority = authority
        self.tokens = tokens

    def handle(self, username: Secret, password: Secret) -> Token:
        """
        Handles authentication and authorization of an User. If not user is found
        it registers one and authorize it. 

        This is for personal usage only and is not secure for production.

        Args:
            username (Secret): The username of the user. 
            password (Secret): The password of a user.

        Raises:
            Unauthorized: An exception when the passwords do not match.

        Returns:
            Token: An access token according to OAuth specifications.
        """
        user = self.users.read(by='credentials', username=username)
        if not user:
            user = self.users.create(id=uuid4())
            user.credentials.add(username, password)

        elif not user.credentials.verify(username, password):
            raise Unauthorized
        
        claims = self.authority.sign(user)
        return self.tokens.issue(claims)