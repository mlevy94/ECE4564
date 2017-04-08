from aiocoap import *
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

class MinecraftResource(resource.Resource):


    def __init__(self):
        super(MinecraftResource, self).__init__()
#        self.add_param(resource.LinkParam("title", "Large resource."))

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = "current location in minecraft:"  # needs to be filled out

        return aiocoap.Message(payload=payload)

    async def render_put(self, request):

        print('POST payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in " \
                 "Python's repr format:\n\n%r" % self.content).encode('utf8')
        return aiocoap.Message(payload=payload)


    logging.basicConfig(level=logging.INFO)
    logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(('Main', 'Minecraft'), MinecraftResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


    if __name__ == "__main__":
        main()