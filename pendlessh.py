#!/usr/bin/env python3

import asyncio
import logging
import sys

from os import getenv
from aioprometheus import Counter, Gauge, Service
from random import randint
from socket import gethostname


logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)-15s %(levelname)-7s %(message)s ",
    level=logging.INFO,
)
log = logging.getLogger("pendlessh")


async def handler(_reader, writer):
    try:
        peername = writer.get_extra_info("peername")
        PromConnectionCounter.inc({"type": "total"})
        PromActiveConnectionGauge.inc({"type": "current"})
        log.info(f"Connection received from {peername}")

        while True:
            await asyncio.sleep(randint(0, MESSAGE_MAX_DELAY))
            writer.write(b"%x\r\n" % randint(0, 2 ** 32))

            if not writer.is_closing():
                await writer.drain()
            else:
                break

    except ConnectionResetError:
        pass

    PromActiveConnectionGauge.dec({"type": "current"})
    log.info(f"Client {peername} no longer connected")


async def main(PromServer: Service):

    await PromServer.start(addr="0.0.0.0", port=9191)
    server = await asyncio.start_server(handler, LISTEN_ADDRESS, LISTEN_PORT)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    LISTEN_PORT = getenv("PENDLESSH_PORT", default=22)
    LISTEN_ADDRESS = getenv("PENDLESSH_ADDRESS", default="0.0.0.0")
    MESSAGE_MAX_DELAY = int(getenv("PENDLESSH_MAX_DELAY", default=30))
    PROMETHEUS_HOSTNAME = getenv("PENDLESSH_PROMETHEUS_HOSTNAME", default=gethostname())

    log.info(
        f"Starting server on {LISTEN_ADDRESS}:{LISTEN_PORT}"
        f"with {MESSAGE_MAX_DELAY}s max delay"
    )

    const_labels = {
        "host": PROMETHEUS_HOSTNAME,
        "app": f"{sys.argv[0].split('/')[-1].replace('.py', '')}",
    }
    PromConnectionCounter = Counter(
        "pendlessh_connections",
        "Number of connections received",
        const_labels=const_labels,
    )
    PromActiveConnectionGauge = Gauge(
        "pendlessh_active_connections",
        "Number of currently active connections",
        const_labels=const_labels,
    )

    PromServer = Service()
    PromServer.register(PromConnectionCounter)
    PromServer.register(PromActiveConnectionGauge)

    asyncio.run(main(PromServer))
