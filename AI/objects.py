from ai_base import *
from db_manager import *

class Entity(IEntity):
	entity_type: str
	location: Optional[ILocation]
	main_controller: Optional[IController]
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

	def push_command(self, command: Command):
		'''
		发送命令
		'''
		self.commands.append(command)

	async def run(self):
		'''
		实体运行
		'''	
		if self.main_controller is not None:
			# 运行主控制器
			await self.main_controller.run()

	def save(self):
		'''
		保存
		'''
		global_db.update_object(self)

class Organization(IOrganization):
	child_organizations: list[IOrganization] = []
	'''组织'''
	pass

class Human(IHuman):
	'''人类'''
	pass

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
	控制器
	'''
	owner: IEntity # 所属实体
	parent_controller: Optional[IController] = None # 父控制器
	child_controllers: dict[str, IController] = {} # 子控制器
	def __init__(self, owner: Entity, parent_controller: Optional[IController] = None):
		super().__init__()
		self.owner = owner
		self.parent_controller = parent_controller
		if parent_controller is not None:
			parent_controller.child_controllers[self.id] = self

class CmdClearCommands(Command):
	'''
	清空命令
	'''

class CmdCancelCommand(Command):
	'''
	取消命令
	'''
	def __init__(self, command: Command):
		self.command = command

class CtrlEntityMain(Controller):
	commands = [CmdClearCommands, CmdCancelCommand]
	'''
	实体主控制器
	'''
	async def run(self):
		'''
		运行实体主控制器, 处理命令
		'''
		# 处理命令
		self.owner.commands.sort(key=lambda x: x.priority)
		child_controllers = [controller for controller in self.child_controllers.values() if controller.__class__ in self.commands]
		child_controllers.sort(key=lambda x: x.priority)
		for command in self.owner.commands:
			for child_controller in child_controllers:
				result = await child_controller.do_command(command)
				if result:
					self.owner.commands.remove(command)
					break

		self.owner.commands.clear()

	async def do_command(self, command: Command):
		'''
		处理命令
		'''
		if isinstance(command,CmdClearCommands):
			self.owner.commands.clear()
			return True
		elif isinstance(command, CmdCancelCommand):
			self.owner.commands.remove(command)
		return False

class CtrlOutter(Controller):
	'''
	外界控制器
	'''
	pass

class CtrlAI(Controller):
	'''
	AI控制器
	'''
	ai_api: IAIApi
	def __init__(self, owner: Entity, ai_api: IAIApi):
		super().__init__(owner)
		self.ai_api = ai_api

class CtrlHuman(Controller):
	'''
	人类控制器
	'''
	pass
