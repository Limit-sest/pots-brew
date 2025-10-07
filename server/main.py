from server import get_existing, create_new, get_initial
from rich.console import Console
from rich.text import Text

discovered = get_initial()
console = Console()

with console.screen():
  while True:
    print("Discovered ingredients:")
    for i in range(len(discovered)):
      ing = discovered[i]
      console.print(f"[bright_black]{i+1}[/bright_black] {ing['emoji']} [b]{ing['name']}[/b]")
      console.print(f"   {ing["description"]}", style='italic bright_black')
    print("\nWhat do you want to brew today? Enter numbers separated by space.")
    ingredients_raw = input('> ').split(' ')
    ingredients = []
    for ing in ingredients_raw:
      try:
        ingredients.append(discovered[int(ing)-1]['id'])
      except:
        continue
    if len(ingredients) < 2:
      print("Nothing happened.")
      continue
    
    existing = get_existing(ingredients)
    if existing:
      discovered.append(existing)
      # console.clear()
      print("You have discovered a new item!")
      console.print(f"{existing['emoji']} [b]{existing['name']}[/b]")
      console.print(f"   {existing["description"]}\n", style='italic bright_black')
    else:
      print("Brewing...")
      new = create_new(ingredients)
      if (new == None):
        print("You didn't manage to combine these.")
      else:
        discovered.append(new)
        # console.clear()
        print("You have discovered a new item!")
        console.print(f"{new['emoji']} [b]{new['name']}[/b]")
        console.print(f"   {new["description"]}\n", style='italic bright_black')
        
