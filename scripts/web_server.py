#!/usr/bin/python
# -*- coding: utf-8 -*-

from queue import Queue


class WebServer:
    def __init__(self, input_distribution_type, service_time_distribution_type, service_channels, buffer_size,
                 arrival_rate, service_time, requests):
        self.queue = Queue(input_distribution_type, service_time_distribution_type, service_channels, buffer_size,
                           arrival_rate, service_time, requests)

    def show_queue(self):
        self.queue.show_queue_size()
        print(self.queue)
