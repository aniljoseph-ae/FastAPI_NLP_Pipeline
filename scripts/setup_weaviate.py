import weaviate
from app.core.config import settings

client = weaviate.Client(settings.WEAVIATE_URL)
schema = {
    "classes": [
        {
            "class": "Documents",
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["text"]},
            ],
            "vectorizer": "none",
        }
    ]
}
client.schema.create(schema)
print("Weaviate schema created successfully.")