import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'durable-queue', durable=True)
        if queue.declare():
            print('Queue declared')
