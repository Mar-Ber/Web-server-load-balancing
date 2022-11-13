def calculate_n_requests_probability(n, buffer_size, service_intensity):
    if 0 <= n <= buffer_size and service_intensity != 1:
        result = (1-service_intensity) * (service_intensity ** n) / \
                    (1-service_intensity ** (buffer_size+1))
        return round(result, 4)
    else:
        raise ValueError("Calculation not supported")

def calculate_normalized_rejection_rate(buffer_size, service_intensity):
    return calculate_n_requests_probability(buffer_size, buffer_size, service_intensity)

def calculate_average_requests_number(buffer_size, service_intensity):
    if int(service_intensity) == 1:
        result = buffer_size / 2
        return round(result, 4)
    else:
        result = service_intensity / (1-service_intensity) - \
                         ((buffer_size+1) * (service_intensity ** (buffer_size+1)) /
                          (1-(service_intensity ** (buffer_size+1))))
        return round(result, 4)

def calculate_average_response_time(buffer_size, service_intensity, arrival_rate):
    result = 2 * calculate_average_requests_number(buffer_size, service_intensity) * (1-service_intensity**(buffer_size+1)) / \
                     (arrival_rate * (1 - service_intensity ** buffer_size))
    return round(result, 4)
   