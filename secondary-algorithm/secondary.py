#!/usr/bin/env/ python3

import asyncio
from asyncio import StreamReader, StreamWriter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_PORT = 8888


async def handle_echo(reader: StreamReader, writer: StreamWriter):
    data = await reader.readline()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logger.info(f"Received {message!r} from {addr!r}")

    logger.info(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    logger.info("Close the connection")
    writer.close()


async def main(port=DEFAULT_PORT):
    logger.info('Starting secondary algorithm')
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', port)

    addr = server.sockets[0].getsockname()
    logger.info(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
