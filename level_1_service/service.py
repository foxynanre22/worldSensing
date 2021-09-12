import sys
import json
import time
import os

class Message:
    '''
    Class that represent message from sensor.

    Args:
        sensor_id (str): the argument that is used to set the value of sensor_id
        model (str): the argument that is used to set the value of model
        payload (str): the argument that is used to set the value of payload

    Attributes:
        sensor_id (str): id of the sensor that sent the message
        model (str): model of the sensor that sent the message
        payload (str): payload of the message
    '''

    def __init__(self, sensor_id, model, payload):
        self.sensor_id = sensor_id
        self.model = model
        self.payload = payload

class Configuration:
    '''
    Class that represent configuration for sensor model.

    Args:
        sensor_model (str): the argument that is used to set the value of sensor_model
        handlers (list): the argument that is used to set the value of handlers attribute
        outputs (list): the argument that is used to set the value of outputs attribute

    Attributes:
        sensor_model (str): sensor model for which this configuration is used
        handlers (list): list containing all supported handlers in a given configuration
        outputs (list): list containing all supported outputs in a given configuration
    '''

    def __init__(self, sensor_model: str, handlers: list, outputs: list):
        self.sensor_model = sensor_model
        self.handlers = handlers
        self.outputs = outputs

class MessageHandler:
    '''
    Class that represent configuration for sensor model.

    Args:
        filenameToSave (str): the argument that is used to set the value of __filenameToSave attribute

    Attributes:
        __filenameToSave (str): name of the file to save payloads from messages
        __configurations (list): list containing all configurations from json file for all supported sensors
    '''
    def __init__(self, filenameToSave: str):
        self.__filenameToSave = filenameToSave
        self.__configurations = JsonWorker.json_to_configuration("config.json")

    def __trim(self, message: Message):
        '''
        Remove whitespace from both ends of the payload attribute in the message

        Args:
            message (Message): The message for change

        Returns:
            message: message from arguments with all changes
        '''
        message.payload = message.payload.strip()
        return message

    def __padToMultiple(self, message: Message, char: str, n: int):
        '''
        Pad the payload on the right with a configured character to a length that is a multiple of some configured N

        Args:
            message (Message): The message for change
            char (string): character to add for multiplicity
            n (int): the value to be a multiple of the message payload

        Returns:
            message: message from arguments with all changes
        '''
        while len(message.payload) % n != 0:
            message.payload += char
    
        return message

    def __addTimestamp(self, message: Message):
        '''
        Add a current timestamp in seconds to the payload.

        Args:
            message (Message): The message for change

        Returns:
            message: message from arguments with all changes
        '''
        message.payload += "_" + str(int(round(time.time() * 1000))//1000)
        return message

    def __message_hook(self, dict_message):
        '''
        Method that represent object_hook argument for json.loads(). Used in handMessage method. 

        Args:
            dict_message (dict): dictionary with json elements to create Message object

        Returns:
            message: Message object with values from dict_message 
        '''
        return Message(dict_message["sensor_id"],dict_message["model"],dict_message["payload"] )
    
    def __find_sensor_config(self, message_model: str, default=None):
        '''
        The method that looks for a configuration for a specific sensor to associate it with the message in handMessage method.

        Args:
            message_model (str): model of the sensor that sent the message

        Returns:
            config: Configuration object for a specific sensor
            defaut: Default value to return if configuration for this model was not found 
        '''

        for config in self.__configurations:
            if config.sensor_model == message_model:
                return config
        return default

    def handMessage(self, message: str):
        '''
        The method that modified payload from message and store it in available outputs using specific configuration.

        Args:
            message (str): message from a sensor
        '''
        message = json.loads(message, object_hook=self.__message_hook)
        current_configuration = self.__find_sensor_config(message.model)
        
        for handler in current_configuration.handlers:
            if handler == "trim":
                self.__trim(message)
            elif handler == "padToMultiple":
                self.__padToMultiple(message, '#', 5)
            elif handler == "addTimestamp":
                self.__addTimestamp(message)
        
        for output in current_configuration.outputs:
            if output == "Console":
                print(message.payload)
            if output == "File":
                with open(os.path.join(sys.path[0], self.__filenameToSave), "a") as f:
                    f.write((message.payload + '\n'))
                    f.close()

class JsonWorker:
    @staticmethod
    def configuration_to_json(fileName: str):
        pass
    
    @staticmethod
    def json_to_configuration(fileName: str):
        with open(os.path.join(sys.path[0], fileName)) as f:
            data = json.load(f)
        
        configurations = []

        for sensor in data["sensors"]:
            conf = Configuration(sensor["sensor_model"], sensor["handlers"], sensor["outputs"])
            configurations.append(conf)

        return configurations

def main(message : str):
    handler = MessageHandler("payloads.txt")
    handler.handMessage(message)

if __name__ == "__main__":
    main(str(sys.argv[1]))