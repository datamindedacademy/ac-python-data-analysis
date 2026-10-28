ARG DEBIAN_CODENAME=bookworm
ARG PYTHON_VERSION=3.14
ARG NODE_VERSION=24
ARG UV_VERSION=0.13.6
ARG PNPM_VERSION=12.15.0

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv
FROM node:${NODE_VERSION}-${DEBIAN_CODENAME}-slim AS node

FROM mcr.microsoft.com/devcontainers/python:${PYTHON_VERSION}-${DEBIAN_CODENAME}

# Install uv
COPY --from=uv /uv /uvx /usr/local/bin/

# Install node and npm
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

# Install pnpm
ARG PNPM_VERSION
RUN npm install -g pnpm@${PNPM_VERSION}

# Chromium, for PDF export of the slides (make pdf)
RUN apt-get update \
 && apt-get install -y --no-install-recommends chromium \
 && rm -rf /var/lib/apt/lists/*

# Venv outside the project folder, so it never clashes with a host .venv
# (in case it's a different OS)
ENV UV_PYTHON_PREFERENCE=only-system \
    UV_PROJECT_ENVIRONMENT=/home/vscode/.venv \
    PATH="/home/vscode/.venv/bin:${PATH}"
