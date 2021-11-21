from  fastapi import FastAPI
from config import setting
from sql_app import models,database
from routers import user,blog
from webapps.routers import blog as web_items
from fastapi.staticfiles import StaticFiles




app = FastAPI(title = setting.title,description = setting.description,version=setting.version)

models.Base.metadata.create_all(database.engine)

app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(web_items.router)







# alembic init migration to create alembic