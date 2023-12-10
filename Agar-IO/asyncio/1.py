
import asyncio

async def handler():
    await asyncio.sleep(2)
    print("Hello World")

asyncio.run(handler())

"""
import asyncio

async def print_delayed_message():
    await asyncio.sleep(2)  # Wait for 2 seconds
    print("Python Exercises!")

# Create an event loop and run the asynchronous function
async def main():
    await print_delayed_message()

# Run the event loop
asyncio.run(main())
"""