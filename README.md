## Quick Start with Docker

The easiest way to run and evaluate both is using Docker Compose.

### Prerequisites

- Docker and Docker Compose installed
- No other dependencies needed

### Run Demos (Interactive)

**IMPORTANT:** For interactive demos, use `docker-compose run`:

```bash
# Producer-Consumer (Interactive)
docker-compose run --rm producer-consumer

# CSV Analysis (Interactive)
docker-compose run --rm csv-analysis
```

Or use the helper scripts:
```bash
# Producer-Consumer
./run-producer-consumer.sh

# CSV Analysis
./run-csv-analysis.sh
```

### Run Tests

Run all tests for both :
```bash
docker-compose --profile test up
```

Run tests for individual :
```bash
# Test 1
docker-compose --profile test up test-producer-consumer

# Test 2
docker-compose --profile test up test-csv-analysis
```

### Clean Up

Remove containers and images:
```bash
docker-compose down
docker-compose down --rmi all  # Also remove images
```

## Manual Setup (Without Docker)

If you prefer to run without Docker:

### 1: Producer-Consumer

```bash
cd producer-consumer
python3 -m venv venv
source venv/bin/activate
python examples/demo.py
python -m unittest discover tests
```

### 2: CSV Analysis

```bash
cd csv-analysis
python3 -m venv venv
source venv/bin/activate
pip install pandas
python examples/demo.py
python -m unittest discover tests
```

## Project Structure

```
tuitin/
├── docker-compose.yml           # Docker orchestration
├── producer-consumer/           #  1
│   ├── Dockerfile
│   ├── main.py                  # API entry point
│   ├── src/                     # Core implementation
│   ├── tests/                   # Unit tests (53 tests)
│   ├── examples/                # Demo usage
│   └── README.md
└── csv-analysis/                #  2
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py                  # API entry point
    ├── src/                     # Core implementation
    ├── data/                    # Sales dataset
    ├── tests/                   # Unit tests (43 tests)
    ├── examples/                # Demo usage
    └── README.md
```

###  Producer-Consumer Pattern

Demonstrates thread synchronization using:
- Threading with concurrent execution
- Condition variables for wait/notify mechanism
- Thread-safe shared buffer
- Blocking queue behavior

**Test Coverage:** 53 unit tests

See [producer-consumer/README.md](producer-consumer/README.md) for details.

### CSV Data Analysis

Demonstrates functional programming with:
- Lambda expressions for predicates and mappers
- Filter, map, reduce operations
- Stream processing and aggregation
- Time-series analysis

**Test Coverage:** 43 unit tests

See [csv-analysis/README.md](csv-analysis/README.md) for details.

## Docker Image Sizes

Both images are optimized for size:
- Based on `python:3.11-slim`
- Multi-layer caching for faster rebuilds
- Non-root user for security
- Minimal dependencies
