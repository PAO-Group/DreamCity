import uuid
from typing import Any, TypeAlias, Generator, Generic, TypeVar, Union, Optional, List, Dict, Tuple, FrozenSet, NamedTuple, Deque, Counter, DefaultDict, OrderedDict, AsyncContextManager, Required, ReadOnly, NotRequired, Annotated, TypeIs, Never, NoReturn, ClassVar, Final, Literal, Protocol, TypedDict
from collections.abc import Mapping, Sequence, Set, MutableSequence, MutableSet, MutableMapping, Hashable, Callable, Awaitable, AsyncIterator, Coroutine, AsyncGenerator

class ObjectBase():
	name: str
	description: str
	'''
	游戏对象基类
	'''
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

class ILocation(ObjectBase):
	pass

class IEntity(ObjectBase):
	pass

class IRelation(ObjectBase):
	pass

class IController(ObjectBase):
	pass


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
	