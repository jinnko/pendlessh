# A simple python implementation of an SSH tarpit using asyncio

Inspired by endlessh, this tool can be run in a container to tarpit SSH connections endlessly.

The prometheus metrics provide a view of currently active connections and total connections since
startup.

## Configuration options

Configuration can be done using environment variables.  See `pendlessh.env.sample` for available
parameters.  Copy the file to `pendlessh.env` prior to starting.

## Docker

When run in docker the script will run as the `nobody` user.  Ideally you'll also be using docker's
user namespace mapping feature on your deamon.

Another advantage of running within docker is you don't need to attach to port 22 and therefore
don't need any special privileges or capabilities.  Instead the docker layer can do the port
mapping from 22 on the host to 2222 in the container.

To start the service:

1. Copy `pendlessh.env.sample` to `pendlessh.env` and edit as needed
2. Start the service with `docker-compose up -d`

## Prometheus metrics

Two metrics are exposed:

- `pendlessh_connections_total` - counter of total connections
- `pendlessh_active_connections` - gauge of currently active connections
