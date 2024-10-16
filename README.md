# Parallel Request Benchmark

I had a need to understand the performance of the different python async packages for file download.
I started with requests and httpx SyncClient to define a baseline and then I looked at:
 - multiprocessing;
 - multithreading, both sync and async with httpx, single and multiple event loops;
 - asyncio, both aiohttp and httpx;
 - anyio, both aiohttp and httpx.

The execution time for a single run based on the average of 20 executions is:

| Test Name                                         | Duration   |
|---------------------------------------------------|------------|
| test_synchronous_requests                          | 0.208629   |
| test_synchronous_httpx                             | 0.231735   |
| test_multiprocessing_requests                      | 0.103449   |
| test_multithreading_requests                       | 0.065041   |
| test_multithreading_httpx_single_event_loop       | 0.031216   |
| test_multithreading_httpx_multiple_event_loops    | 0.056664   |
| test_async_aiohttp_asyncio                         | 0.000023   |
| test_async_aiohttp_anyio                           | 0.065789   |
| test_async_httpx_asyncio                           | 0.078591   |
| test_async_httpx_anyio                             | 0.088228   |


I stated from the initial work in [async-http-requests-tut](https://github.com/nikhilkumarsingh/async-http-requests-tut).

Making multiple HTTP requests using Python (synchronous, multiprocessing, multithreading, asyncio)

Watch tutorial video [here](https://www.youtube.com/watch?v=R4Oz8JUuM4s).

More tutorials:
- [Multiprocessing in Python](https://www.youtube.com/watch?v=Ju4xkvFm07o&list=PLyb_C2HpOQSDUh4kIJnprJjh5n5Wqsww8)
- [Multithreading in Python](https://www.youtube.com/watch?v=ZPM8TCz5cd8&list=PLyb_C2HpOQSC-Ncui9S4ncUdaGI2YEhwK)
- [Concurrent Programming in Python (asyncio)](https://www.youtube.com/watch?v=y85G7GLYhYA&list=PLyb_C2HpOQSBsygWeCYkJ7wjxXShIql43)
