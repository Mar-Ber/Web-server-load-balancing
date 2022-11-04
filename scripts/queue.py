#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class Queue:
    def __init__(self, input_distribution_type, service_time_distribution_type, service_channels, buffer_size,
                 arrival_rate, service_frequency, requests):
        self.input_distribution_type = input_distribution_type
        self.service_time_distribution_type = service_time_distribution_type
        self.service_channels = service_channels
        self.buffer_size = buffer_size
        self.arrival_rate = arrival_rate
        self.service_frequency = service_frequency
        self.requests = requests

        self.requests_arrival_times = self.calculate_requests_arrival_times()
        self.requests_service_time = self.calculate_requests_service_time()
        self.queue_size = None

    def calculate_requests_arrival_times(self):
        if self.input_distribution_type == "M":
            requests_period = (-np.log(np.random.rand(1, self.requests))/self.arrival_rate)[0]
            return (np.cumsum(requests_period)).tolist()
        else:
            raise ValueError("Input distribution type = {0} is not supported".format(self.input_distribution_type))

    def calculate_requests_service_time(self):
        return (-np.log(np.random.rand(1, self.requests))/self.service_frequency)[0].tolist()

    def simulate_queue(self):
        if self.service_channels == 1:
            service_start = self.requests_arrival_times[0]
            requests_exit_time = [service_start+self.requests_service_time[0]]
            self.queue_size = [0]*self.requests
            for i in range(1, self.requests):
                service_start = max(requests_exit_time[i-1], self.requests_arrival_times[i])
                if service_start > self.requests_arrival_times[i]:
                    self.queue_size[i] = self.queue_size[i-1] + 1
                elif self.queue_size[i-1] > 0:
                    self.queue_size[i] = self.queue_size[i-1] - 1
                requests_exit_time.append(service_start + self.requests_service_time[i])
        else:
            raise ValueError("Service channels = {0} is not supported".format(self.service_channels))

    def show_queue_size(self):
        if self.queue_size is None:
            self.simulate_queue()
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(range(1, self.requests+1), self.queue_size, marker="o")
        plt.title("Queue size")
        plt.xlabel("n")
        plt.ylabel("value")
        plt.show()

    def __repr__(self):
        return f"<Queue ---{self.input_distribution_type}/{self.service_time_distribution_type}/" \
               f"{self.service_channels}/FIFO/{self.buffer_size}--- " \
               f"(lambda={self.arrival_rate}, mi={self.service_frequency}, N={self.requests})>"
