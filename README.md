# A simple python implementation of an SSH tarpit using asyncio

Inspired by endlessh, this tool can be run in a container to tarpit SSH connections endlessly.

The prometheus metrics provide a view of currently active connections and total connections since
startup.

## Configuration options

Configuration can be done using environment variables.

Environment variable | Default | Description
--- | --- | ---
PENDLESSH_ADDRESS | 0.0.0.0 | IP to listen on
PENDLESSH_PORT | 2222 | Port to listen on
PENDLESSH_MAX_DELAY | 30 | A random delay between 0 and this value between short messages

## Docker

When run in docker the script will run as the `nobody` user.  Ideally you'll also be using docker's
user namespace mapping feature on your deamon.

## Prometheus metrics

Two metrics are exposed:

- pendlessh_connections_total - counter of total connections
- pendlessh_active_connections - gauge of currently active connections
