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

class ControllerWeb(CtrlOutter):
	commands = [CmdWebBroadCast]
	web_api: IWebApi
	async def run(self):
		# 从web端接收输入命令并反馈给parent控制器执行
		# parent控制器执行结果向web端反馈
		command = await self.web_api.get_request(self.owner)
		if command is not None:
			self.owner.push_command(command)

	async def do_command(self, command: Command):
		# 向web端发送命令
		if isinstance(command, CmdWebBroadCast) \
			or isinstance(command, CmdWebShowMessageFromEntity):
			await self.web_api.post_response(self.owner, command)
			return True
		return False