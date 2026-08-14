from typing import Annotated
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from app.core.config import settings
from sqlmodel import Session, text
from app import models
from app.users.router import router as users_router


from app.core.database import engine


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

app.include_router(users_router)

# @app.get("/")
# async def read_root():
#     # return {"Hello": "FastAPI"}
#     result = '';
#     with Session(engine) as session:
#         result = session.exec(text("SELECT 1"))
#         print(result.one())

#     return {
#         "app_name": settings.app_name,
#         "app_version": settings.app_version,
#         "db_url": settings.database_url,
#     }


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}
