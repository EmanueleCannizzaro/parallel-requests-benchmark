# Parallel Request Benchmark

I had a need to understand the performance of the different python async packages for file download.
I started with requests and httpx SyncClient to define a baseline and then I looked at:
 - multiprocessing,
 - multithreading, both sync and async with httpx, single and multiple event loops
 - asyncio, both aiohttp and httpx
 - anyio, both aiohttp and httpx

I stated from the initial work in [async-http-requests-tut]().

Making multiple HTTP requests using Python (synchronous, multiprocessing, multithreading, asyncio)

Watch tutorial video [here](https://www.youtube.com/watch?v=R4Oz8JUuM4s).

More tutorials:
- [Multiprocessing in Python](https://www.youtube.com/watch?v=Ju4xkvFm07o&list=PLyb_C2HpOQSDUh4kIJnprJjh5n5Wqsww8)
- [Multithreading in Python](https://www.youtube.com/watch?v=ZPM8TCz5cd8&list=PLyb_C2HpOQSC-Ncui9S4ncUdaGI2YEhwK)
- [Concurrent Programming in Python (asyncio)](https://www.youtube.com/watch?v=y85G7GLYhYA&list=PLyb_C2HpOQSBsygWeCYkJ7wjxXShIql43)
