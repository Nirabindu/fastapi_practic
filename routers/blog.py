from fastapi import HTTPException, APIRouter, Depends, status, Request, responses
from sqlalchemy.orm import Session
from sql_app import schemas, models, database
from datetime import datetime
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from security import oauth2
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["blogs"])

templates = Jinja2Templates(directory="templates")


@router.get("/create_blog")
def create_blog(request: Request):
    return templates.TemplateResponse("create_blog.html", {"request": request})


@router.post("/create_blog")
async def blog(request: Request, db: Session = Depends(database.get_db)):

    form = await request.form()
    title = form.get("title")
    description = form.get("description")

    errors = []

    if not title or len(title) < 5:
        errors.append("title should be greater then 5 charecter")
        return templates.TemplateResponse(
            "create_blog.html", {"request": request, "errors": errors}
        )
    if not description or len(description) < 10:
        errors.append("description should be greater then 20 charecter")
        return templates.TemplateResponse(
            "create_blog.html", {"request": request, "errors": errors}
        )
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return responses.RedirectResponse(
                "/?msg=you are not logged in login fast",
                status_code=status.HTTP_302_FOUND,
            )
        else:
            # partition method of string
            scheme, _, param = token.partition(
                " "
            )  # from token scheme = bearer and param = token data

            get_user = oauth2.get_current_user(param)
            check_user = (
                db.query(models.User).filter(models.User.email == get_user).first()
            )

            if not check_user:
                errors.append("invalid user details")
            else:
                date_posted = datetime.now().date()
                create_blg = models.Blog(
                    title=title,
                    description=description,
                    date=date_posted,
                    id=check_user.id,
                )
                db.add(create_blg)
                db.commit()
                db.refresh(create_blg)
                return responses.RedirectResponse(
                    "/?msg=blog posted",
                    status_code=status.HTTP_302_FOUND,
                )

    except Exception as e:

        errors.append("Something wrong")


@router.get("/blog_posted")
def blog_by_owner(request: Request, db: Session = Depends(database.get_db)):
    errors = []
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return responses.RedirectResponse(
                "/user_login?msg=you are not logged in login fast",
                status_code=status.HTTP_302_FOUND,
            )
        else:
            scheme, _, param = token.partition(" ")
            get_user = oauth2.get_current_user(param)
            check_user = (
                db.query(models.User).filter(models.User.email == get_user).first()
            )
            if not check_user:
                return responses.RedirectResponse("/user_register")
            else:
                get_blog = (
                    db.query(models.Blog).filter(models.Blog.id == check_user.id).all()
                )
                return templates.TemplateResponse(
                    "won_blog.html",
                    {"request": request, "errors": errors, "blogs": get_blog},
                )
    except Exception as e:
        print("somthing wrong with get blogs")


    



@router.delete("/delete_blog/{blog_id}")
def del_blog(request: Request, blog_id: int, db: Session = Depends(database.get_db)):
    errors = []
    try:
        token = request.cookies.get("access_token")
        if not token:
            return responses.RedirectResponse(
                "/user_login?msg=login fast", status_code=status.HTTP_302_FOUND
            )
        else:
            scheme, _, param = token.partition(" ")
            get_user = oauth2.get_current_user(param)
            current_user = (
                db.query(models.User).filter(models.User.email == get_user).first()
            )
            if not current_user:
                errors.append("user not found")
                return responses.RedirectResponse(
                    "/user_login?msg=login fast", status_code=status.HTTP_302_FOUND
                )
            else:
                get_blog = (
                    db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
                )
                if not get_blog:
                    errors.append("blog not found")
                    return templates.TemplateResponse(
                        ("card_for_won_blog.html", {"request": request, "errors": errors})
                    )
                else:
                    db.delete(get_blog)
                    db.commit()
    except Exception as e:
        print("somthing wrong")


# @router.get("/get_blog", response_model=List[schemas.Blog])
# def get_blog(
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User_login = Depends(oauth2.get_current_user),
# ):

#     get_id = db.query(models.User).filter(models.User.email == current_user).first()
#     get_blogs = db.query(models.Blog).filter(models.Blog.id == get_id.id).all()
#     return get_blogs


# @router.get("/get_blog_details/{blog_id}")
# def get_blog_details(blog_id: int, db: Session = Depends(database.get_db)):
#     get_blog_in_details = (
#         db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
#     )
#     if not get_blog_in_details:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"id {blog_id} not found"
#         )

#     return get_blog_in_details




@router.get('/update_blog/{blog_id}')
def del_blog(blog_id:int, request:Request,db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    return templates.TemplateResponse('update_blog.html',{'request':request,'blogs':blogs})




@router.put("/update_blog/{blog_id}")
def update_blog(
    blog_id: int,
    request:Request,
    data:schemas.Blog,
    db: Session = Depends(database.get_db),
):
    # form = await request.form()
    # title = form.get("title")
    # description = form.get("description")
    # print(title,description)
    errors =[]
    try:
        token = request.cookies.get('access_token')
        if not token:
            return responses.RedirectResponse(
                "/user_login?msg=you are not logged in login fast",
                status_code=status.HTTP_302_FOUND,
            )
        else:
            scheme ,_,param = token.partition(' ')
            get_user = oauth2.get_current_user(param)
            if not get_user:
                errors.append('user not found')
            else:
                verify_user = db.query(models.User).filter(models.User.email == get_user).filter()
                if  not verify_user:
                    errors.append('user not found please login again')
                else:
                    date = datetime.now().date()
                    get_blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
                    get_blog.title = data.title
                    get_blog.description = data.description
                    get_blog.date = date
                    db.commit()
                    db.refresh(get_blog)
                    return {'msg':'blog update success'}
                    
    except Exception as e:
        print('none')



# existing_item.first().owner_id == user.id  we can do in this way also


@router.get('/auto_complete')
#term should be used cant any other variable name
def autocomplete(term:Optional[str],db:Session=Depends(database.get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.title.contains(term)).all()
    suggestion=[]
    for blog in blogs:
        suggestion.append(blog.title)
    return  suggestion  

@router.get('/search')
def search(request:Request,query:Optional[str] ,db:Session=Depends(database.get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.title.ilike(f'%{query}%')).all()
    if blogs:
        return templates.TemplateResponse('home.html',{'request':request,'blogs':blogs})
    else:
        errors='nothing found' 
        return templates.TemplateResponse('home.html',{'request':request,'errors':errors})   

 