from objects import *

class CmdWebBroadCast(Command):
	'''
	Web广播
	'''
	pass

class CmdWebShowMessageFromEntity(Command):
	'''
	Web中显示来自实体的消息
	'''
	target: Entity
	message: str
	pass

class CmdDoSomework(Command):
	'''
	工作命令
	'''
	time: int # 工作时间
	pass

class CtrlPlayer(CtrlOutter):
	'''
	玩家控制器
	'''
	commands = [CmdWebBroadCast]
	web_api: IWebApi
	state: str = 'idle' # 玩家状态
	async def run(self):
		# 从web端接收输入命令并反馈给parent控制器执行
		# parent控制器执行结果向web端反馈
		command = await self.web_api.get_request(self.owner)
		if command is not None:
			self.owner.push_command(command) # 向实体推送异步命令

	async def do_command(self, command: Command):
		# 向web端发送命令
		if isinstance(command, CmdWebBroadCast) \
			or isinstance(command, CmdWebShowMessageFromEntity):
			await self.web_api.post_response(self.owner, command) # 同步等待函数的执行结果
			return True
		elif isinstance(command, CmdDoSomework):
			if self.state == 'working':
				return False # 玩家正在工作中，不能再次工作
			
			self.state = 'working'
			await asyncio.sleep(command.time)			# 模拟工作的执行
			self.state = 'idle'
			return True
		return False