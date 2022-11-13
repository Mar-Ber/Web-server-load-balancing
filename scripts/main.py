#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_server import WebServer


buffer_size = 3         # param: K
arrival_rate = 20      # param: lambda
service_frequency = 30 # param: mi
requests = 80   # param: N
n = 3 # number of requests that the script calculates math info about queue


try:
    web_server = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                           buffer_size=buffer_size, arrival_rate=arrival_rate, service_frequency=service_frequency,
                           requests=requests, policy_type="shortest")
    web_server2 = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                           buffer_size=buffer_size, arrival_rate=arrival_rate, service_frequency=service_frequency,
                           requests=requests, policy_type="random")
    # Show math info
    web_server2.show_math_info(n)

    # Show plots for each type of queue
    web_server.show_plots()
    web_server2.show_plots()
except ValueError as ve:
    print("\n[ERROR] -> {0}".format(ve))
