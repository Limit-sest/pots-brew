import dataset
from google import genai
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
client = genai.Client(api_key=getenv('AI_TOKEN'))

db = dataset.connect('sqlite:///cache.db')
cache = db['cache']
parents = db['parents']

# First db setup
# cache.insert(dict(name='River Water', emoji='💧', description='Water sourced from the local river.'))
# cache.insert(dict(name='Magical Leaves', emoji='🍃', description='Leaves collected from the old magical tree.'))
# cache.insert(dict(name='Ancient Soil', emoji='🌱', description='A handful of rich, dark earth, containing the condensed mineral dust from the deepest strata of the world. The source of all physical matter.'))
# cache.insert(dict(name='Arcane Flame', emoji='🔥', description='A tiny, restless flicker of captured wild magic.'))

def get_initial() -> list[dict]:
  return list(cache.find(id=[1,2,3,4]))

def create_new(ingredients: list[int]) -> dict | None:
  new_ingredient = {}
  # Give the AI 3 tries
  for i in range(3):
    try:
      response = client.models.generate_content(
        model="gemini-2.5-flash-preview-09-2025",
        contents=f"""Create a short understandable name, one emoji and one-sentence description for a magical or normal ingredient, thing, potion or anything else that would be created by combining following ingredients in a cauldron:
        {json.dumps(list(cache.find(id=ingredients)))}
        Return this as a json object with following fields: name, emoji, description
        Do not use the word of the ingredients, return only one emoji!
        Return this as a json, without code blocks!
        Consider things like dilution. The result can be mild, they do not have to be always epic.""",
      ).text
      response.replace("```json", "").replace("```", "")
      new_ingredient = dict(json.loads(response))
      new_ingredient['id'] = cache.insert(new_ingredient)
      for ing in ingredients:
        parents.insert(dict(child_id=new_ingredient['id'], parent_id=ing))
    except:
      pass
    else:
      break
  else:
    return None
  return new_ingredient

def get_existing(ingredients: list[int]) -> int | None:
  child_ids = {row['child_id'] for row in parents.all()}

  for child_id in child_ids:
      rows = list(parents.find(child_id=child_id))
      parent_ids = [r['parent_id'] for r in rows]
      parent_set = set(parent_ids)

      if parent_set == set(ingredients):
          return cache.find_one(id=child_id)
  return None

