import os
import time
import random
import matplotlib.pyplot as plt

def create_test_file(file_path, size_in_mb):
    """Create a test file filled with random data."""
    with open(file_path, 'wb') as f:
        for _ in range(size_in_mb):
            f.write(os.urandom(1024 * 1024))

def measure_read_performance(file_path, access_size, iterations):
    """Measure the average read latency and bandwidth for a given access size."""
    latencies = []
    total_bytes = access_size * iterations
    file_size = os.path.getsize(file_path)
    start_time = time.perf_counter()
    with open(file_path, 'rb') as f:
        for _ in range(iterations):
            position = random.randint(0, file_size - access_size)
            f.seek(position)
            op_start = time.perf_counter_ns()
            f.read(access_size)
            op_end = time.perf_counter_ns()
            latency = op_end - op_start
            latencies.append(latency)
    end_time = time.perf_counter()
    total_time = end_time - start_time

    average_latency_ns = sum(latencies) / len(latencies)
    average_latency_us = average_latency_ns / 1000

    # Calculate bandwidth
    if access_size <= 65536:
        iops = iterations / total_time
        bandwidth = iops
    else:
        mb_transferred = total_bytes / (1024 * 1024)
        bandwidth = mb_transferred / total_time

    return average_latency_us, bandwidth

def experiment_effect_of_access_size_on_performance():
    """Run the experiment and plot the results."""
    file_path = 'test_file.bin'
    if not os.path.exists(file_path):
        print("Creating test file...")
        create_test_file(file_path, 200)

    access_sizes = [4096, 16384, 131072]
    iterations = 10000
    latencies_us = []
    bandwidths = []

    for access_size in access_sizes:
        avg_latency_us, bandwidth = measure_read_performance(file_path, access_size, iterations)
        print(f"Access Size: {access_size} bytes, Average Latency: {avg_latency_us:.2f} µs, Bandwidth: {bandwidth:.2f}")
        latencies_us.append(avg_latency_us)
        bandwidths.append(bandwidth)

    # Plotting Latency
    plt.figure()
    plt.plot(access_sizes, latencies_us, marker='o')
    plt.xlabel('Access Size (bytes)')
    plt.ylabel('Average Latency (µs)')
    plt.title('Effect of Access Size on Read Latency')
    plt.grid(True)
    plt.savefig('experiment1_access_size_latency.png')
    plt.show()

    # Plotting Bandwidth
    plt.figure()
    bandwidth_labels = []
    for size in access_sizes:
        if size <= 65536:
            bandwidth_labels.append('IOPS')
        else:
            bandwidth_labels.append('MB/s')
    plt.plot(access_sizes, bandwidths, marker='o')
    plt.xlabel('Access Size (bytes)')
    plt.ylabel('Bandwidth')
    plt.title('Effect of Access Size on Bandwidth')
    plt.grid(True)
    plt.savefig('experiment1_access_size_bandwidth.png')
    plt.show()

experiment_effect_of_access_size_on_performance()
