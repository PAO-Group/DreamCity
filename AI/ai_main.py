from db_manager import *
from objects import *

async def main():
	global global_db
	global_db = DbManager("")
	GameContext.entities = global_db.find_object(Entity)
	GameContext.tick = 0
	while True:
		for entity in GameContext.entities:
			try:
				asyncio.create_task(entity.run())
			except:
				print('运行发生错误')

		GameContext.tick += 1

if __name__ == '__main__':
	asyncio.create_task(main())