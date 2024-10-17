#!/bin/bash

function run_benchmark() {
  if [[ -n $1 ]]; then
    python parallel_requests_benchmark/$1.py
  fi
}

function check_results() {
  if [[ -n $1 ]]; then
    no_of_results=$(cat  parallel_requests_benchmark.log | grep "INFO:parallel_requests_benchmark.$1:" | wc -l)
    echo -e "The number of results of $1 is : $no_of_results"
  fi
}

function check_requests() {
  if [[ -n $1 ]]; then
    no_of_requests=$(cat  parallel_requests_benchmark.log | grep "INFO:parallel_requests_benchmark.$1:Request completed successfully:" | wc -l)
    echo -e "The number of requests of $1 is : $no_of_requests"
  fi
}

function check_errors() {
  echo
  no_of_errors=$(cat  parallel_requests_benchmark.log | grep "ERROR:parallel_requests_benchmark.:" | wc -l)
  echo -e "The number of errors is : $no_of_errors"
}

function check_warnings() {
  echo
  no_of_warnings=$(cat  parallel_requests_benchmark.log | grep "WARNING:parallel_requests_benchmark.:" | wc -l)
  echo -e "The number of warnings is : $no_of_warnings"
}

# python -m venv py312
# python -m pip  install -r requirements.txt 
# python -m pip  install -U pip

rm -f parallel_requests_benchmark.log

source py312/bin/activate

run_benchmark test_synchronous_requests
run_benchmark test_synchronous_httpx
run_benchmark test_multiprocessing_requests
run_benchmark test_multithreading_requests
run_benchmark test_multithreading_httpx_single_event_loop
run_benchmark test_multithreading_httpx_multiple_event_loops
run_benchmark test_async_aiohttp_asyncio
run_benchmark test_async_aiohttp_anyio
run_benchmark test_async_httpx_asyncio
run_benchmark test_async_httpx_anyio

deactivate

check_errors
check_warnings
echo
check_results test_synchronous_requests
check_results test_synchronous_httpx
check_results test_multiprocessing_requests
check_results test_multithreading_requests
check_results test_multithreading_httpx_single_event_loop
check_results test_multithreading_httpx_multiple_event_loops
check_results test_async_aiohttp_asyncio
check_results test_async_aiohttp_anyio
check_results test_async_httpx_asyncio
check_results test_async_httpx_anyio
echo
check_requests test_synchronous_requests
check_requests test_synchronous_httpx
check_requests test_multiprocessing_requests
check_requests test_multithreading_requests
check_requests test_multithreading_httpx_single_event_loop
check_requests test_multithreading_httpx_multiple_event_loops
check_requests test_async_aiohttp_asyncio
check_requests test_async_aiohttp_anyio
check_requests test_async_httpx_asyncio
check_requests test_async_httpx_anyio


cat parallel_requests_benchmark.log | grep timer