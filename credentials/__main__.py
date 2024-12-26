import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    from uvicorn import run
    run('api:api', host='0.0.0.0', port=8001, log_level='info')