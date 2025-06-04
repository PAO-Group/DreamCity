import openai
from ai_base import *

class APApi_OpenAI(IAIApi):
	api_key: str = "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"
	def __init__(self):
		openai.api_key = self.api_key

	async def run_ai(self, prompt: str, params: list[dict[str, Any]])->str:
		response = openai.ChatCompletion.create(
				model="gpt-4o",
				message=params,  # 输入信息
				prompt="Hello, how can I help you?",  # 提示信息
				max_tokens=250,  # 最大返回令牌数
				temperature=0.9  # 控制输出的随机性
		)
		return response.choices[0].message["content"]