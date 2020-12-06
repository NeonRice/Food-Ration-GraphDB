class Option():
    def __init__(self, optionName, optionFunction):
        self.name = optionName
        self.function = optionFunction


def drawOptions(listOfOptions):
    optionNr = 1
    for option in listOfOptions:
        print(optionNr, option.name)
        optionNr += 1

def clearOutput():
    print("\033[H\033[J")

def handleInput(options):
    choice = input()
    if choice.isdigit() and int(choice) <= len(options):
        choice = int(choice)
        return options[choice - 1].function()

def enterToContinue(instruction="\nPress enter to continue.."):
    input(instruction)

def initOptions(query):

    def find_ingredient_by_name():
        clearOutput()
        query.find_ingredient(input("Enter ingredient to look for -> ").title())
        enterToContinue()
    
    def find_ingredients_in_meal():
        clearOutput()
        query.find_ingredients_by_meal(input("Enter meal -> ").title())
        enterToContinue()

    def find_allergenic_meals():
        clearOutput()
        query.find_allergen_food(input("Enter person name -> ").title())
        enterToContinue()

    def find_calculate_meal_price():
        clearOutput()
        query.find_meal_price(input("Enter meal name -> ").title())
        enterToContinue()

    def find_shortest_path_to_meal():
        clearOutput()
        query.find_shortest_path_to_meal(
                input("Enter person name -> ").title(), 
                input("Enter meal name -> ").title())
        enterToContinue()

    options = (
        Option("Find ingredient by name", find_ingredient_by_name),
        Option("Find ingredients in a meal", find_ingredients_in_meal),
        Option("Find a person's allergenic meals", find_allergenic_meals),
        Option("Find and calculate a meals price", find_calculate_meal_price),
        Option("Find the shortest path to a meal source for person", find_shortest_path_to_meal)
    )

    return options