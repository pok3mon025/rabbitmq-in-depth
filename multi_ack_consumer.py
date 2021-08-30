import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        channel.prefetch_count(10)
        unacknowledged = 0
        for message in rabbitpy.Queue(channel, 'test-messages'):
            message.pprint()
            unacknowledged += 1
            if unacknowledged == 10:
                message.ack(all_previous=True)
                unacknowledged = 0
