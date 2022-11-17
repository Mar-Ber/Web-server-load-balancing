#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from queue import Queue, QueueShortest
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from math_utils import *


class WebServer:
    def __init__(self, input_distribution_type, service_time_distribution_type, service_channels, buffer_size,
                 arrival_rate, service_frequency, requests, policy_type):
        self.arrival_rate = arrival_rate
        self.service_frequency = service_frequency
        self.service_intensity = arrival_rate / (2 * service_frequency)
        self.buffer_size = buffer_size
        self.requests = requests
        self.policy_type = policy_type
        self.queues_number = 2
        self.input_distribution_type = input_distribution_type
        self.service_time_distribution_type = service_time_distribution_type

        self.requests_arrival_times = self.calculate_requests_arrival_times()
        self.requests_service_times = self.calculate_requests_service_times()
        # self.requests_service_times[0] = [x+0.1 for x in self.requests_service_times[0]] # Add servie time, needed to show bigger differences the types of queues

        # Create objects for queues class
        if self.policy_type == "random":
            self.queues = []
            for i in range(self.queues_number):
                self.queues.append(Queue(self.input_distribution_type, self.service_time_distribution_type,
                                         self.requests_arrival_times[i], self.requests_service_times[i],
                                         service_channels, buffer_size, arrival_rate/2,
                                         service_frequency, int(self.requests/2)))
        elif self.policy_type == "shortest":
            self.shortest_queues = [QueueShortest(service_channels),
                                    QueueShortest(service_channels)]
            self.calculate_shortest_queue_simulation()
        else:
            raise ValueError("Policy type = '{0}' is not supported.".format(self.policy_type))
 

    def calculate_shortest_queue_simulation(self):
        """ Function that simulates pre-queue buffer that separates requests between the queue with less number of requests """
        self.choice = [] # save which queue was choosen
        self.queue_size = [0]*int(self.requests/2) 
        self.queue_size2 = [0]*int(self.requests/2)

        for i in range(1, int(self.requests/2)):
            # on first iteration or at equal queues or condition in following if statement:
            if self.shortest_queues[0].queue_size <= self.shortest_queues[1].queue_size: 
                self.shortest_queues[0].simulate_shortest_queue(self.requests_arrival_times[0][i], self.requests_service_times[0][i], i)
                self.queue_size[i]=self.shortest_queues[0].queue_size
                self.queue_size2[i]=self.shortest_queues[1].queue_size
                self.choice.append("1")
            else:
                self.choice.append("2")
                self.shortest_queues[1].simulate_shortest_queue(self.requests_arrival_times[0][i], self.requests_service_times[0][i], i)
                self.queue_size2[i]=self.shortest_queues[1].queue_size
                self.queue_size[i]=self.shortest_queues[0].queue_size


    def calculate_requests_arrival_times_for_random_policy(self):
        if self.input_distribution_type == "M":
            requests_period = (-np.log(np.random.rand(1, int(self.requests/self.queues_number)))
                               / (self.arrival_rate/self.queues_number))[0]
            return (np.cumsum(requests_period)).tolist()


    def calculate_requests_service_time_for_random_policy(self):
        if self.input_distribution_type == "M":
            return (-np.log(np.random.rand(1, int(self.requests/self.queues_number))) /
                    self.service_frequency)[0].tolist()
      

    def calculate_requests_arrival_times(self):
        result = []
        for _ in range(self.queues_number):
            result.append(self.calculate_requests_arrival_times_for_random_policy())
        return result
      

    def calculate_requests_service_times(self):
        result = []
        for _ in range(self.queues_number):
            result.append(self.calculate_requests_service_time_for_random_policy())
        return result
      

    def show_shortest_queue_plots(self):
        plt.figure(0)
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        # add star to plot to explain what was the choice, which queue was choosen in each iteration
        list_choice = [self.queue_size[i] if choice == '1' else self.queue_size2[i] for i, choice in enumerate(self.choice)]
    
        plt.plot(range(1, int(self.requests/2)+1), self.queue_size)
        plt.plot(range(1, int(self.requests/2)+1), self.queue_size2)
        plt.plot(range(1, int(self.requests/2)), list_choice, "r*")
        plt.title("Queue size")
        plt.xlabel("Processed request")
        plt.ylabel("Value")
        plt.savefig("./data_output/shortest.png")
        plt.show()



    def show_random_queue_plots(self):
       for i, queue in enumerate(self.queues):
                if i == self.queues_number-1:
                    queue.plot_queue(should_show=True)
                else:
                    queue.plot_queue(should_show=False)
                print("Queue {0} -> {1}".format(i+1, queue))

    def show_plots(self):
        if self.policy_type == "random":
            self.show_random_queue_plots()
        elif self.policy_type == "shortest":
            self.show_shortest_queue_plots()
        else:
            raise ValueError("Policy type = '{0}' is not supported.".format(self.policy_type))


    def show_math_info(self, n):
        if self.policy_type == "random":
            print("\nProbability of {0} requests in the system = {1}".
                                        format(n, calculate_n_requests_probability(n, self.buffer_size, self.service_intensity)))
            print("Normalized rejection rate = {0}".
                                        format(calculate_normalized_rejection_rate(self.buffer_size, self.service_intensity)))
            print("Average requests number in the system = {0}".
                                        format(calculate_average_requests_number(self.buffer_size, self.service_intensity)))
            print("Average system response time = {0}\n".
                                        format(calculate_average_response_time(self.buffer_size, self.service_intensity, self.arrival_rate)))
        else:
            raise ValueError("Policy type = '{0}' is not supported.".format(self.policy_type))
