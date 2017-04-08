import logging
import asyncio
import aiocoap

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def mine_get():

    protocol = await Context.create_client_context()

    request = Message(code=aiocoap.Get, uri='coap://localhost/Main/Minecraft')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

async def mine_put():

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = "update minecraft with put"
    request = Message(code=aiocoap.PUT, payload=payload)
    request.opt.uri_host = 'coap://localhost'
    request.opt.uri_path = ("Main", "Minecraft")

    response = await context.request(request).response

    print('Result: %s\n%r' % (response.code, response.payload))

async def main():
    
    await mine_get()
    await mine_put()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())