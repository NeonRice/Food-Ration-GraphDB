from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class QueryManager:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_ingredient(self, ingredient_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_ingredient, ingredient_name)
            if result:
                print("Found ingredient: {result}".format(
                    result=result[0]['ingredient']['name']))
                print("Ingredient price: {price}".format(
                    price=result[0]['ingredient']['price']))
            else:
                print("Ingredient not found")

    def find_ingredients_by_meal(self, meal_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_ingredients_by_meal, meal_name)
            if result:
                print("Ingredients in {meal}:".format(meal=meal_name))
                for ingredient in result:
                    print("{i} Price: {p}".format(
                        i=ingredient['ingredient']['name'], 
                        p=ingredient['ingredient']['price']))
            else:
                print("Meal not found")

    def find_allergen_food(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_allergen_food, person_name)
            if result:
                print("{p} shouldn't eat the following meals: ".format(p=person_name))
                for allergen in result:
                    print("Meal: {a}, because allergic to: {i}".format(
                        a=allergen['meal']['name'], 
                        i=allergen['ingredient']['name']))
            else:
                print("Person is not allergic to any meals on record")

    def find_meal_price(self, meal_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_meal_price, meal_name)
            if result[0]['meal_price']:
                print("Price of Meal: {m} -> {p}".format(
                    m=meal_name, 
                    p=result[0]['meal_price']))
            else:
                print("Either meal doesn't exit or it's ingredients don't have a price set..")

    def find_shortest_path_to_meal(self, person_name, meal_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_shortest_path_to_meal, person_name, meal_name)
            if result:
                for value in result[0]['shortest_path']:
                    if isinstance(value, str):
                        print(value, end="->")
                    else:
                        print("{name}-".format(name=value['name']), end="")
            else:
                print("A path doesn't exist")

    @staticmethod
    def _find_and_return_ingredient(tx, ingredient_name):
        query = (
            "MATCH (ingredient:Ingredient) "
            "WHERE ingredient.name = $ingredient_name "
            "RETURN ingredient"
        )
        result = tx.run(query, ingredient_name=ingredient_name)

        return result.data()

    @staticmethod
    def _find_and_return_ingredients_by_meal(tx, meal_name):
        query = (
            "MATCH (:Meal {name: $meal_name})-[:REQUIRES]->(ingredient:Ingredient)"
            "RETURN ingredient"
        )
        result = tx.run(query, meal_name=meal_name)

        return [ingredient for ingredient in result.data()]

    @staticmethod
    def _find_and_return_allergen_food(tx, person_name):
        query = (
            "MATCH (p:Person {name: $person_name}),"
            "(p)-[:ALLERGIC_TO]->(ingredient)<-[:REQUIRES]-(meal)"
            "RETURN meal, ingredient"
        )
        result = tx.run(query, person_name=person_name)

        return [record for record in result.data()]

    @staticmethod
    def _find_and_return_meal_price(tx, meal_name):
        query = (
            "MATCH (m:Meal {name: $meal_name}), (i:Ingredient),"
            "(m)-[:REQUIRES]->(i)"
            "RETURN sum(i.price) as meal_price"
        )
        result = tx.run(query, meal_name=meal_name)

        return result.data()

    @staticmethod
    def _find_and_return_shortest_path_to_meal(tx, person_name, meal_name):
        query = (
            "MATCH (in:Meal {name: $meal_name}), (j:Person {name: $person_name}),"
            "p = shortestPath((j)-[:KNOWS|COOKS*]->(in))"
            "return p as shortest_path"
        )
        result = tx.run(query, meal_name=meal_name, person_name=person_name)

        return result.data()

    """ SOMEDAY
    RETURN MIN total_price with name
    MATCH (d1:Meal)-[:REQUIRES]->(d2:Ingredient)
    with d1, sum (d2.price) AS total_price
    RETURN d1, min(total_price) """