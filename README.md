# 🛑 Coal Mine Dust Detection System

A modular sensor data processing system for monitoring environmental parameters (like dust levels, gases, temperature) in coal mines. The system uses Python's multiprocessing shared memory to simulate real-time sensor data streaming, stores the readings via a Django REST API, and will be extended to include JSON-based storage and data computation services.

---

## 📌 Project Overview

This project simulates a sensor network where each sensor writes its readings into a shared memory segment. A reader service fetches these readings periodically and sends them to a Django REST API, which stores the data in a MySQL database. Additional independent services like **Historian** and **Alert Service** can access data via shared memory or JSON files.

---

## 📦 Features

- Real-time sensor data simulation using Python's `multiprocessing.shared_memory`
- Data transfer from shared memory to Django REST API
- Data persistence in a MySQL database
- REST endpoints for fetching all data and high dust level alerts
- Structured data packet handling (fixed byte structure)
- Modular, scalable design for adding Historian and Alert services later
- Logging for errors in data reading and API interactions
- Planned JSON-based tag storage and computational value processing