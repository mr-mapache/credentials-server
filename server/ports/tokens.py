from typing import Protocol   
from typing import Optional
from datetime import datetime 
from server.ports.claims import Claims

class Headers(Protocol):
    """
    Represents the headers in a JSON Web Token (JWT) as defined by the JOSE 
    (JSON Object Signing and Encryption) Header specification.
    
    The headers typically include information about the cryptographic 
    operations applied to the JWT, and optionally, additional properties 
    like the type of the JWT (typ) and content type (cty). The handling of 
    these headers depends on whether the JWT is a JWS (JSON Web Signature) 
    or JWE (JSON Web Encryption).
    """
    
    alg: str
    """
    The "alg" (algorithm) header parameter identifies the algorithm used 
    to sign or encrypt the JWT. This is a required field and must be a 
    string representing the algorithm used (e.g., "HS256", "RS256").
    JWT implementations MUST process this parameter to determine the 
    cryptographic operations to apply to the JWT.
    """
    
    typ: Optional[str] = None
    """
    The "typ" (type) header parameter indicates the media type of the JWT. 
    Its value is typically "JWT", but applications can use it to declare 
    other media types if necessary. The "typ" parameter is used for 
    disambiguation when multiple types of objects might be present in an 
    application data structure. While it is generally optional, it is 
    recommended to use "JWT" (in uppercase) if the object is a JWT. 
    JWT implementations ignore this parameter; it is handled by the JWT 
    application.
    """
    
    cty: Optional[str] = None
    """
    The "cty" (content type) header parameter indicates the structure of 
    the JWT when nested signing or encryption operations are employed. 
    If nested JWTs are not used, this parameter is not recommended. However, 
    if a nested JWT is present (e.g., in the case of nested signing or 
    encryption), the "cty" parameter MUST be included, and its value 
    MUST be "JWT". This ensures the JWT structure is correctly recognized 
    as a nested JWT.
    """

class Token(Protocol):
    payload: str
    expires_at: datetime


class Tokens(Protocol):
    ...

    def issue(self, claims: Claims) -> Token:
        ...
 