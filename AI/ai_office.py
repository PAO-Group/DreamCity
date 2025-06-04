from objects import *

class CmdMeetingStart(Command):
	'''开始会议'''

class CmdMeetingEnd(Command):
	'''结束会议'''

class CmdMeetingSpeechEnd(Command):
	'''会议发言'''
	member: Human
	topic: str
	response: str

class EntMeeting(Organization):
	'''会议'''
	chairman: Human
	members: List[Human]
	

class CtrlMeeting(CtrlAI):
	commands = [CmdMeetingStart, CmdMeetingEnd, CmdMeetingSpeechEnd]
	status = 'idle'
	meeting_goals:list[str] = []
	speech_member_index = 0
	current_goal_index = 0
	achieved_goals:dict[str, str] = {}
	'''
	会议控制器
	'''
	async def run(self):
		# 主席发言
		if isinstance(self.owner, EntMeeting):
			if self.status == 'exited':
				'''退出会议'''
				self.owner.destroy()
				return

			# 主席发言
			if self.status == 'started':
				self.owner.chairman.push_command(CmdMeetingSpeech(topic='会议开始', content='开场白'))
				self.status = 'member_speaking'
				self.current_goal_index = 0
			# 针对每个目标循环发言
			if self.status == 'member_speaking':
				if self.current_goal_index < len(self.meeting_goals):
					goal = self.meeting_goals[self.current_goal_index]	
					# 循环发言
					if self.speech_member_index < len(self.owner.members):
						member = self.owner.members[self.speech_member_index]
						member.push_command(CmdMeetingSpeech(topic='发言时间', content=f'请针对主题{goal}发言'))
						self.speech_member_index += 1
					else:
						self.speech_member_index = 0
						self.current_goal_index += 1
				else:
					self.status = 'summary_speaking'
			
			if self.status == 'member_speakend':
				self.status = 'member_speaking'
				
			# 总结发言
			if self.status =='summary_speaking':
				self.owner.chairman.push_command(CmdMeetingSpeech(topic='会议结束', content='总结发言'))

	async def do_command(self, command):
		if isinstance(command, CmdMeetingStart):
			# 开始会议
			self.status = 'started'
			return True
		elif isinstance(command, CmdMeetingSpeechEnd):
			# 成员结束发言后，记录发言内容
			self.achieved_goals[self.meeting_goals[self.current_goal_index]] = command.response
			self.status = 'member_speakend'
			return True
		elif isinstance(command, CmdMeetingEnd):
			# 结束会议
			self.status = 'stopped'
			return True
		return False

class CmdMeetingSpeech(Command):
	'''会议发言'''
	meeting: EntMeeting
	topic: str
	content: str

class CtrlHumanSpeech(CtrlAI):
	commands = [CmdMeetingSpeech]
	'''
	人类发言控制器
	'''
	async def do_command(self, command):
		if isinstance(command, CmdMeetingSpeech):
			result = await self.ai_api.run_ai('会议中，准备发言', [{'content': command.content, 'topic': command.topic}])
			command.meeting.push_command(CmdMeetingSpeechEnd(topic=command.topic, response=result, member=self.owner))
			return True
		return False