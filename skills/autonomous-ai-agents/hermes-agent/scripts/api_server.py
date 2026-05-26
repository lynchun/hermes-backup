#!/usr/bin/env python3
"""Standalone Hermes API Server — provider and model configurable via env vars.

Usage:
    HERMES_INFERENCE_PROVIDER=deepseek API_SERVER_MODEL_NAME="Epictetus" \\
      API_SERVER_PORT=8642 API_SERVER_HOST=0.0.0.0 API_SERVER_KEY=local-dev \\
      python3 /path/to/api_server.py

    HERMES_INFERENCE_PROVIDER=openai-codex API_SERVER_MODEL="gpt-5.3-codex" \\
      API_SERVER_PORT=8643 API_SERVER_MODEL_NAME="Epictetus (Codex)" \\
      API_SERVER_HOST=0.0.0.0 API_SERVER_KEY=local-dev \\
      python3 /path/to/api_server.py
"""
import os, sys, asyncio
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))

provider = os.environ.get('HERMES_INFERENCE_PROVIDER', 'deepseek')
model = os.environ.get('API_SERVER_MODEL', '')
port = os.environ.get('API_SERVER_PORT', '8642')
model_name = os.environ.get('API_SERVER_MODEL_NAME', 'Epictetus')
api_key_env = os.environ.get('API_SERVER_KEY', 'local-dev')
host = os.environ.get('API_SERVER_HOST', '0.0.0.0')

os.environ['API_SERVER_PORT'] = port
os.environ['API_SERVER_HOST'] = host
os.environ['API_SERVER_KEY'] = api_key_env
os.environ['HERMES_INFERENCE_PROVIDER'] = provider

if model:
    config_path = os.path.expanduser('~/.hermes/config.yaml')
    import yaml
    with open(config_path) as f:
        cfg = yaml.safe_load(f) or {}
    old_model = cfg.get('model', {}).get('default', '')
    if 'model' not in cfg:
        cfg['model'] = {}
    cfg['model']['default'] = model
    with open(config_path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False)
    os.environ['_API_SERVER_RESTORE_MODEL'] = old_model

from gateway.config import PlatformConfig

async def main():
    config = PlatformConfig(enabled=True)
    from gateway.platforms.api_server import APIServerAdapter
    adapter = APIServerAdapter(config)
    print(f'Starting: {model_name} ({provider}:{model or "default"}) on :{port}')
    success = await adapter.connect()
    print(f'Connected: {success}')
    if success:
        print(f'API server running: {model_name}')
        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            old = os.environ.pop('_API_SERVER_RESTORE_MODEL', '')
            if old:
                import yaml
                config_path = os.path.expanduser('~/.hermes/config.yaml')
                with open(config_path) as f:
                    cfg = yaml.safe_load(f) or {}
                if 'model' not in cfg:
                    cfg['model'] = {}
                cfg['model']['default'] = old
                with open(config_path, 'w') as f:
                    yaml.dump(cfg, f, default_flow_style=False)
                print(f'Restored model to: {old}')
    else:
        print('Failed to start')

if __name__ == '__main__':
    asyncio.run(main())
