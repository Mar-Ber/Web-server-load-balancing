#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_server import WebServer

K = 2
lambda_ = 15
mi = 30
N = 30

web_server = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                       buffer_size=K, arrival_rate=lambda_, service_time=mi, requests=N)
web_server.show_queue()
