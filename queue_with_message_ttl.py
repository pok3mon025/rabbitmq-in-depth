import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'expiring-msg-queue', arguments={'x-message-ttl': 1000})
        queue.declare()
