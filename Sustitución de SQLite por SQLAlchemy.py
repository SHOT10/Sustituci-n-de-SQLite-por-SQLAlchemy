from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión con MariaDB
# Cambia 'usuario', 'contraseña' y 'localhost' por tus credenciales.
DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/recetas_db"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    Base = declarative_base()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Modelo de la base de datos
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)

# Crear las tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")
    exit()

# Funciones de la lógica de la aplicación
def add_recipe():
    session = SessionLocal()
    try:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        ingredients = input("Enter ingredients (comma-separated): ").strip()
        if not ingredients:
            print("Ingredients cannot be empty.")
            return

        steps = input("Enter steps (separated by periods): ").strip()
        if not steps:
            print("Steps cannot be empty.")
            return

        new_recipe = Recipe(name=name, ingredients=ingredients, steps=steps)
        session.add(new_recipe)
        session.commit()
        print("Recipe added successfully.")
    except Exception as e:
        print(f"Error while adding recipe: {e}")
    finally:
        session.close()

def update_recipe():
    session = SessionLocal()
    try:
        name = input("Enter the name of the recipe to update: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        recipe = session.query(Recipe).filter(Recipe.name == name).first()
        if not recipe:
            print("Recipe not found.")
            return

        new_name = input("Enter new recipe name (leave blank to keep current): ").strip()
        new_ingredients = input("Enter new ingredients (leave blank to keep current): ").strip()
        new_steps = input("Enter new steps (leave blank to keep current): ").strip()

        if new_name:
            recipe.name = new_name
        if new_ingredients:
            recipe.ingredients = new_ingredients
        if new_steps:
            recipe.steps = new_steps

        session.commit()
        print("Recipe updated successfully.")
    except Exception as e:
        print(f"Error while updating recipe: {e}")
    finally:
        session.close()

def delete_recipe():
    session = SessionLocal()
    try:
        name = input("Enter the name of the recipe to delete: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        recipe = session.query(Recipe).filter(Recipe.name == name).first()
        if not recipe:
            print("Recipe not found.")
            return

        session.delete(recipe)
        session.commit()
        print("Recipe deleted successfully.")
    except Exception as e:
        print(f"Error while deleting recipe: {e}")
    finally:
        session.close()

def list_recipes():
    session = SessionLocal()
    try:
        recipes = session.query(Recipe).all()
        if recipes:
            print("\nList of Recipes:")
            for recipe in recipes:
                print(f"- {recipe.name}")
        else:
            print("No recipes found.")
    except Exception as e:
        print(f"Error while listing recipes: {e}")
    finally:
        session.close()

def view_recipe():
    session = SessionLocal()
    try:
        name = input("Enter the name of the recipe to view: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        recipe = session.query(Recipe).filter(Recipe.name == name).first()
        if not recipe:
            print("Recipe not found.")
            return

        print("\nIngredients:")
        print(recipe.ingredients)
        print("\nSteps:")
        print(recipe.steps)
    except Exception as e:
        print(f"Error while viewing recipe: {e}")
    finally:
        session.close()

def main():
    while True:
        print("\nRecipe Book")
        print("1. Add New Recipe")
        print("2. Update Recipe")
        print("3. Delete Recipe")
        print("4. List Recipes")
        print("5. View Recipe")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_recipe()
        elif choice == '2':
            update_recipe()
        elif choice == '3':
            delete_recipe()
        elif choice == '4':
            list_recipes()
        elif choice == '5':
            view_recipe()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



