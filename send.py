import pika
import bcrypt
import json
from itertools import product
from string import ascii_lowercase

# membangkitkan kombinasi karakter
keywords = [''.join(i) for i in product(ascii_lowercase, repeat=4)]
# membuat koneksi ke queue
cred = pika.PlainCredentials('admin','admin');
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=cred))
channel = connection.channel()
# membuat queue job
channel.queue_declare(queue='jobs')
# kata sandi yang di enkripsi
hashed = bcrypt.hashpw("aaas", bcrypt.gensalt())
njobs = len(keywords) / 10
for i in range(0, len(keywords), njobs):
    a = i
    b = 0
    if (i + njobs) < len(keywords):
        b = i + njobs - 1
    else:
        b = len(keywords) - 1
    print a, b
    # membuat message
    message = {
        'password': hashed,
        'input_sequences': keywords[a:b],
    }
    ready_to_send = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='jobs', body=ready_to_send)

    print(" [x] Sent " + ready_to_send)


# callback untuk menampilkan passwword yang berhasil
def callback(ch, method, properties, body):
    print "encrypted password is:", body
    channel.close()

# menanti hasil
print "waiting for result"
channel.queue_declare(queue='result')
channel.basic_consume(callback, no_ack=True, queue='result')

channel.start_consuming()
# connection.close()