from pymongo import MongoClient
from django.conf import settings
from pymongo.server_api import ServerApi
import os
from ..models import Equipment, Category

def get_mongo_client():
    client = MongoClient(os.getenv('MONGO_URI'), server_api=ServerApi('1'))
    return client

def sync_to_mongodb():
    client = None
    try:
        client = get_mongo_client()
        db = client[os.getenv('DB_NAME')]
        
        # Sync categories
        categories_collection = db['categories']
        categories_collection.delete_many({})  
        
        categories = Category.objects.all()
        category_data = [
            {
                'id': str(category.id),
                'categoryname': category.categoryname
            }
            for category in categories
        ]
        if category_data:
            categories_collection.insert_many(category_data)
        
        # Sync equipment
        equipment_collection = db['equipment']
        equipment_collection.delete_many({})
        
        equipment = Equipment.objects.all()
        equipment_data = [
            {
                'id': str(eq.id),
                'category_id': str(eq.category.id),
                'category_name': eq.category.categoryname,
                'eqname': eq.eqname,
                'imglink': eq.imglink,
                'ytlink': eq.ytlink,
                'stock': eq.stock,
                'description': eq.description
            }
            for eq in equipment
        ]
        if equipment_data:
            equipment_collection.insert_many(equipment_data)
            
        return True, "Sync completed successfully"
        
    except Exception as e:
        return False, f"Error during sync: {str(e)}"
    finally:
        if client:
            client.close()