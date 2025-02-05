import pymongo
import urllib.parse
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBBackend:
    def __init__(self, username, password, db_name, collection_name, cluster_url="cluster13.wiqb1.mongodb.net"):
        """
        Initialize MongoDB connection.

        :param username: MongoDB username
        :param password: MongoDB password
        :param db_name: Database name
        :param collection_name: Collection name
        :param cluster_url: MongoDB cluster URL (default: cluster0.mongodb.net)
        """
        self.username = username
        self.password = password
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = pymongo.MongoClient(
            f"mongodb+srv://{urllib.parse.quote(username)}:{urllib.parse.quote(password)}@{cluster_url}/?retryWrites=true&w=majority"
        )
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_post(self, title, content, tags, length, language):
        """
        Save a generated post to the database with additional metadata.

        :param title: Title of the post
        :param content: Content of the post
        :param tags: Associated tags
        :param length: Length of the post
        :param language: Language of the post
        :return: Inserted document ID
        """
        document = {
            "title": title,
            "content": content,
            "tags": tags,
            "length": length,
            "language": language,
        }
        result = self.collection.insert_one(document)
        return result.inserted_id

    def get_all_posts(self):
        return list(self.collection.find())  # Ensures all fields, including _id, are fetched

    def delete_post(self, post_id):
        from bson.objectid import ObjectId
        result = self.collection.delete_one({"_id": ObjectId(post_id)})
        return result.deleted_count

    def get_all_topics(self):
        topics = self.collection.distinct("tags")
        return topics

    def update_post_title(self, post_id, new_title):
        if post_id in self.collection:
            self.collection[post_id]["title"] = new_title
            return True
        return False

