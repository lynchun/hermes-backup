#!/usr/bin/env python3
"""Hermes API server — standalone launcher for Open WebUI integration.

Usage:
  # DeepSeek backend
  HERMES_INFERENCE_PROVIDER=deepseek  # REQUIRED: without this defaults to openai-codex
  API_SERVER_PORT=8642
  API_SERVER_KEY=local-dev
  API_SERVER_MODEL_NAME="Epictetus"
  DEEPSEEK_API_KEY=sk-xxx
  python3 hermes-api-server.py

  # Codex backend (vision-capable but model-name-sensitive)
  HERMES_INFERENCE_PROVIDER=openai-codex  # May fail with model-not-supported error
  API_SERVER_PORT=8643
  python3 hermes-api-server.py
"""
import os, sys, asyncio

sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))

os.environ.setdefault('API_SERVER_PORT', '8642')
os.environ.setdefault('API_SERVER_HOST', '0.0.0.0')
os.environ.setdefault('API_SERVER_KEY', 'local-dev')
os.environ.setdefault('API_SERVER_MODEL_NAME', 'Epictetus')

from gateway.config import PlatformConfig

async def main():
    provider = os.environ.get('HERMES_INFERENCE_PROVIDER', '(not set — will use openai-codex default)')
    port = os.environ['API_SERVER_PORT']
    model_name = os.environ['API_SERVER_MODEL_NAME']
    print(f'Starting API server: provider={provider} port={port} model="{model_name}"')
    
    config = PlatformConfig(enabled=True)
    from gateway.platforms.api_server import APIServerAdapter
    adapter = APIServerAdapter(config)
    success = await adapter.connect()
    if success:
        print(f'API server running on port {port}!')
        while True:
            await asyncio.sleep(3600)
    else:
        print('Failed to start. Check HERMES_INFERENCE_PROVIDER is set correctly.')
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
