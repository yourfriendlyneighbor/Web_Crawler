import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = input('What will your project name be? ') #'thenewboston'
HOMEPAGE = input('What will your project homepage be? Ex: https://example.com ') #'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = int(input('How many threads will there be? Recommended: 8 ')) #8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # Will die when main exits
        t.start()

# Each Queue Links is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# Check if there a items in the queue, if so crawl them
def crawl():
    queued_Links = file_to_set(QUEUE_FILE)
    if len(queued_Links) > 0:
        print(str(len(queued_Links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()
