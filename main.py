from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

app = FastAPI()

# 1. Store your assigned values exactly as provided
ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-kzxxg0ho.apps.exam.local"

# Copy the entire key including the BEGIN and END lines
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

# 2. Define the expected request body format
class TokenRequest(BaseModel):
    token: str

# 3. Create the POST /verify endpoint
@app.post("/verify")
async def verify_token(request: TokenRequest):
    try:
        # jwt.decode automatically verifies the signature, issuer, audience, and expiry all at once.
        decoded_payload = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE
        )
        
        # If decode succeeds, the token is perfectly valid
        return {
            "valid": True,
            "email": decoded_payload.get("email"),
            "sub": decoded_payload.get("sub"),
            "aud": decoded_payload.get("aud")
        }
        
    except Exception:
        # If ANY check fails (expired, wrong audience, bad signature), it jumps here
        return JSONResponse(
            status_code=401,
            content={"valid": False}
        )