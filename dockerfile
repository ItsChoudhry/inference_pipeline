FROM python:3.10-slim

WORKDIR /app

# Update package lists and install curl
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv \
    && uv --version

ENV PATH="/usr/local/bin:/root/.cargo/bin:$PATH"

COPY . .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


