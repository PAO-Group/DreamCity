from ai_base import *
from db_manager import *

class Entity(IEntity):
	entity_type: str
	location: Optional[ILocation]
	'''
	游戏实体
	'''
	def on_saving(self, dt: dict):
		dt.update({
			'location': None,
			'location_id': None if self.location is None else str(self.location.id),
		})
	
	def on_loaded(self, dt: dict):
		self.location = global_db.get_object(Location, dt['location_id'])
		
	def find_relatives(self, relation_type: str):
		'''
		查找与自己有关的关系
		'''
		return global_db.find_object(Relation, relation_type=relation_type, subject_id=self.id) + global_db.find_object(Relation, relation_type=relation_type, object_id=self.id)

class Location(ILocation):
	'''
	位置
	'''
	parent_location: Optional[ILocation]
	
	def on_saving(self, dt: dict):
		dt.update({
			'parent_location': None,
			'parent_id': None if self.parent_location is None else str(self.parent_location.id),
		})
	
	def on_loaded(self, dt: dict):
		self.parent_location = global_db.get_object(Location, dt['parent_id'])

	def find_child_locations(self):
		'''
		查找子位置
		'''
		return global_db.find_object(ILocation, parent_id=self.id)
	
class Relation(IRelation):
	'''
	关系
	'''
	relation_type: str
	subject: Optional[Entity]
	object: Optional[Entity]
	def on_saving(self, dt: dict):
		dt.update({
			'subject': None,
			'object': None,
			'subject_id': None if self.subject is None else str(self.subject.id),
			'object_id': None if self.object is None else str(self.object.id)
		})
	
	def on_loaded(self, dt: dict):
		self.subject = global_db.get_object(Entity, dt['subject_id'])
		self.object = global_db.get_object(Entity, dt['object_id'])

class Controller(IController):
	'''
	AI控制器
	'''
	pass

class PersonControll(Controller):
	'''
	人员控制器
	'''
	
	pass