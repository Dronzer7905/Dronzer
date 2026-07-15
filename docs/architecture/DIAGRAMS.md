# Dronzer v2.0 Architecture Diagrams

This document contains Mermaid diagrams illustrating the core architecture, sequence flows, and deployment topologies of the Dronzer Platform.

## 1. High-Level Architecture
```mermaid
graph TD
    Client["Client Applications (SDKs, APIs)"]
    Gateway["Dronzer AI Gateway (FastAPI)"]
    Router["Multi-Provider Router"]
    PromptOps["PromptOps Engine (Jinja2)"]
    Workflows["DAG Workflow Engine"]
    Cache["Semantic Cache (Redis)"]
    DB["Enterprise DB (Postgres 15+)"]
    
    OpenAI["OpenAI"]
    Anthropic["Anthropic"]
    Local["Local Models (Ollama)"]

    Client -->|REST / GraphQL| Gateway
    Gateway --> Cache
    Gateway --> PromptOps
    Gateway --> Workflows
    PromptOps --> Router
    Workflows --> Router
    
    Router --> OpenAI
    Router --> Anthropic
    Router --> Local
    
    Gateway --> DB
```

## 2. Sequence Diagram: Prompt Execution & A/B Testing
```mermaid
sequenceDiagram
    participant App as Client Application
    participant GW as Dronzer Gateway
    participant Cache as Redis Cache
    participant DB as Postgres DB
    participant Engine as ABExperimentEngine
    participant LLM as LLM Provider

    App->>GW: execute_prompt("support-bot", vars)
    GW->>Cache: check_cache(vars)
    alt Cache Hit
        Cache-->>GW: Cached Response
        GW-->>App: Cached Response
    else Cache Miss
        GW->>DB: fetch_prompt("support-bot")
        DB-->>GW: Prompt Versions (Champion & Challenger)
        GW->>Engine: route_traffic()
        Engine-->>GW: Selected Version (Challenger)
        GW->>GW: Compile Jinja2 Template
        GW->>LLM: execute(Compiled Template)
        LLM-->>GW: LLM Output
        GW->>Cache: set_cache(Output)
        GW-->>App: LLM Output
    end
```

## 3. Kubernetes Multi-Cluster Deployment Topology
```mermaid
graph TD
    subgraph "Region: US-East"
        LB1["Load Balancer"]
        GWEast1["Gateway Node 1"]
        GWEast2["Gateway Node 2"]
        RedisEast["Redis (Rate Limit / PubSub)"]
    end
    
    subgraph "Region: EU-West"
        LB2["Load Balancer"]
        GWEU1["Gateway Node 1"]
        RedisEU["Redis"]
    end
    
    DB["Global Postgres Database (Multi-AZ)"]
    GlobalLB["Global DNS / Traffic Manager"]
    
    GlobalLB --> LB1
    GlobalLB --> LB2
    
    LB1 --> GWEast1
    LB1 --> GWEast2
    
    LB2 --> GWEU1
    
    GWEast1 --> RedisEast
    GWEast2 --> RedisEast
    GWEU1 --> RedisEU
    
    GWEast1 --> DB
    GWEast2 --> DB
    GWEU1 --> DB
```
