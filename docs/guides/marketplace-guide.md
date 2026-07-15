# Dronzer AI Marketplace Guide

Welcome to the Dronzer Marketplace! This ecosystem allows developers and organizations to discover, publish, and manage AI plugins, Agent templates, and system Prompts natively within the Dronzer Gateway.

## 1. Package Architecture
Every extension in Dronzer is distributed as a `.dzpkg` (Dronzer Package) archive. 
- It contains a `manifest.json` describing dependencies, Publisher namespace, and Semantic Version constraints (e.g. `>=1.2.0`).
- The `PackageEngine` strictly enforces Semantic Versioning.

## 2. Publishing & Security
Publishers (like `@google` or `@community`) upload packages via the Publisher Portal.
Before a package is accepted into the registry:
- **Digital Signatures**: The bundle is cryptographically verified to ensure it hasn't been tampered with.
- **Capabilities Scanner**: Dronzer scans the package for high-risk capabilities (like `network_raw_sockets` or `filesystem_write`). If found, it flags the package, ensuring the Sandbox Engine heavily restricts its runtime execution.

## 3. Dependency Resolution & Auto-Updates
Installing a package triggers the **Directed Acyclic Graph (DAG) Resolver**.
If you install a complex Agent Template, Dronzer will automatically recursively fetch all required Prompts and Tools it depends on, ensuring zero version conflicts.
The **AutoUpdateEngine** can gracefully upgrade packages in the background and instantly rollback if it detects a failure.

## 4. Enterprise Air-Gapped Mode
For highly secure, offline environments (e.g., Banks, Government), Dronzer supports an Air-Gapped Catalog.
IT Administrators can export `.tar.gz` bundles from the public web and physically import them into the Private Registry. An explicit **IT SecOps Approval Gate** ensures no AI Agent can execute unapproved software.
