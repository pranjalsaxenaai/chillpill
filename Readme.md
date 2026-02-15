# How to Setup
1. Start terminal in chillpill directory
    ```
    .\setup.ps1
    ```
2. Install Docker
3. Pull Redis Image
    ```
    docker pull redis
    ```
4. Run Redis Server
    ```
    docker run --name redis -p 6379:6379 -d redis # This will create a docker container and start it.

    docker start redis # Run an already created container

    ```

#  How to run
1. Start 3 terminals in chillpill directory
2. Run venv\scripts\Activate.ps1 in all terminals
3. In first terminal, run Python Chill Pill API
    ```
    cd api
    py manage.py runserver
    ```
    This runs the django API server.

4. In second terminal, run langgraph local server
    ```
    cd langgraph-server
    langgraph dev
    ```
    This will run the langgraph server locally on URL http://127.0.0.1:2024

5. In third terminal, run the UI Server
    ```
    cd ui\chillpillui
    npm run dev
    ```
    

# How to Test Langgraph
1. Open 2 Terminals in chillpill directory
2. Run venv\scripts\Activate.ps1 in all terminals
3. In first terminal, run Python Chill Pill API, because langraph internally sends requests to ChillPill API for storing data in DB.
    ```
    cd api
    py manage.py runserver
    ```
4. In second terminal, run langgraph local server
    ```
    cd langgraph-server
    langgraph dev
    ```
    This will run the langgraph server locally on URL http://127.0.0.1:2024
5. Use experiments\langgraph\langgraph.ipynb for sending calls to the local langgraph server.

# [DEPRECATED] How to run
1. Start 3 terminals in chillpill directory
2. Run venv\scripts\Activate.ps1 in all terminals
3. In All terminals 
    ```
    cd api
    ```
3. In first terminal, run 
    ```
    celery -A api worker --loglevel=info -P solo # For a single thread in one worker
    celery -A api worker --loglevel=info --concurrency=10 --pool=gevent # For 10 concurrent gevent threads
    ```
    This needs to run first, to start the celery worker for background tasks.
4. In second terminal, run
    ```
    celery -A api flower
    ```
    This needs to run second, to activate a UI for managing celery worker.
5. In third terminal, run
    ```
    py manage.py runserver
    ```
    This runs the django API server.
