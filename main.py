from typing import Optional
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI

app = FastAPI()

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
    return Ingredient.all_pks()

@app.get("/ingredients/{item_id}")
def get_ingredient(item_id: int, q: Optional[str] = None):
    return Ingredient.get(item_id)

@app.post("/ingredients")
def add_ingredient(ingredient: Ingredient):
    return ingredient.save()

@app.delete("/ingredients/{item_id}")
def del_ingredient(item_id: int, q: Optional[str] = None):
    return Ingredient.delete(item_id)
