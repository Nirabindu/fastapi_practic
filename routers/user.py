from fastapi import APIRouter, HTTPException, Depends, status,Request,responses,Response
from sql_app import schemas, database, models
from sqlalchemy.orm import Session
from security.hashing import hash
from security import tokens
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["user_auth"])


templates = Jinja2Templates(directory='templates')

@router.get('/user_register')
def reg(request:Request):
    return templates.TemplateResponse("user_reg.html",{'request':request})



@router.post("/user_register")
async def user_reg(
    request: Request ,db: Session = Depends(database.get_db)
):
    form = await request.form()

    name = form.get('name')
    email = form.get('email')
    phone = form.get('phone')
    password = form.get('password')




    date = datetime.now().date()
    checking_existing_email = (
        db.query(models.User).filter(email == models.User.email).first()
    )

    # if len(phone) != 10:
    #     return {'status':'phone should be 10 digit'}



    checking_existing_phone = (
        db.query(models.User).filter(models.User.phone == phone).first()
    )

    if checking_existing_email:
         return templates.TemplateResponse('user_reg.html',{'request':request,'status':'email already in used'})
        # raise HTTPException(
        #     status_code=status.HTTP_226_IM_USED,
        #     detail=f"the email id {email} already in used",
        # )
    elif checking_existing_phone:
        return templates.TemplateResponse('user_reg.html',{'request':request,'status':'phone already in use'})
        # raise HTTPException(
        #     status_code=status.HTTP_226_IM_USED,
        #     detail=f"the phone {phone} already in used",
        # )
    else:
        add_user = models.User(
            name=name,
            email=email,
            phone=phone,
            password=hash.hash_password(password),
            date=date,
        )
        db.add(add_user)
        db.commit()
        db.refresh(add_user)
        return responses.RedirectResponse("/?msg=registration success",status_code=status.HTTP_302_FOUND)











@router.get('/user_login')
def reg(request:Request):
    return templates.TemplateResponse("user_log.html",{'request':request})



@router.post('/user_login')
async def user_login(request:Request,response:Response,db:Session=Depends(database.get_db)):

    form = await request.form()
    email = form.get('email')
    password = form.get('password')
    errors = []
    check_email = db.query(models.User).filter(models.User.email == email).first()
    if not check_email:
        errors.append('please enter valid email!!')
        return templates.TemplateResponse("user_log.html",{'request':request,'errors':errors})
        
    if not hash.verify_password(password,check_email.password):
        errors.append('Wrong password!!')
        return templates.TemplateResponse('user_log.html',{'request':request,'errors':errors})  
    
    access_token =  tokens.create_access_token(data={'sub':check_email.email})
    msg = 'Login successfull'
    response = templates.TemplateResponse('user_log.html',{'request':request,'msg':msg})  
    response.set_cookie(key =  "access_token", value=f'Bearer {access_token}',httponly=True )
    return response
    






#httponly means the token store into cookie but not accessible bpy any scripts




@router.delete('/dele_user/{id}')
def del_u(id:int,db:Session=Depends(database.get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    db.delete(get_user)
    db.commit()
    return{'msg':'delete success'}