#!/bin/bash

run_benchmark() {
  if [[ $1 != "" ]]; then
    python parallel_requests_benchmark/$1.py
  fi
}

check_results() {
  if [[ $1 != "" ]]; then
    no_of_results=$(cat  parallel_requests_benchmark.log | grep "DEBUG:parallel_requests_benchmark.$1:" | wc -l)
    echo -e "The number of results of $1 is : $no_of_results"
  fi
}

# python -m venv py312
# python -m pip  install -r requirements.txt 
# python -m pip  install -U pip

# rm parallel_requests_benchmark.log

source py312/bin/activate

run_benchmark test_synchronous
run_benchmark test_synchronous_httpx
run_benchmark test_multiprocessing
run_benchmark test_multithreading
run_benchmark test_async_aiohttp_asyncio
run_benchmark test_async_aiohttp_anyio
run_benchmark test_async_httpx_asyncio
run_benchmark test_async_httpx_anyio

deactivate

check_results test_synchronous
check_results test_synchronous_httpx
check_results test_multiprocessing
check_results test_multithreading
check_results test_async_aiohttp_asyncio
check_results test_async_aiohttp_anyio
check_results test_async_httpx_asyncio
check_results test_async_httpx_anyio

cat parallel_requests_benchmark.log | grep timer