#!/usr/bin/python
# -*- coding: utf-8 -*-

from queue import Queue


class WebServer:
    def __init__(self, input_distribution_type, service_time_distribution_type, service_channels, buffer_size,
                 arrival_rate, service_frequency, requests, policy_type):
        self.arrival_rate = arrival_rate
        self.service_frequency = service_frequency
        self.service_intensity = arrival_rate / (2 * service_frequency)
        self.buffer_size = buffer_size
        self.queues = []
        self.policy_type = policy_type

        if self.policy_type == "random":
            for _ in range(2):
                self.queues.append(Queue(input_distribution_type, service_time_distribution_type, service_channels,
                                         buffer_size, arrival_rate/2, service_frequency, requests))

    def calculate_n_requests_probability(self, n):
        if self.policy_type == "random":
            if 0 <= n <= self.buffer_size and self.service_intensity != 1:
                result = (1-self.service_intensity) * (self.service_intensity ** n) / \
                         (1-self.service_intensity ** (self.buffer_size+1))
                return round(result, 4)
            else:
                raise ValueError("Calculation not supported")

    def calculate_normalized_rejection_rate(self):
        if self.policy_type == "random":
            return self.calculate_n_requests_probability(n=self.buffer_size)

    def calculate_average_requests_number(self):
        if self.policy_type == "random":
            if int(self.service_intensity) == 1:
                result = self.buffer_size / 2
                return round(result, 4)
            else:
                result = self.service_intensity / (1-self.service_intensity) - \
                         ((self.buffer_size+1) * (self.service_intensity ** (self.buffer_size+1)) /
                          (1-(self.service_intensity ** (self.buffer_size+1))))
                return round(result, 4)

    def calculate_average_response_time(self):
        if self.policy_type == "random":
            result = 2 * self.calculate_average_requests_number() * (1-self.service_intensity ** (self.buffer_size+1)) / \
                     (self.arrival_rate * (1 - self.service_intensity ** self.buffer_size))
            return round(result, 4)

    def show_queues(self):
        for queue in self.queues:
            queue.show_queue_size()
            print(queue)
