
from pymongo import MongoClient
from ai_base import *

T = TypeVar('T', bound = ObjectBase)
class DbManager:
	'''
	数据库管理器
	'''
	def __init__(self, uri: str, db_name: str="storyDB", collection_name: str="sessions"):
		self.client = MongoClient(uri)
		self.db = self.client[db_name]
		self.sessions = self.db[collection_name]
		
	def add_object(self, entity: ObjectBase):
		'''
		向数据库添加实例
		'''
		self.sessions.insert_one(entity.to_dict())

	def update_object(self, entity: ObjectBase):
		'''
		更新数据库中的实例
		'''
		self.sessions.update_one({"_id": entity.id}, {"$set": entity.to_dict()})

	def get_object(self, obj_class: type[T], entity_id: str) -> Optional[T]:
		'''
		从数据库中获取实例
		'''
		entity_dict = self.sessions.find_one({"_id": entity_id})
		if entity_dict is None:
			return None
		return from_dict(obj_class, entity_dict)

	def delete_object(self, entity_id: str):
		'''
		从数据库中删除实例
		'''
		self.sessions.delete_one({"_id": entity_id})

	def find_object(self, object_class: type[T], **kwargs) -> list[T]:
		'''
		从数据库中查询实体
		'''
		entity_dicts = self.sessions.find({"_type": object_class.__name__, **kwargs})
		return [from_dict(object_class, entity_dict) for entity_dict in entity_dicts]

global_db = DbManager("mongodb://localhost:27017/")
