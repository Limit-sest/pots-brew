from server import discover, get_initial
from rich.console import Console
from rich.text import Text
import asyncio
async def main():
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
      
      print('Brewing...')
      new = await discover(ingredients)
      if new == None:
        print("You didn't manage to combine these. Maybe try again?")
      else:
        discovered.append(new)
        print("You have discovered a new item!")
        console.print(f"{new['emoji']} [b]{new['name']}[/b]")
        console.print(f"   {new["description"]}\n", style='italic bright_black')

if __name__ == "__main__":
    asyncio.run(main())
