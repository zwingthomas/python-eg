# Acknowledgements
# pixegami
# Python FastAPI Tutorial: Build a REST API in 15 Minutes
# https://www.youtube.com/watch?v=iWS9ogMPOI0&t=147s&ab_channel=pixegami
#
# Tech with Tim
# Python FastAPI Tutorial
# https://www.youtube.com/watch?v=-ykeT6kk4bk&ab_channel=TechWithTim


"""
FastAPI is a framework for creating an API in Python. It is
- Easy to learn
- Performant
- High developer velocity

It also supports Pydantic models

If you type in http://API_BASE_URL:PORT/docs#/ you get automatically
generated docs for your API in Swagger UI! You can even use this to
automatically send requests to your API and test it out easily.

If you type in .../redoc/ instead it is other documentation, pretty much 
the same thing. But slightly beautified.

If you type in .../openapi.json/ you get the documentation as json even!

FastAPI vs Flask:
FastAPI is async by default, running on ASGI with uvicorn rather than
WSGI with gunicorn. It is easier to use too. But it has less adoption
and less support than Flask though. Some of these points compare to 
Django as well, but Django is really heavy so if you need something
lighter, then FastAPI is the way to go.
"""


from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel
from typing import Optional  # Recommended, not enforced, by FastAPI docs

app = FastAPI()


class Item(BaseModel):
    text: str                        # Required: no default, must be str
    is_done: Optional[bool] = False  # Optional, but must be bool

# Decorators define paths which define what to return when people visit
# different URLs of your app.


items = []


@app.get("/")
def root():
    return {"Hello": "World"}


# @app.post("/items")
# def create_item(item: str):
#     # item is now a query parameter!
#     # API_BASE_URL/items?item=apple
#     items.append(item)
#     return item

@app.post("/items")
def create_item(*,  # default args follow nondefault always. To avoid use
                    # *. this is bad practice but essentially this says to
                    # allow unlimited positional arguments and the rest,
                    # as well as their matches, should be treated as key
                    # word arguments.
                item: Item = Path(None,
                                  description="The item you're adding to the backend", max_length=10, min_length=1),
                is_done: Optional[bool],):
    # Path
    # Path allows you to add more detail to what you expect for the
    # path parameter.
    # It works with Path(default input, description, constraints)
    # This Path import is really great for your docs.
    # It can also do contraints like max_length, min_length, gt:
    # greater than, lt: less than, ge, le, and min_items/max_items for
    # lists in Pydantic v1.
    # DO NOT USE THEM DYNAMICALLY, Bounds are evaluated at import time!
    #
    # Now it expects the item to be passed through the json body!!
    # API_BASE_URL/items with a body of Item:
    # {"text": "apple", "is_done": "True"}
    # {"text": "orange"}
    items.append(item)
    # Common to return the same item back with the 200
    return item


# @app.get("/items")
# def list_items(limit: int = 10):
#     return items[0:limit]

@app.get("/items", response_model=list[Item])
# With response_model we tell our server that the response from this
# endpoint would be conforming to the pydantic model. Allows for defined
# response structures.
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Path arguments, everything in the path is assumed to be a path
       parameter."""
    # API_BASE_URL/items/3
    if item_id > 0 and item_id < len(items):
        return items[item_id]
    else:
        return HTTPException(status_code=404,
                             detail=f"Item {item_id} for found")

# PUT is for full updates, PATCH has a lot of optionals with the
# pydantic model.


@app.put("/update-item/{item_id}")
# lt=len(items) is not okay to do. Bounds are evaluated at import time!!
# items could grow or shrink as the application runs (it does)
def update_item(is_done: bool, item_id: int = Path(None, ge=0)):
    """
    Update the item, ensure that the id passed in is within our array
    size / index.
    """
    try:
        items[item_id].is_done = is_done
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/delete")
# lt=len(items) is not okay to do. Bounds are evaluated at import time!!
# items could grow or shrink as the application runs (it does)
def delete_item(item_id: int = Path(...,
                                    description="The ID of the item to delete", ge=0)):
    try:
        items = items[:item_id-1]+items[item_id:]
        return status.HTTP_204_NO_CONTENT
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")
