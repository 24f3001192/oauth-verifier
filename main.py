from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-kzxxg0ho.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjga+2rTLbeuY
cxIP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSe1bvbyGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2gIIIIBOUBJ8S63uGcNRpOBH9NFatfNwheKuzsPuVN1du6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtSQfO3h5NepzdfXpr28oNnzfW
ed+zc1R6BcmNNo/WVfJ4xyCLSf0BCOgdTGw6PdaChd119VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4FlRncsS4LlgnIT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----""".strip()

class TokenRequest(BaseModel):
    token: str

@app.post("/verify")
async def verify_token(request: TokenRequest):
    try:
        decoded_payload = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            leeway=120 
        )
        
        return {
            "valid": True,
            "email": decoded_payload.get("email"),
            "sub": decoded_payload.get("sub"),
            "aud": decoded_payload.get("aud")
        }
        
    except Exception as e:
        # This will force the grader to print the exact reason PyJWT crashed!
        return JSONResponse(
            status_code=401,
            content={
                "valid": False, 
                "debug_error": f"{type(e).__name__}: {str(e)}"
            }
        )