#!/usr/bin/env python3
"""Start Hermes API server - provider and model configurable via env vars."""
import os, sys, asyncio, yaml
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))

provider = os.environ.get('HERMES_INFERENCE_PROVIDER', 'deepseek')
model = os.environ.get('API_SERVER_MODEL', '')
port = os.environ.get('API_SERVER_PORT', '8642')
model_name = os.environ.get('API_SERVER_MODEL_NAME', 'Epictetus')
api_key = os.environ.get('API_SERVER_KEY', 'local-dev')
host = os.environ.get('API_SERVER_HOST', '0.0.0.0')

os.environ['API_SERVER_PORT'] = port
os.environ['API_SERVER_HOST'] = host
os.environ['API_SERVER_KEY'] = api_key
os.environ['API_SERVER_MODEL_NAME'] = model_name
os.environ['HERMES_INFERENCE_PROVIDER'] = provider

from gateway.config import PlatformConfig

async def main():
    # Temporarily set model in config if API_SERVER_MODEL is specified
    if model:
        config_path = os.path.expanduser('~/.hermes/config.yaml')
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        old_model = cfg.get('model', {}).get('default', '')
        if 'model' not in cfg:
            cfg['model'] = {}
        cfg['model']['default'] = model
        with open(config_path, 'w') as f:
            yaml.dump(cfg, f, default_flow_style=False)
        os.environ['_API_SERVER_RESTORE_MODEL'] = old_model

    config = PlatformConfig(enabled=True)
    from gateway.platforms.api_server import APIServerAdapter
    adapter = APIServerAdapter(config)
    print(f'Connecting API server ({provider}:{model or "default"}) on port {port}...')
    success = await adapter.connect()
    print(f'Connected: {success}')
    if success:
        print('API server running!')
        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            old = os.environ.pop('_API_SERVER_RESTORE_MODEL', '')
            if old:
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
