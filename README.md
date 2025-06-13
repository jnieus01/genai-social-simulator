# GenAI Social Sim

> **Multi-Agent Generative AI Social Simulation Framework**

---

## 🚀 Project Inspiration & Vision

What happens when language models talk mostly to other language models?

As synthetic agents proliferate the internet—from customer‑service chatbots to covert Reddit commenters ([Undisclosed LLM bots on r/changemyview (2024‑2025)](https://www.404media.co/researchers-secretly-ran-a-massive-unauthorized-ai-persuasion-experiment-on-reddit-users))—the majority of online traffic could soon originate from machines. Understanding how Gen AI models influence one another is therefore a pressing research problem.

Some research has been done in this space already. For example, researchers developed a proposed simulator that can host 10 000+ generative agents and produce 5 million interactions in a sandbox city (see [AgentSociety (2025)](https://arxiv.org/abs/2502.08691)).

These events motivate a framework that is:

- **Lightweight & reproducible** – runs on a laptop with Docker + Redis so small labs (or solo practitioners) can explore multi‑agent dynamics.

- **Focused on agent‑to‑agent discourse** – every run is a closed loop of LLMs, letting researchers probe how prompt framing, network topology, or role authority drives collective behaviour—without any human interlocutors.

- **Transparent & fully auditable** – every prompt, parameter, and message is logged with timestamps and seeds, enabling rigorous replication, statistical analysis, and shareable datasets without ever involving real users.

---

## 🧱 Development Status

**This project is under active development and remains experimental.**  
Expect frequent updates, architecture changes, and ongoing enhancements as new capabilities are added.

---

## 🛠 Architecture Overview

`genai-social-sim` is a fully autonomous multi-agent LLM conversation system that uses:

- **Redis Pub/Sub backend** for real-time message coordination
- **Turn-taking orchestration** for controlled dialogue simulation
- **Multiple LLM-powered bots** that listen, generate, and respond in sequence
- **Analytics tracking** for measuring message counts, turn counts, response times, and processing behavior
- **CSV export utilities** to generate structured logs for offline analysis

---

## 🔧 Why Redis? (Strengths & Limitations)

The system currently uses **Redis Pub/Sub** as the backend message transport layer. Redis offers several advantages:

- Extremely fast publish-subscribe messaging
- Lightweight, simple architecture for quick prototyping
- Easy deployment via Docker
- Well-suited for real-time chat-like systems where message persistence isn't critical

However, Redis Pub/Sub also has important limitations:

- No message durability — messages are lost if a subscriber is unavailable or lagging
- No delivery guarantees across multiple consumers
- Coordination between multi-threaded agents requires careful queue management to avoid race conditions

One long-term goal for this project is to upgrade the backend to **Redis Streams** or a true message queue (Kafka, NATS, RabbitMQ) to ensure stronger delivery guarantees and better scaling for production-level multi-agent simulation.

---

## 🦙 Why Ollama?

Running large generative models locally used to mean heavyweight GPU servers or costly API calls. Using Ollama brings several benefits: 

**Full local control** - Tweak temperature, max‑tokens, top‑p, system prompts, or even swap model checkpoints without hitting rate limits.

**Model composability** - Ollama’s straightforward model registry simplifies mixing and matching model families (Gemma, Llama 3, etc.) to test prompt effects across diverse model behaviours.

**Rapid iteration** - No network latency; prompt changes reflect instantly, enabling tighter experiment loops.

**Lower energy & cost footprint** - Fine‑tune experiments on consumer GPUs or CPU‑only machines, pause containers when idle, and avoid thousands of remote‑inference calls during large agent sweeps.

**Privacy & compliance** - All conversation data stays on your machine, which is desirable for simulations that might ingest proprietary, classified, or sensitive datasets. 

---

## 🚀 How to Run the Project

### 0️⃣ Prerequisites

- [Docker](https://www.docker.com/)
- [Ollama](https://ollama.com/)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/genai-social-sim.git
cd genai-social-sim
````

### 2️⃣ Build the Docker containers

```bash
docker-compose up --build
```

This launches:

* Redis backend (port 6379)
* Application container

Enter the app container where you can execute python commands for steps 3-6 using this Docker command.

```bash
docker exec -it redis-python bash
```

### 3️⃣ Start the bots

In your main terminal (inside your app container), run:

```bash
python run_bots.py
```

This starts all configured bots.

### 4️⃣ Seed a conversation to start the simulation

In a separate terminal (inside your app container), run:

```bash
python utils/seed_conversation.py
```

This publishes an initial message to the Redis channel to trigger the first bot turn, which will begin the turn-based multi-agent conversations.

### 5️⃣ (Optional) Observe the conversation live

You can watch all published messages with:

```bash
python utils/channel_observer.py
```

### 6️⃣ Export analytics

After your simulation completes, export metrics to CSV:

```bash
python utils/export_analytics.py
```

This produces an `analytics_export.csv` containing bot-level analytics.

---

## 📊 Analytics Tracking

The system automatically collects:

* Message receipt counts
* Turn participation counts
* Response generation counts
* Processing latency (in seconds)
* Ignored messages (self-generated)

This data is exported into CSV for external analysis or research.

---

## ⚙ Technology Stack

* Python 3.11+
* Redis Pub/Sub backend
* Ollama for LLM inference (local/private LLM API)
* Docker & Docker Compose
* CSV-based analytics export
* Turn-based state coordination via Redis keys

---

## 🚀 Roadmap Highlights

* ✅ Current turn-based LLM-to-LLM conversations
* 🚧 Upgrade technology for durable coordination
* 🚧 Persona modeling extensions
* 🚧 Timeout and deadlock recovery for turn advancement
