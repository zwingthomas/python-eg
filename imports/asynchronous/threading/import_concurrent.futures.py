# Acknowledgements____
# Corey Schafer
# Python Threading Tutorial: Run Code Concurrently Using the Threading Module
# https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1381s&ab_channel=CoreySchafer

"""
This is the new way of doing threading. It is much simpler and even
allows you to switch over to mutliprocessing within the same objects.

# TODO: Locks, semaphores, all that jazz. A write up with the various
        important aspects of threading that is more advanced than this.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests

from import_threading import do_something_thread_executor as do_something_thread_executor, timer


@timer
def simple():
    with ThreadPoolExecutor() as executor:
        f1 = executor.submit(do_something_thread_executor, 1)
        f2 = executor.submit(do_something_thread_executor, 1)
        print(f1.result())
        print(f2.result())


@timer
def loop():
    with ThreadPoolExecutor() as executor:
        seconds = [5, 4, 3, 2, 1]
        results = [executor.submit(do_something_thread_executor, x)
                   for x in seconds]

        # This will output as they complete
        for f in as_completed(results):
            print(f.result())


@timer
def map_method():
    with ThreadPoolExecutor() as executor:
        seconds = [5, 4, 3, 2, 1]
        results = executor.map(do_something_thread_executor, seconds)

        # This will output in the order they were started
        for result in results:
            print(result)


img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]


@timer
def download_images():

    for img_url in img_urls:
        img_bytes = requests.get(img_url).content
        img_name = img_url.split('/')[3]
        img_name = f'{img_name}.jpg'
        with open(img_name, 'wb') as img_file:
            img_file.write(img_bytes)
            print(f'{img_name} was downloaded...')

    for img_url in img_urls:
        try:
            img_name = img_url.split('/')[3]
            img_name = f'{img_name}.jpg'
            os.remove(img_name)
            print(f"{img_name} was deleted")
        except OSError as err:
            print(f"Could not delete {img_name}: {err}")


def download_images_thread(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[3]
    img_name = f'{img_name}.jpg'
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} was downloaded...')

    try:
        img_name = img_url.split('/')[3]
        img_name = f'{img_name}.jpg'
        os.remove(img_name)
        print(f"{img_name} was deleted")
    except OSError as err:
        print(f"Could not delete {img_name}: {err}")


@timer
def download_images_thread_pool():
    with ThreadPoolExecutor() as executor:
        executor.map(download_images_thread, img_urls)


if __name__ == "__main__":
    simple()
    loop()
    map_method()
    download_images()
    download_images_thread_pool()
