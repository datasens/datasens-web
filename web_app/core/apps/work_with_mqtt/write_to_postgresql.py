from datetime import datetime
import paho.mqtt.client as mqtt
import psycopg2

temperature_topic = "esp32/bme280/temperature"
humidity_topic = "esp32/bme280/humidity"

dataTuple = [-1,-1]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(temperature_topic)
    client.subscribe(humidity_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    theTime = datetime.strftime(datetime.now(), "'%Y-%m-%d %H:%M:%S'")
    result = (theTime + "\t" + msg.payload.decode("utf-8"))
    print(msg.topic + ":\t" + result)
    if (msg.topic == temperature_topic):
        dataTuple[0] = msg.payload.decode("utf-8")
    if (msg.topic == humidity_topic):
        dataTuple[1] = msg.payload.decode("utf-8")
        #return
    if (dataTuple[0] != -1 and dataTuple[1] != -1):
        writeToDb(theTime, dataTuple[0], dataTuple[1])
    return

def writeToDb(theTime, temperature, humidity):
    conn = psycopg2.connect(database = "test_mqtt",
                            user = "postgres",
                            password = "postgres",
                            host = "172.17.0.3",
                            port = "5432"
                            )
    cur = conn.cursor()
    print("Writing to db...")
    cur.execute("INSERT INTO climate (theTime, temperature, humidity) VALUES ({0}, {1}, {2});".format(theTime, temperature, humidity))
    conn.commit()
    global dataTuple
    dataTuple = [-1, -1]
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.17.0.2", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()