import uuid
from typing import Any, TypeAlias, Generator, Generic, TypeVar, Union, Optional, List, Dict, Tuple, FrozenSet, NamedTuple, Deque, Counter, DefaultDict, OrderedDict, AsyncContextManager, Required, ReadOnly, NotRequired, Annotated, TypeIs, Never, NoReturn, ClassVar, Final, Literal, Protocol, TypedDict
from collections.abc import Mapping, Sequence, Set, MutableSequence, MutableSet, MutableMapping, Hashable, Callable, Awaitable, AsyncIterator, Coroutine, AsyncGenerator
import asyncio
import json
import os
import sys
import time
import random
import math

class ObjectBase():
	'''
	游戏对象基类
	'''
	name: str # 名称
	description: str # 描述
	def __init__(self):
		self.id = str(uuid.uuid4())

	def on_saving(self, dt: dict):
		pass

	def on_loaded(self, dt: dict):
		pass

	def to_dict(self):
		'''
		转换为字典
		'''
		dt = self.__dict__
		self.on_saving(dt)
		return dt

T = TypeVar('T', bound=ObjectBase)
def from_dict(object_class: type[T], data: dict) -> T:
	'''
	从字典中恢复
	'''
	new_object = object_class()
	new_object.__dict__.update(data)
	new_object.on_loaded(data)
	return new_object

class Command(ObjectBase):
	params: list[dict[str, Any]] = [] # 参数
	priority: int = 0 # 优先级
	'''
	命令接口
	'''
	def __init__(self, **kwargs):
		super().__init__()
		self.__dict__.update(kwargs)

class ILocation(ObjectBase):
	'''
	位置接口
	'''
	pass

class IEntity(ObjectBase):
	commands: list[Command] = [] # 命令列表
	'''
	实体接口
	'''
	async def run(self):
		'''运行'''
		pass
	def push_command(self, command: Command):
		'''
		推送命令
		'''
		pass
	def destroy(self):
		pass

class IOrganization(IEntity):
	'''
	组织接口
	'''
	pass

class IHuman(IEntity):
	'''
	人物接口
	'''
	pass

class IRelation(ObjectBase):
	'''
	关系接口
	'''
	pass

class IController(ObjectBase):
	commands: list[type[Command]] = [] # 命令列表
	priority: int = 0 # 优先级
	child_controllers: dict[str, Any] = {}# 子控制器
	'''
	控制器接口
	'''
	async def run(self):
		'''
		运行
		'''
		pass

	async def do_command(self, command: Command)->bool:
		'''
		执行命令
		'''
		return False
	
class EntityType:
	'''
	游戏实体类型
	'''
	organization = 'organization'
	person = 'person'
	object = 'object'
	friend_ship = 'friend_ship'
	meeting = 'meeting'

class RelationType:
	'''
	关系类型
	'''
	child = 'child'
	parent = 'parent'
	friend = 'friend'
	master = 'master'
	boss = 'boss'

class GameContext:
	'''
	游戏上下文
	'''
	tick: int = 0
	speed: float = 1.0
	time_scale: float = 1.0
	entities: list[IEntity] = []

class IAIApi():
	'''
	AI API接口
	'''
	async def run_ai(self, prompt:str, params: list[dict[str, Any]])->Optional[str]:
		pass

class IWebApi():
	'''
	Web API接口
	'''
	async def get_request(self, entity: IEntity)->Optional[Command]:
		pass

	async def post_response(self, entity: IEntity, command: Command)->None:
		pass
