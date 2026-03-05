# EmbodiedAI-Core Dockerfile
# Multi-stage build for development and production

# =============================================================================
# Stage 1: Base Image with CUDA
# =============================================================================
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    git \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# =============================================================================
# Stage 2: Development Image
# =============================================================================
FROM base AS development

# Create virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .

# Install dependencies (including dev)
RUN pip install -e ".[dev,docs]"

# Copy source code
COPY . .

# Default command
CMD ["bash"]

# =============================================================================
# Stage 3: Production Image
# =============================================================================
FROM base AS production

# Create virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .

# Install only production dependencies
RUN pip install --no-cache-dir embodiedai-core

# Copy only necessary files
COPY src/ /app/src/
COPY config/ /app/config/

# Create non-root user
RUN useradd -m -u 1000 embodiedai && \
    chown -R embodiedai:embodiedai /app
USER embodiedai

WORKDIR /app

# Default command
CMD ["python", "-c", "import embodiedai; print(f'EmbodiedAI-Core v{embodiedai.__version__}')"]

# =============================================================================
# Stage 4: GPU-Enabled Simulation
# =============================================================================
FROM production AS simulation

# Install additional simulation dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    libosmesa6-dev \
    libgl1-mesa-glx \
    libglfw3 \
    && rm -rf /var/lib/apt/lists/*

USER embodiedai

# Install simulation extras
RUN pip install --no-cache-dir embodiedai-core[simulation]

CMD ["bash"]
