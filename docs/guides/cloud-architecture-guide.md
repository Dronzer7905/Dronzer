# Dronzer Cloud-Native Architecture Guide

Welcome to the Global Infrastructure layer of Dronzer. This guide explains how Dronzer operates as a distributed, multi-region platform capable of handling enterprise-grade disaster recovery, high availability, and dynamic scaling.

## 1. Global Topology & Consensus
Dronzer organizes compute into **Clusters** and **Nodes**.
- **Nodes** continuously pulse heartbeats to the central database. If a node misses a heartbeat, the Service Registry evicts it.
- **Consensus**: To prevent Split-Brain scenarios across global regions, Dronzer utilizes a Distributed Lock Manager (backed by Redis) to ensure that only ONE node is designated as the `Leader`. The Leader is responsible for orchestrating background jobs and triggering failovers.

## 2. Dynamic Routing & Service Discovery
The `GlobalRouter` acts as an intelligent L7 proxy.
When an incoming AI request or API call arrives, the Router interrogates the `ServiceRegistry`. It can dynamically route traffic to specific regions based on:
- **Compliance**: Forcing EU requests to stay in EU data centers.
- **Hardware**: Routing GPU-heavy model inference directly to nodes labeled with GPU capabilities.
- **Latency/Cost**: Weighted round-robin across the cheapest available compute regions.

## 3. High Availability (HA) & Disaster Recovery (DR)
- **Failover**: The `FailoverController` constantly monitors cross-cluster health. If `aws-us-east` goes offline, it automatically promotes `gcp-eu-central` to `PRIMARY`, instructing the Global Router to bleed traffic away from the dead zone.
- **Snapshots**: Dronzer performs automated point-in-time snapshots of both PostgreSQL (Config/Metadata) and Qdrant (Vector Embeddings) pushing them to S3. In the event of catastrophic failure, the `DisasterRecoveryEngine` can restore the entire platform state.

## 4. Kubernetes Operator
For enterprise deployments, Dronzer includes a Python-based Kubernetes Operator (`kopf`). 
Administrators can deploy Dronzer by applying a simple `DronzerCluster` Custom Resource Definition (CRD). The operator automatically negotiates ReplicaSets, Deployments, and Horizontal Pod Autoscalers based on traffic load.
