# Simple Python-based IBM Cloud Activity Tracker - MS Sentinel Bridge

This very simple app:
- Reads messages from an IBM Cloud Event Streams topic
- Publishes received message "as-is" to MS Sentinel using Rest API

## Prerequisites

- A Mezmo-based instance (LogDNA, Sysdig or Activity Tracker) on IBM Cloud
- An Event Streams instance on IBM Cloud
- Mezmo configuration to stream messages to Event Streams

## Setup

### Python prerequisites

You need Python3 and `pip` to install dependencies. For apt-based Linux:
```sh
apt install python3 python3-pip
```

You also need to install module dependencies (use a virtual env if applicable):
```sh
pip install -r requirements.txt
```

### Application setup

You must obtain:
- From Event Streams credentials:
  - The Event Streams bootstrap servers list
  - The Event Streams API Key  
- From MS Sentinel (Agents > Log Analytics agent instructions):
  - Sentinel Workspace ID
  - Sentinel authentication (primary or secondary key)

The value for `MS_SENTINEL_LOG_TYPE` can be freely chosen, e.g. `IBMCloudLogDNA`.

Export the following environment variables:
```sh
export EVENT_STREAMS_BOOTSTRAP_SERVERS=...
export EVENT_STREAMS_API_KEY=...
export MS_SENTINEL_WORKSPACE_ID=...
export MS_SENTINEL_AUTH_KEY=...
export MS_SENTINEL_LOG_TYPE=...
```

Finally run the app:
```sh
python3 main.py
```
