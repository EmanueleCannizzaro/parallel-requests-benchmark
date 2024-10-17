The execution time for a single run is:

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
