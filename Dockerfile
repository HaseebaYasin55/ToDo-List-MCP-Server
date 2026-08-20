# Dockerfile
# ----------
# Glama builds every listed server from a Dockerfile — either one you provide
# (this one) or one it infers automatically from your project structure.
# Providing our own keeps the build predictable and beginner-readable.

FROM python:3.12-slim

WORKDIR /app

# Copy dependency list first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# This server speaks MCP over stdio (standard input/output),
# so it has no network port to expose — the MCP client starts
# this process directly and talks to it over stdin/stdout.
CMD ["python", "server.py"]