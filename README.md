# Content Delivery Network (CDN) Simulator & Implementation

## Overview
A robust project demonstrating the core principles of a Content Delivery Network (CDN). It includes HTTP proxying, dynamic DNS routing based on load/proximity, and network simulation environments.

## Architecture
- **DNS Server** (`dns/`): Custom DNS implementation to route clients to the optimal edge server.
- **HTTP Proxy** (`starter_proxy/`): Caching proxy servers handling client video/web requests.
- **Simulation Environment** (`netsim/`): Tools to emulate network topologies, latency, and bandwidth constraints using Mininet/Click.
- **Docker Setup**: Infrastructure configurations for deploying the CDN nodes.

## Setup & Usage
1. Configure your network topologies in `netsim/`.
2. Start the proxy nodes using the Python scripts in `starter_proxy/` (e.g., `proxy1.py`).
3. Launch the DNS server to begin intelligently routing traffic.

*(Note: Requires a Linux environment capable of running Mininet/Docker for full topology simulation).*

## Highlights
- Implements active load balancing and geographic routing logic.
- Adaptive Bitrate (ABR) video streaming support.
- Extensive logging and graphing tools (`grapher.py`) for performance analysis (utilization, fairness, smoothness).

## Limitations
- Primarily designed as an academic/simulation project rather than a production-ready global CDN.
- Docker and Mininet setups require specific host environments and privileges.
