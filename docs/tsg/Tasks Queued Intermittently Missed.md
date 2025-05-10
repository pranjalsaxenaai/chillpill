# Issue
Enqueued 7 tasks using delay
```
res1 = adder.delay(267,5)
res2 = adder.delay(268,5)
res3 = adder.delay(269,5)
res4 = adder.delay(270,5)
res5 = adder.delay(271,5)
res6 = adder.delay(272,5)
res7 = adder.delay(273,5)
```

The queued task res2 was getting missed by the celery worker and res2.get() throws error 'Not Registered'

# Investigation
1. Check the running workers by running in powershell   
```
celery -A mycelerymodule inspect active 
```

2. If there are multiple nodes (workers) with same name running for same celery app, this will create confusion amongst workers.

# Solution
1. Stop all workers in powershell
```
celery -A mycelerymodule control shutdown
```
2. Clear Redis Entries by running this command in interactive shell in docker container
```
redis-cli FLUSHALL
```
3. Start the new worker
```
celery -A mycelerymodule worker --loglevel=info -P solo
```

