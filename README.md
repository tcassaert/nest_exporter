# Prometheus Nest Exporter

## Introduction

This project contains a Python script that can be used to extract some metrics that get exposed on the API endpoint of your Nest thermostat. The script acts as a Prometheus exporter and can be scraped by Prometheus itself. 

## The exporter

The exporter is written in Python and uses the [Prometheus Python client][0]. Currently it only supports the Nest Thermostat and the following metrics:

  * humidity
  * ambient_temperature_c
  * target_temperature_c
  * has_leaf
  * hvac_state

### Prerequisites

The exporter is written in Python 3, and has not been tested for backwards compatibility with Python 2, so it is advised to invoke the exporter with Python 3. 

To let the script use your Nest Thermostat, you'd need a Nest Developer Account. You can find instructions on how to create an account [here][1].

A lot of the following steps use Docker, so you might want to install that as well, but it's not required to make use of the exporter.

### Standalone usage

The script can be simply invoked with

```
nest_exporter.py --type=$DEVICE_TYPE --id=$DEVICE_ID --secret=$SECRET
```

This starts the simple webserver from which Prometheus can fetch its metrics. 

### Running in a container

This repo contains an example Dockerfile to provide the ability to run the `nest_exporter` in a container. 

You can build the image with 

```
docker build -t nest_exporter .
```

from the root of this repository. This will include the `docker-entrypoint.sh` script, which is used to start the exporter and provide it with necessary credentials. 

When the container image build is done, you can start the container with

```
docker run -d -p 9601:9601 -e DEVICE_ID=$DEVICE_ID -e SECRET=$SECRET --name=nest_exporter nest_exporter
```

This uses the environment variables that contain the credentials for your Nest Thermostat. 
## Prometheus

We are now already exposing metrics about our Nest Thermostat, now we need something that can scrape and store those metrics. This is where [Prometheus][2] comes into the picture. 

This repository contains a very minimal `prometheus.yaml` configuration file. 

To run Prometheus in a container, you can issue

```
docker run -d --user 1234:5678 -p 9090:9090 -v $(pwd)/prometheus_data:/prometheus -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml --name prometheus prom/prometheus
```

Now Prometheus should start scraping the metrics of your `nest_exporter`.

## Grafana

We are now collecting metrics, but there's no use in collecting metrics, if you can't see them anywhere. Luckily, we have [Grafana][3] for this.

Grafana can also run in a simple container:

```
docker run -d --user 472:472 -p 3000:3000 -v $(pwd)/grafana_data:/var/lib/grafana --name=grafana grafana/grafana
```

I've provided a sample dashboard to show the collected metrics:

![Example Grafana Dashboard][grafana_dashboard]

This dashboard requires you to have setup Prometheus as data source for Grafana.

[0]: https://github.com/prometheus/client_python
[1]: https://codelabs.developers.google.com/codelabs/wwn-api-quickstart
[2]: https://prometheus.io/
[3]: https://grafana.com/
[grafana_dashboard]: https://github.com/tcassaert/nest_exporter/images/dashboard.png
