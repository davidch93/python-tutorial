import concurrent.futures
import datetime
from time import sleep


def return_after_n_secs(seconds, message):
    sleep(seconds)
    return message


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_task1 = executor.submit(return_after_n_secs, 3, "Hello")
        future_task2 = executor.submit(return_after_n_secs, 6, "World")
        print('Start time: ' + str(datetime.datetime.today()))
        # print('Wait until task 1 & 2 done.')
        # print('Task 1 (' + future_task1.result() + ') done.')
        # print('Wait until task 2 done')
        # print('Task 2 (' + future_task2.result() + ') done.')
        print(future_task1.result() + ' ' + future_task2.result())
        print('End time: ' + str(datetime.datetime.today()))


if __name__ == '__main__':
    main()
