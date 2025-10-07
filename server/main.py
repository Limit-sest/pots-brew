import dataset
from google import genai
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
client = genai.Client(api_key=getenv('AI_TOKEN'))

# response = client.models.generate_content(
#     model="gemini-2.5-flash-lite",
#     contents="""Create a short understandable name, one utf-8 encoded emoji and one-sentence description for a magical or normal ingredient, thing, potion or anything else that would be created by combining following ingredients in a cauldron:
#     {"id": 1, "name": "River Water", "emoji": "\ud83d\udca7"}, {"name": "Glimmer Dew", "emoji": "✨", "description": "A luminous liquid that captures the essence of flowing currents and celestial radiance."}
#     Return this as a json object with following fields: name, emoji (utf-8 encoded), description
#     Do not use the word of the ingredients 
#     Return this as a json, without code blocks!
#     Consider things like dilution. The result can be mild, they do not have to be always epic.""",
# )

# print(response.text)

db = dataset.connect('sqlite:///cache.db')
cache = db['cache']
parents = db['parents']


# First db setup
# cache.insert(dict(name='River Water', emoji='💧', description='Water sourced from the local river.'))
# cache.insert(dict(name='Magical Leaves', emoji='🍃', description='Leaves collected from the old magical tree.'))
# cache.insert(dict(name='Ancient Soil', emoji='🌱', description='A handful of rich, dark earth, containing the condensed mineral dust from the deepest strata of the world. The source of all physical matter.'))
# cache.insert(dict(name='Arcane Flame', emoji='🔥', description='A tiny, restless flicker of captured wild magic.'))

discovered = list(cache.find(id=[1,2,3,4]))
while True:
  print("Discovered ingredients:")
  for ing in discovered:
    print(f"{ing["id"]} {ing["emoji"]} {ing["name"]}")
    print(f"   {ing["description"]}")
  print("What do you want to brew today? Enter numbers separated by space.")
  ingredients_raw = input('> ').split(' ')
  if len(ingredients_raw) < 2:
    print("Nothing happened.")
    continue
  ingredients = []
  for ing in ingredients_raw:
    try:
      ingredients.append(int(ing))
    except:
      continue
  