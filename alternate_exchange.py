import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        my_ae = rabbitpy.Exchange(channel, 'my-ae',
                                  exchange_type='fanout')
        my_ae.declare()

        # Graphite 익스체인지의 대체 익스체인지를 지정하는 dict 정의
        args = {'alternate-exchange': my_ae.name}

        exchange = rabbitpy.Exchange(channel,
                                     'graphite',
                                     exchange_type='topic',
                                     arguments=args)
        exchange.declare()

        queue = rabbitpy.Queue(channel, 'unroutable-messages')
        queue.declare()
        # 큐와 대체 익스체인지 연결
        if queue.bind(my_ae, '#'):
            print('Queue bound to alternate-exchange')
