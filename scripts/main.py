#!/usr/bin/python
# -*- coding: utf-8 -*-

from web_server import WebServer

K = 6
lambda_ = 15
mi = 30
N = 30

web_server = WebServer(input_distribution_type="M", service_time_distribution_type="M", service_channels=1,
                       buffer_size=K, arrival_rate=lambda_, service_frequency=mi, requests=N, policy_type="random")

n = 3
print("\nProbability of {0} requests in the system = {1}".format(n, web_server.calculate_n_requests_probability(n)))
print("Normalized rejection rate = {0}".format(web_server.calculate_normalized_rejection_rate()))
print("Average requests number in the system = {0}".format(web_server.calculate_average_requests_number()))
print("Average system response time = {0}\n".format(web_server.calculate_average_response_time()))
web_server.show_queues()
