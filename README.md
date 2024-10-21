# SSD Performance Profiling

This repository contains a project that profiles SSD performance by measuring latency and bandwidth under various conditions.

## Overview

The project investigates how the following factors affect SSD performance:

- **Data Access Size**: 4KB, 16KB, 128KB
- **Read/Write Intensity Ratio**: 100% reads, 70% reads / 30% writes, 50% reads / 50% writes, 100% writes
- **I/O Queue Depth**: 1, 10, 100

## Contents

- `report.pdf`: The project report detailing the experiments and findings.
- `scripts/`: Custom Python scripts used for simulating I/O operations and collecting data.
- `figures/`: Graphs and figures generated from the experiments.
- `README.md`: This file.
