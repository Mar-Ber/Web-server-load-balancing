#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_server import WebServer

buffer_size = 6         # param: K
arrival_rate = 30       # param: lambda
service_frequency = 20  # param: mi
requests = 60           # param: N
n = 3

try:
    web_server = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                           buffer_size=buffer_size, arrival_rate=arrival_rate, service_frequency=service_frequency,
                           requests=requests, policy_type="random")
    web_server.show_queueing_model(n)
except ValueError as ve:
    print("\n[ERROR] -> {0}".format(ve))
