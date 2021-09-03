import rabbitpy
import time

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'exclusive-example', arguments={'x-expires': 1000})
        queue.declare()
        messages, consumers = queue.declare(passive=True)
        time.sleep(2)
        try:
            messages, consumers = queue.declare(passive=True)
        except rabbitpy.exceptions.AMQPNotFound:
            print('The queue no longer exists')
