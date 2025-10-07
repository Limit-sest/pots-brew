from server import get_existing, create_new, get_initial

discovered = get_initial()

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
  
  existing = get_existing(ingredients)
  if existing:
    discovered.append(existing)
  else:
    new = create_new(ingredients)
    if (new == None):
      print("You didn't manage to combine these.")
    else:
      discovered.append(new)
