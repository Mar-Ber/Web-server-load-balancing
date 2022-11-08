#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from queue import Queue, QueueShortest
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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
        self.requests_service_times[0] = [x+0.1 for x in self.requests_service_times[0]]
        self.queues = []
        self.choice = []


        if self.policy_type == "random":
            for i in range(self.queues_number):
                self.queues.append(Queue(self.input_distribution_type, self.service_time_distribution_type,
                                         self.requests_arrival_times[i], self.requests_service_times[i],
                                         service_channels, buffer_size, arrival_rate/2,
                                         service_frequency, int(requests/2)))
        elif self.policy_type == "shortest":
            self.shortest_queues = [QueueShortest(service_channels, int(requests/2)),
                                    QueueShortest(service_channels, int(requests/2))]

            ########
            print(self.requests_arrival_times[0])
            print(self.requests_service_times[0])
            self.queue_size = [0]*int(requests/2)
            self.queue_size2 = [0]*int(requests/2)

            for i in range(1, int(requests/2)):
                if i == 1:
                    print("Kolejka nr 1", i)
                    self.shortest_queues[0].simulate_shortest_queue(self.requests_arrival_times[0][i], self.requests_service_times[0][i], i)
                    self.queue_size[i]=self.shortest_queues[0].iterator
                    self.queue_size2[i]=self.shortest_queues[1].iterator
                    self.choice.append("1")
                else:

                    if self.shortest_queues[0].iterator <= self.shortest_queues[1].iterator:
                        print("Kolejka nr 1")

                        self.shortest_queues[0].simulate_shortest_queue(self.requests_arrival_times[0][i], self.requests_service_times[0][i], i)
                        self.queue_size[i]=self.shortest_queues[0].iterator
                        self.queue_size2[i]=self.shortest_queues[1].iterator
                        self.choice.append("1")
                    else:
                        print("Kolejka nr 2")
                        self.choice.append("2")
                        self.shortest_queues[1].simulate_shortest_queue(self.requests_arrival_times[0][i], self.requests_service_times[0][i], i)
                        self.queue_size2[i]=self.shortest_queues[1].iterator
                        self.queue_size[i]=self.shortest_queues[0].iterator


            print(self.queue_size, self.queue_size2)
            # QueueShortest(request_arrival_time, request_service_time,
            #                              service_channels, request)]
            ########
        else:
            print("fajne te kolejki")

    def calculate_n_requests_probability(self, n):
        if self.policy_type == "random":
            if 0 <= n <= self.buffer_size and self.service_intensity != 1:
                result = (1-self.service_intensity) * (self.service_intensity ** n) / \
                         (1-self.service_intensity ** (self.buffer_size+1))
                return round(result, 4)
            else:
                raise ValueError("Calculation not supported")
        else:
            raise ValueError("Policy type = '{0}' is not supported".format(self.policy_type))

    def calculate_normalized_rejection_rate(self):
        if self.policy_type == "random":
            return self.calculate_n_requests_probability(n=self.buffer_size)
        else:
            raise ValueError("Policy type = '{0}' is not supported".format(self.policy_type))

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
        else:
            raise ValueError("Policy type = '{0}' is not supported".format(self.policy_type))

    def calculate_average_response_time(self):
        if self.policy_type == "random":
            result = 2 * self.calculate_average_requests_number() * (1-self.service_intensity**(self.buffer_size+1)) / \
                     (self.arrival_rate * (1 - self.service_intensity ** self.buffer_size))
            return round(result, 4)
        else:
            raise ValueError("Policy type = '{0}' is not supported".format(self.policy_type))

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
        if self.policy_type == "shortest":
            for _ in range(self.queues_number):
                result.append(self.calculate_requests_arrival_times_for_random_policy())
            return result
      

    def calculate_requests_service_times(self):
        result = []
        if self.policy_type == "shortest":
            for _ in range(self.queues_number):
                result.append(self.calculate_requests_service_time_for_random_policy())
            return result
      

    def print_calculated_values(self, n):
        if self.policy_type == "random":
            print("\nProbability of {0} requests in the system = {1}".format(n,
                                                                             self.calculate_n_requests_probability(n)))
            print("Normalized rejection rate = {0}".format(self.calculate_normalized_rejection_rate()))
            print("Average requests number in the system = {0}".format(self.calculate_average_requests_number()))
            print("Average system response time = {0}\n".format(self.calculate_average_response_time()))
        else:
            raise ValueError("Policy type = '{0}' is not supported".format(self.policy_type))

    def plot_queues(self):
        if self.policy_type == "random":
            for i, queue in enumerate(self.queues):
                if i == self.queues_number-1:
                    queue.plot_queue(should_show=True)
                else:
                    queue.plot_queue(should_show=False)
                print("Queue {0} -> {1}".format(i+1, queue))
        else:
            for i, queue in enumerate(self.shortest_queues):
                if i == self.queues_number-1:
                    queue.plot_queue(should_show=True)
                else:
                    queue.plot_queue(should_show=False)
                print("Queue {0} -> {1}".format(i+1, queue))
    
    def plot_nasze(self):
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        print(self.choice)
        wektor_wyborow = []
        for i, choice in enumerate(self.choice):
            if choice == '1':
                wektor_wyborow.append(self.queue_size[i])
            else:
                wektor_wyborow.append(self.queue_size2[i])

        plt.plot(range(1, int(self.requests/2)+1), self.queue_size)
        plt.plot(range(1, int(self.requests/2)+1), self.queue_size2)
        plt.plot(range(1, int(self.requests/2)), wektor_wyborow, "r*")
        plt.title("Queue size")
        plt.xlabel("n")
        plt.ylabel("value")
        plt.show()

    

    def show_queueing_model(self, n=5):
        # self.print_calculated_values(n)
        # self.plot_queues()
        self.plot_nasze()
