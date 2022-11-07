#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_server import WebServer

buffer_size = 3         # param: K
arrival_rate = 10040       # param: lambda
service_frequency = 250  # param: mi
requests = 70        # param: N
n = 3

try:
    web_server = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                           buffer_size=buffer_size, arrival_rate=arrival_rate, service_frequency=service_frequency,
                           requests=requests, policy_type="shortest")
    web_server.show_queueing_model(n)
except ValueError as ve:
    print("\n[ERROR] -> {0}".format(ve))
