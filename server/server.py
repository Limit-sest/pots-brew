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
cache.insert(dict(name='Spring Water', emoji='💧', description='Fresh, clear water from a natural source.', evolution=0))
cache.insert(dict(name='Green Leaves', emoji='🍃', description='Freshly picked leaves from a common forest plant.', evolution=0))
cache.insert(dict(name='Rich Loam', emoji='🌱', description='Dark, fertile earth, ideal for growing things.', evolution=0))
cache.insert(dict(name='Flickering Ember', emoji='🔥', description='A small, glowing coal that provides a gentle warmth.', evolution=0))

def get_initial() -> list[dict]:
  return list(cache.find(id=[1,2,3,4]))

def create_new(ingredients: list[int]) -> dict | None:
  new_ingredient = {}
  ingredients_str = json.dumps(list(cache.find(id=ingredients)))
  evolution = list(cache.find(id=ingredients, order_by='evolution'))[0]['evolution']+1
  # Give the AI 3 tries
  for i in range(3):
    try:
      response = client.models.generate_content(
        model="gemini-2.5-flash-preview-09-2025",
        contents=f"""
        You are a village herbalist who crafts simple magical remedies and charms for everyday life. Based on the ingredients and their **Evolution Stage**, describe the resulting concoction.

        **Inputs:**
        - "ingredients": {ingredients_str}
        - "evolution_stage": {evolution}

        **Process Goal:**
        1.  **Logical Foundation:** Determine the basic *physical consistency* (e.g., Paste, Dust, Tonic, Liniment) that would logically result from combining the raw ingredients.
        2.  **Magic Depth Integration:** Use the `evolution_stage` to determine the level of enchantment:
            *   **Stage 1:** The result is a common item that often has no magical properties. 
            *   **Stage 2:** The result is a simple, very practical item. Its magic is barely noticeable.
            *   **Stage 3:** The result is a proper folk charm or minor remedy. Its magic is subtle but verifiable.
            *   **Stage 4+:** The result verges on true low-level magic. The item's function is more abstract and enchanted.

        **Output Constraint:**
        The final item's name **must** reflect its physical state and its evolution stage (more advanced names for higher stages)

        Your output must be a single JSON object (without code blocks) with three keys:
        - "name": A simple, evocative name that fits the Evolution Stage and includes its physical consistency.
        - "emoji": One fitting emoji for the item.
        - "description": A one-sentence summary of its gentle magical property or use, directly aligning with the Magic Depth rules above.

        Do not reuse the ingredient names in your output.
        """
        ,
      ).text
      response.replace("```json", "").replace("```", "")
      new_ingredient = dict(json.loads(response))
      new_ingredient['evolution'] = evolution
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

