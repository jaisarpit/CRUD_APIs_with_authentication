from fastapi import Body, FastAPI, Response , status, HTTPException , Depends , APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database , schemas , utils, models, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    
    #{                                     Auth2PasswordRequestForm has by default these 2 fields
    #   username :
    #   password :   
    # }

    user = db.query(models.User).filter( models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token({"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"} 

