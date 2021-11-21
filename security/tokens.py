from config import setting
from jose import jwt,JWTError
from datetime import datetime,timedelta
from sql_app import schemas



#creating token
def  create_access_token(data:dict):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes = setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,setting.SECRET_KEY,algorithm=setting.ALGORITHM)
    return encoded_jwt

# def verify_token(token:str,credentials_exception):
#     try:
#         payload = jwt.decode(token,setting.SECRET_KEY,setting.ALGORITHM)
#         user:str = payload.get("sub")
#         if user is None:
#             raise credentials_exception
#         return user   
#     except JWTError:
#         raise credentials_exception