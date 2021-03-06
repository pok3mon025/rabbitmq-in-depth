import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'fanout-rpc-requests', exchange_type='fanout')
        exchange.declare()
