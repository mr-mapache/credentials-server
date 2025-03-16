from typing import Any
from typing import Protocol  
from typing import Optional 
from typing import Optional 

class Claims(Protocol):
    """
    Represents the claims in a JSON Web Token (JWT).
    
    This class outlines the optional claims that can be included in a JWT,
    as defined by the IANA "JSON Web Token Claims" registry. The claims provide
    information about the token, such as its issuer, subject, audience, and 
    expiration time. Each claim has different processing rules depending on 
    the application.
    """
    
    iss: Optional[str] = None
    """
    The "iss" (Issuer) claim identifies the principal that issued the JWT.
    The value is a case-sensitive string containing a String value.
    Use of this claim is optional and its processing is generally application-specific.
    """
    
    sub: Optional[str] = None
    """
    The "sub" (Subject) claim identifies the principal that is the subject of the JWT.
    This value MUST either be scoped to be locally unique in the context of the issuer
    or be globally unique. The value is a case-sensitive string containing a String value.
    Use of this claim is optional and its processing is generally application-specific.
    """
    
    aud: Optional[str] = None
    """
    The "aud" (Audience) claim identifies the recipients that the JWT is intended for.
    It is either a single case-sensitive string or an array of strings (String).
    The processing principal MUST identify itself with a value in the "aud" claim to process the JWT.
    Use of this claim is optional.
    """
    
    exp: Optional[int] = None
    """
    The "exp" (Expiration Time) claim identifies the expiration time, after which the JWT
    MUST NOT be accepted for processing. Its value is a NumericDate representing 
    the expiration timestamp. Implementers MAY allow some leeway for clock skew.
    Use of this claim is optional.
    """
    
    nbf: Optional[int] = None
    """
    The "nbf" (Not Before) claim identifies the time before which the JWT MUST NOT
    be accepted for processing. Its value is a NumericDate representing the not-before timestamp.
    Implementers MAY allow some leeway for clock skew.
    Use of this claim is optional.
    """
    
    iat: Optional[str] = None
    """
    The "iat" (Issued At) claim identifies the time at which the JWT was issued.
    This claim can be used to determine the age of the JWT. Its value is a NumericDate 
    in string format representing the issued timestamp.
    Use of this claim is optional.
    """
    
    jti: Optional[str] = None
    """
    The "jti" (JWT ID) claim provides a unique identifier for the JWT. The value 
    MUST be unique and collision-free across different issuers. It is used to prevent JWT 
    replay attacks. Its value is a case-sensitive string.
    Use of this claim is optional.
    """


class Subject(Protocol): 
    """
    A subject to be authenticated in the system. 
    """
    id: Any



class Authority(Protocol):
    """
    An authority is an entity or system responsible for issuing and attesting to the validity
    of claims and thereby asserts their authenticity. The authority's signature serves as a trust 
    mechanism, enabling other systems to verify the claims' integrity and truthfulness. Verification 
    is achieved when the system reading the claims successfully validates the authority's signature, 
    confirming that the claims originate from a recognized and trusted source.
    """

    def sign(self, subject: Subject) -> Claims:
        """
        Signs a set of claims associated with a given subject, asserting their validity.

        Parameters:
            subject (Subject): The entity whose claims are being signed.

        Returns:
            Claims: A signed set of claims that can be verified by other systems.
        """