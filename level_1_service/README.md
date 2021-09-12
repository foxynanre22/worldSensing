This is a service that accepts messages from sensors, modifies the payload and store it.

## Setup
1. Clone the repository.
2. Install required Python dependencies: 

    `pip install -r requirements.txt`
3. Open folder in Terminal or Command Line and run program with the message. Example:

    `python service.py '{\"sensor_id\":\"1\", \"model\":\"WS-0004\",\"payload\":\"      asdasd\"}'`


## Comments
1. 'model' argument in message means model of the sensor. Now program might work with next models: WS-0001, WS-0002, WS-0003, WS-0004. You can add supported models to config.json