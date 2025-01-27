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
    docker run --name redis -p 6379:6379 -d redis
    ```

# How to run
1. Start 3 terminals in chillpill directory
2. Run venv\scripts\Activate.ps1 in all terminals
3. In All terminals 
    ```
    cd api
    ```
3. In first terminal, run 
    ```
    celery -A api worker --loglevel=info -P solo
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
