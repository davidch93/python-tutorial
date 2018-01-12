from concurrent.futures import ThreadPoolExecutor
from time import sleep


def return_after_5_secs(message):
    sleep(5)
    return message


def main():
    # The ThreadPoolExecutor is better suited for network operations or I/O.
    pool = ThreadPoolExecutor(3)
    future = pool.submit(return_after_5_secs, "hello")
    print(future.done())
    sleep(5)
    print(future.done())
    print(future.result())


if __name__ == '__main__':
    main()
