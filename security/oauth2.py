from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from sql_app import database,models
from security import tokens
from jose import jwt,JWTError
from config import setting


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user_login')


def get_current_user(token:str=Depends(oauth2_scheme)):
    # credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Could not validate credential',
    # headers = {"WWW-Authenticate":"Bearer"})
    payload = jwt.decode(token,setting.SECRET_KEY,setting.ALGORITHM)
    email:str = payload.get("sub")
    if email is None:
        print('none')
    else:
        return email   
        # if not check_user:
        #     raise credential_exception
        # else:
        #     print(check_user.email)       

    # except JWTError:
    #     raise credential_exception

    
        
 
