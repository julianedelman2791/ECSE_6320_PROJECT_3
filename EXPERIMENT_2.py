import os
import time
import random
import matplotlib.pyplot as plt

def create_test_file(file_path, size_in_mb):
    """Create a test file filled with random data."""
    with open(file_path, 'wb') as f:
        for _ in range(size_in_mb):
            f.write(os.urandom(1024 * 1024))

def measure_read_write_performance(file_path, access_size, iterations, read_ratio):
    """Measure average latency and bandwidth based on read/write ratio."""
    latencies = []
    total_bytes = access_size * iterations
    file_size = os.path.getsize(file_path)
    num_reads = int(iterations * read_ratio)
    num_writes = iterations - num_reads

    start_time = time.perf_counter()
    with open(file_path, 'r+b') as f:
        # Perform reads
        for _ in range(num_reads):
            position = random.randint(0, file_size - access_size)
            f.seek(position)
            op_start = time.perf_counter_ns()
            f.read(access_size)
            op_end = time.perf_counter_ns()
            latency = op_end - op_start
            latencies.append(latency)

        # Perform writes
        for _ in range(num_writes):
            position = random.randint(0, file_size - access_size)
            f.seek(position)
            data_to_write = os.urandom(access_size)
            op_start = time.perf_counter_ns()
            f.write(data_to_write)
            op_end = time.perf_counter_ns()
            latency = op_end - op_start
            latencies.append(latency)
    end_time = time.perf_counter()
    total_time = end_time - start_time

    average_latency_ns = sum(latencies) / len(latencies)
    average_latency_us = average_latency_ns / 1000

    # Calculate bandwidth in IOPS (since access size is 4KB)
    iops = iterations / total_time
    bandwidth = iops

    return average_latency_us, bandwidth

def experiment_effect_of_read_write_ratio_on_performance():
    """Run the experiment and plot the results."""
    file_path = 'test_file.bin'
    access_size = 4096
    iterations = 10000
    read_write_ratios = [1.0, 0.7, 0.5, 0.0]
    latencies_us = []
    bandwidths = []

    # Check if test file exists, create if it doesn't
    if not os.path.exists(file_path):
        print("Test file not found. Creating test file...")
        create_test_file(file_path, 200)

    for ratio in read_write_ratios:
        avg_latency_us, bandwidth = measure_read_write_performance(file_path, access_size, iterations, ratio)
        print(f"Read Ratio: {ratio*100:.0f}%, Average Latency: {avg_latency_us:.2f} µs, Bandwidth (IOPS): {bandwidth:.2f}")
        latencies_us.append(avg_latency_us)
        bandwidths.append(bandwidth)

    # Plotting Latency
    ratios_percent = [int(r*100) for r in read_write_ratios]
    plt.figure()
    plt.plot(ratios_percent, latencies_us, marker='o')
    plt.xlabel('Read Percentage (%)')
    plt.ylabel('Average Latency (µs)')
    plt.title('Effect of Read/Write Ratio on Latency')
    plt.grid(True)
    plt.savefig('experiment2_read_write_ratio_latency.png')
    plt.show()

    # Plotting Bandwidth (IOPS)
    plt.figure()
    plt.plot(ratios_percent, bandwidths, marker='o')
    plt.xlabel('Read Percentage (%)')
    plt.ylabel('Bandwidth (IOPS)')
    plt.title('Effect of Read/Write Ratio on Bandwidth')
    plt.grid(True)
    plt.savefig('experiment2_read_write_ratio_bandwidth.png')
    plt.show()

experiment_effect_of_read_write_ratio_on_performance()
