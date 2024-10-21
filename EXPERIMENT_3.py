import os
import time
import random
import threading
import matplotlib.pyplot as plt

def create_test_file(file_path, size_in_mb):
    """Create a test file filled with random data."""
    with open(file_path, 'wb') as f:
        for _ in range(size_in_mb):
            f.write(os.urandom(1024 * 1024))

def read_operation(file_path, access_size, file_size, latencies):
    """Perform a single read operation and record latency."""
    with open(file_path, 'rb') as f:
        position = random.randint(0, file_size - access_size)
        f.seek(position)
        op_start = time.perf_counter_ns()
        f.read(access_size)
        op_end = time.perf_counter_ns()
        latency = op_end - op_start
        latencies.append(latency)

def measure_performance_with_queue_depth(file_path, access_size, iterations, queue_depth):
    """Measure latency and bandwidth with a given queue depth."""
    latencies = []
    total_bytes = access_size * iterations * queue_depth
    file_size = os.path.getsize(file_path)
    start_time = time.perf_counter()
    for _ in range(iterations):
        threads = []
        for _ in range(queue_depth):
            t = threading.Thread(target=read_operation, args=(file_path, access_size, file_size, latencies))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    end_time = time.perf_counter()
    total_time = end_time - start_time

    average_latency_ns = sum(latencies) / len(latencies)
    average_latency_us = average_latency_ns / 1000

    # Calculate bandwidth in IOPS
    total_operations = iterations * queue_depth
    iops = total_operations / total_time
    bandwidth = iops

    return average_latency_us, bandwidth

def experiment_effect_of_queue_depth_on_performance():
    """Run the experiment and plot the results."""
    file_path = 'test_file.bin'
    access_size = 4096
    iterations = 100
    queue_depths = [1, 10, 100]
    latencies_us = []
    bandwidths = []

    # Check if test file exists, create if it doesn't
    if not os.path.exists(file_path):
        print("Test file not found. Creating test file...")
        create_test_file(file_path, 200)

    for depth in queue_depths:
        avg_latency_us, bandwidth = measure_performance_with_queue_depth(file_path, access_size, iterations, depth)
        print(f"Queue Depth: {depth}, Average Latency: {avg_latency_us:.2f} µs, Bandwidth (IOPS): {bandwidth:.2f}")
        latencies_us.append(avg_latency_us)
        bandwidths.append(bandwidth)

    # Plotting Latency
    plt.figure()
    plt.plot(queue_depths, latencies_us, marker='o')
    plt.xlabel('Queue Depth')
    plt.ylabel('Average Latency (µs)')
    plt.title('Effect of I/O Queue Depth on Latency')
    plt.grid(True)
    plt.savefig('experiment3_queue_depth_latency.png')
    plt.show()

    # Plotting Bandwidth (IOPS)
    plt.figure()
    plt.plot(queue_depths, bandwidths, marker='o')
    plt.xlabel('Queue Depth')
    plt.ylabel('Bandwidth (IOPS)')
    plt.title('Effect of I/O Queue Depth on Bandwidth')
    plt.grid(True)
    plt.savefig('experiment3_queue_depth_bandwidth.png')
    plt.show()

experiment_effect_of_queue_depth_on_performance()
