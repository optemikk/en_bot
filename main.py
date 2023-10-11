from loader import *
import asyncio


async def on_shutdown():
    await bot.close()
    await dp.close()


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    from handlers import *
    asyncio.run(main())