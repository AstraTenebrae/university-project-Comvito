from api_settings import app, db
from db_tables import Category

def add_default_categories():
    """Добавляет стандартные категории в базу данных"""
    with app.app_context():
        # Проверяем, есть ли уже категории
        existing = db.session.scalars(db.select(Category)).first()
        if existing:
            print("Категории уже существуют")
            return
        
        # Список категорий по умолчанию
        default_categories = [
            "Одежда",
            "Обувь",
            "Электроника",
            "Книги",
            "Мебель",
            "Спорт",
            "Игры",
            "Детские товары",
            "Красота и здоровье",
            "Автотовары",
            "Инструменты",
            "Хобби и творчество"
        ]
        
        # Добавляем категории
        for cat_name in default_categories:
            category = Category(category_name=cat_name)
            db.session.add(category)
        
        db.session.commit()
        print(f"Добавлено {len(default_categories)} категорий")

if __name__ == "__main__":
    add_default_categories()