import pika
import bcrypt
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='jobs')


# fungsi yang dieksekusi ketika mendapat pesan
def callback(ch, method, properties, body):
    parsed_json = json.loads(body)
    hashed = parsed_json['password'].encode('utf-8')
    sequences = [w.encode('utf-8') for w in parsed_json['input_sequences']]
    #mencoba segala kombinasi dari input sequence yang diterima
    for word in sequences:
        if bcrypt.hashpw(word, hashed) == hashed:
            sendresult(word)
            break
        else:
            print word, "salah"
    channel.close()


def sendresult(result):
    channel.queue_declare(queue='result')
    channel.basic_publish(exchange='', routing_key='result', body=result)


channel.basic_consume(callback, no_ack=True, queue='jobs')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
