#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class Queue:
    def __init__(self, input_distribution_type, service_time_distribution_type,
                 requests_arrival_times, requests_service_times, service_channels,
                 buffer_size, arrival_rate, service_frequency, requests):
        self.input_distribution_type = input_distribution_type
        self.service_time_distribution_type = service_time_distribution_type
        self.service_channels = service_channels
        self.buffer_size = buffer_size
        self.arrival_rate = arrival_rate
        self.service_frequency = service_frequency
        self.requests = requests

        self.requests_arrival_times = requests_arrival_times
        self.requests_service_times = requests_service_times
        self.queue_size = None

    def simulate_queue(self):
        if self.service_channels == 1:
            service_start = self.requests_arrival_times[0]
            requests_exit_time = [service_start+self.requests_service_times[0]]
            self.queue_size = [0]*self.requests
            print(self.requests)
            for i in range(1, self.requests):
                service_start = max(requests_exit_time[i-1], self.requests_arrival_times[i])
                if service_start > self.requests_arrival_times[i]:
                    self.queue_size[i] = self.queue_size[i-1] + 1
                elif self.queue_size[i-1] > 0:
                    self.queue_size[i] = self.queue_size[i-1] - 1
                requests_exit_time.append(service_start + self.requests_service_times[i])
        else:
            raise ValueError("Service channels = {0} is not supported".format(self.service_channels))

    def plot_queue(self, should_show=True):
        if self.queue_size is None:
            self.simulate_queue()
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(range(1, self.requests+1), self.queue_size, marker="o")
        plt.title("Queue size")
        plt.xlabel("n")
        plt.ylabel("value")
        if should_show:
            plt.show()

    def __repr__(self):
        return f"<Queue ---{self.input_distribution_type}/{self.service_time_distribution_type}/" \
               f"{self.service_channels}/FIFO/{self.buffer_size}--- " \
               f"(lambda={self.arrival_rate}, mi={self.service_frequency}, N={self.requests})>"


class QueueShortest:
    def __init__(self, service_channels, requests):
        self.service_channels = service_channels
        self.first_time = True
        self.service_start = None
        # self.queue_size = [0]*requests
        self.requests = requests
        self.requests_exit_time = None
        self.iterator = 0
    def simulate_shortest_queue(self, request_arrival_time, request_service_time, i):
        if self.service_channels == 1:
            if self.first_time is True:
                self.service_start = request_arrival_time
                self.requests_exit_time = [self.service_start+ request_service_time]
                self.first_time = False
                self.iterator+=1

                print("1 itaracja ")
            else:
                print("h: ", self.requests_exit_time)
                print("a: ", request_arrival_time)
                # print("q ", self.queue_size)
                self.service_start = max(self.requests_exit_time[-1], request_arrival_time)
                if self.service_start > request_arrival_time:
                    # self.queue_size[i] = self.queue_size[i-1] + 1
                    self.iterator+=1

                    print("Do gory kolejka")
                elif self.iterator > 0:
                    # self.queue_size[i] = self.queue_size[i-1] - 1
                    self.iterator-=1
                    print("W dol kolejka")

                        
                self.requests_exit_time.append(self.service_start + request_service_time)

        else:
            raise ValueError("Service channels = {0} is not supported".format(self.service_channels))

    def plot_queue(self, should_show=True):
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(range(1, self.requests+1), self.queue_size, marker="o")
        plt.title("Queue size")
        plt.xlabel("n")
        plt.ylabel("value")
        if should_show:
            plt.show()

    # def __repr__(self):
    #     return f"<Queue ---{}/{self.service_time_distribution_type}/" \
    #            f"{self.service_channels}/FIFO/{self.buffer_size}--- " \
    #            f"(lambda={self.arrival_rate}, mi={self.service_frequency}, N={self.requests})>"
