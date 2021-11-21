from fastapi import APIRouter,Request,Depends,HTTPException,status
from fastapi.templating import Jinja2Templates
from sql_app import database,schemas,models
from sqlalchemy.orm import Session

# we are not showing it in swagger ui
router = APIRouter(include_in_schema=False) 

templates = Jinja2Templates(directory='templates')

@router.get("/")
def home(request:Request,db:Session = Depends(database.get_db),msg:str=None ):
    blogs = db.query(models.Blog).all()
    return templates.TemplateResponse('home.html',{'request':request,"blogs":blogs,'msg':msg})

@router.get('/details/{id}')
def blog_details(request:Request,id:int,db:Session=Depends(database.get_db)):
    blog_details = db.query(models.Blog).filter(models.Blog.blog_id == id).first()
    if not blog_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} not found')
    user = db.query(models.User).filter(models.User.id == blog_details.id).first()
    return templates.TemplateResponse('blog_details.html',{'request':request,'blog_details':blog_details,'user':user})