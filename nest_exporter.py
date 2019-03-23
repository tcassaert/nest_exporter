#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import http.client
import argparse
from urllib.parse import urlparse
from prometheus_client import start_http_server, Gauge, Metric
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class JsonCollector(object):
    def __init__(self):
        pass

    def collect(self):
        data = get_json()
        metric = Metric('nest_humidity', 'The humidity in the room', 'gauge')
        metric.add_sample('nest_humidity', value=data['humidity'], labels={})
        yield metric
    
        metric = Metric('nest_current_temp', 'The temperature in the room', 'gauge')
        metric.add_sample('nest_current_temp', value=data['ambient_temperature_c'], labels={})
        yield metric
    
        metric = Metric('nest_target_temp', 'The current target temperature', 'gauge')
        metric.add_sample('nest_target_temp', value=data['target_temperature_c'], labels={})
        yield metric
    
        if data['has_leaf']:
            has_leaf = 1
        else:
            has_leaf = 0
    
        metric = Metric('nest_eco_mode', 'Is the NEST in eco mode', 'gauge')
        metric.add_sample('nest_eco_mode', value=has_leaf, labels={})
        yield metric
    
        if data['hvac_state'] == 'off':
            heating = 0
        else:
            heating = 1
    
        metric = Metric('nest_heating_status', 'Is the NEST heating', 'gauge')
        metric.add_sample('nest_heating_status', value=heating, labels={})
        yield metric

def get_json():
    url = http.client.HTTPSConnection("developer-api.nest.com")
    headers = {'authorization': "Bearer {0}".format(bearer_token)}
    url.request("GET", "/", headers=headers)
    response = url.getresponse()

    if response.status == 307:
        redirectLocation = urlparse(response.getheader("location"))
        conn = http.client.HTTPSConnection(redirectLocation.netloc)
        conn.request("GET", "/devices/" + device_type + "/" + device_id, headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("Redirect with non 200 response")

    data = json.loads(response.read().decode('utf-8'))
    return data

def run_webserver():
    start_http_server(9601)
    REGISTRY.register(JsonCollector())
    while True: time.sleep(1)

def main():
    global bearer_token, device_id, device_type

    parser = argparse.ArgumentParser(usage="Python Prometheus json exporter to collect metrics from a Nest device")
    parser.add_argument("--type", action="store", default='thermostat', help="The Nest devide type (default: thermostat)")
    parser.add_argument("--id", action="store", help="The Nest device ID")
    parser.add_argument("--secret", action="store", help="The Nest API secret")
    parser.add_argument("-v", "--version", action="version", version="Nest Prometheus exporter v0.0.1")
    args = parser.parse_args()

    device_id = args.id
    device_type = args.type
    bearer_token = args.secret

    device_type = device_type + 's'

    run_webserver()

if __name__ == '__main__':
    main()
