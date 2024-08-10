from typing import Optional
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["https://recipe-builder.onrender.com/",
           "https://recipe-builder.onrender.com/ingredients"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)

redis = get_redis_connection(
    host="red-cqra9k56l47c73ebbuv0",
    port=6379
)

class Ingredient(HashModel):
    name: str
    class Meta:
        database = redis


@app.get("/ingredients")
async def get_all_ingredients():
    return [format(pk) for pk in Ingredient.all_pks()]


def format(pk: str):
    ingredient = Ingredient.get(pk)

    return {
        'id': ingredient.pk,
        'name': ingredient.name
    }

@app.get("/ingredients/{item_id}")
def get_ingredient(item_id: str, q: Optional[str] = None):
    return Ingredient.get(item_id)

@app.post("/ingredients")
def add_ingredient(ingredient: Ingredient):
    return ingredient.save()

@app.delete("/ingredients/{item_id}")
def del_ingredient(item_id: str, q: Optional[str] = None):
    return Ingredient.delete(item_id)
