import logging
import asyncio

from aiocoap import Context, Message, PUT, GET

logging.basicConfig(level=logging.INFO)

async def mine_get():

    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://localhost/Main/Minecraft')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: {0}\n{1}'.format(response.code, response.payload))

async def mine_put():

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"update minecraft with put\n"
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '127.0.0.1'
    request.opt.uri_path = ("Main", "Minecraft")

    response = await context.request(request).response

    print('Result: {0}\n{1}'.format(response.code, response.payload))

async def main():

#    await mine_get()
    await mine_put()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
