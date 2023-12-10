import asyncio

async def delay(waiting: int):
    await asyncio.sleep(waiting)
    print(f"Waiting {waiting} sec")

async def main():
    await asyncio.gather(
        delay(1),
        delay(2),
        delay(3)
    )

asyncio.run(main())
