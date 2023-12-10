import asyncio

async def display_num():
    for i in range(8):
        print(i)
        await asyncio.sleep(1)

    
asyncio.run(display_num())