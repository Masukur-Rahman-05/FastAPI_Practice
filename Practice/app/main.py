from fastapi import FastAPI,Form,UploadFile,File,Query,Path,Depends,Body,HTTPException,status
from enum import Enum
from pydantic import BaseModel,Field,HttpUrl
from typing import Optional,Annotated,Literal

from sqlalchemy.orm import Session
from .database import sessionLocal,engine
from .model import User,Base
from .schemas import UserCreate,UserOut,UserUpdate

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello From FastAPI"}

@app.get("/products/{product_id}")
async def get_id(product_id : float):
    return {"product_id":product_id}

class Product_Status(str,Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


@app.get("/product_status/{status}")
async def product_status(status: Product_Status):
    return {"Status":status}

@app.get("/users")
async def query_users(skip: int = 0, limit: int = 10):
    return{"skip":skip, "limit":limit}


class UserData(BaseModel):
    name:str
    age:int
    hobby:str | None

@app.post("/api/v1/json")
async def Data(data: UserData):
    return data.model_dump() # Convert Pydantic Instance to Python Dictionary for further processing


@app.post("/api/v1/form")
async def form(
    name : str = Form(...),
    age : int = Form(...),
    hobby : Optional[str] = Form(None)
):
    return {"name":name,"age":age,"hobby":hobby if hobby else None}
    

@app.post("/api/v1/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename":file.filename,"content_type":file.content_type}


# Another use of Data with Pydantic Model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    # Access fields
    item_dict = item.model_dump()  # Converts to dict
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#................................................ Combining Request Body + Path Parameters.........................................
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

# Why using two ** in the item?

# Without the asterix:-

# return {"item_id": item_id, "item": item.model_dump()}

# {
#   "item_id": 10,
#   "item": {
#     "name": "Laptop",
#     "price": 1000,
#     "tax": 50
#   }
# }

# With the two Asterix

# return {"item_id": item_id, **item.model_dump()}

# {
#     "item_id": 10,
#     "name": "Laptop",
#     "price": 1000,
#     "tax": 50
# }

# That means it actually merge the two data into one json format

#.................................Combining Request Body + Path + Query Parameters...................................................
@app.put("/items/{id}")
async def update_item(id: int, item: Item, q: str | None = None):
    result = {"item_id": id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# ....................................................query parameter Validation.....................................

@app.get("/api/v1/query")
async def query_validate(skip : Annotated[int, Query(ge=10,le=50)] = 10):
    result = {"items_number":120, "items_size":"24GB"}
    if skip:
        result.update({"skip":skip})
    
    return result
    
# .....................................................Path parameter Validation.........................................

@app.get("/api/v1/path/{path_id}")
async def path_validate(path_id : Annotated[int,Path(title="This is indicating Path ID")]):
    return {"Path_id":path_id}


# To Find more validation options click [Ctrl + Space]

# ...................................................Query parameter Model.............................................

class Query_Params(BaseModel):
    limit : int = Field(10, ge = 10, le=50, description="Limit must be between 1 to 50") # First argument is always default value
    sort : Literal["price","rating","reviews","popularity"] = "price"
    order_by : Literal["name","date","update_time"] = "name"

# We can use Depends() or Query(). But most api uses Depends()
@app.get("/api/v1/query_model")
# async def query_model(query_params : Annotated[Query_Params,Query()]):  # <-----Query()
async def query_model(query_params : Annotated[Query_Params,Depends()]):
    return query_params


# ...................................................Body Multiple Parameters............................................

class UserBody(BaseModel):
    name : str
    age : int

class Product(BaseModel):
    name : str
    price : float

@app.post("/api/v1/multiple_body")
async def multiple_body(
    user : Annotated[UserBody,Body(embed=True)],
    product : Annotated[Product, Body(embed=True)],
    importance : Annotated[int, Body(embed=False)] = 5 
):
    result = {"use":user, "product":product, "importance":importance}
    return result
    
# Body Multiple Parameter means when we will send multiple data that are associate to Multiple model, then we will use Body(). so that
# FastAPI knows that the data is coming should be extracted From Body(). not from Path() or Query()
# If we want to extracted from path parameter then we will write path()
# If we want from query parameter then we will write Query()


# ...........................................................Body nested Models............................................

class Product1(BaseModel):
    name:str
    price:int
    #tags:list = []
    #tags:list[str] = [] # For impose type safety
    tags: set[str] = set() # prevent duplicate values

@app.post("/api/v1/product1")
async def get_product1(product : Annotated[Product1,Body()]):
    return {"product":product}

# ..................................................Multiple Model...................................................
class Image1(BaseModel):
    url:HttpUrl # imported from Pydantic
    name:str

class User1(BaseModel):
    name:str
    age: int
    images:Image1 | None = None

@app.post("/api/v1/user1")
async def post_user1(user : Annotated[User1, Body()]):
    result = {"user":user}
    return result

# .....................................................Deeply Nested Model.........................................
class Image2(BaseModel):
    url:HttpUrl # imported from Pydantic
    name:str

class User2(BaseModel):
    name:str
    age: int
    images: list[Image2] | None = None

@app.post("/api/v1/user2")
async def post_user2(user : Annotated[User2, Body()]):
    result = {"user":user}
    return result


# ..................................................................Database Related Operations.....................................................

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create User

@app.post("/api/v2/signup",response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    user = User(email=payload.email, username=payload.username)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Read User

@app.get("/api/v2/get",response_model=list[UserOut])
def get_all(db:Session = Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()
    

# Update User

@app.put("/api/v2/update/{user_id}", response_model=UserOut)
def update_user(user_id:int, payload : UserUpdate, db: Session = Depends(get_db)):

    user = db.get(User,user_id)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not Found"
        )

    if payload.email and user.email != payload.email:
        if db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(
                status_code= 400,
                detail= "Email already exists"
            )
        user.email = payload.email
        
    if payload.username and user.username != payload.username:
        if db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        user.username = payload.username

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.delete("/api/v2/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db: Session = Depends(get_db)):
    user = db.get(User,user_id)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not Found"
        )
    
    db.delete(user)
    db.commit()

    return None
        