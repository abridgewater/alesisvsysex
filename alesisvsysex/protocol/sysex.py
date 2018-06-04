from .model import AlesisModel

__all__ = ['SysexMessage']

class SysexMessage (object):
    
    _TYPES = {
        'update': [0x61],
        'query':  [0x62],
        'reply':  [0x63]
    }

    _MANUFACTURER_ALESIS = [0x00, 0x00, 0x0e]

    _START_BYTE = [0xf0]
    _END_BYTE   = [0xf7]
    
    def __init__(self, msg_type, model):
        self.type  = msg_type
        self.model = model

    @classmethod
    def encodeWord(cls, word):
        return [word >> 7, word & 0x7f]

    def serialize(self):
        if self.type == 'query':
            return bytes(self._START_BYTE + self._MANUFACTURER_ALESIS + self.model._DEVICE_ID
                         + self._TYPES[self.type]
                         + self.encodeWord(self.model.num_bytes()) + self._END_BYTE)
        elif (self.type == 'update') or (self.type == 'reply'):
            return bytes(self._START_BYTE + self._MANUFACTURER_ALESIS + self.model._DEVICE_ID
                         + self._TYPES[self.type]
                         + self.encodeWord(self.model.num_bytes())) + self.model.serialize() + bytes(self._END_BYTE)
        else:
            raise RuntimeError('Don\'t know how to encode %s messages' % self.type)

    @classmethod
    def deserialize(cls, b):
        i = 0
        
        start_byte = b[i : i+1]
        if start_byte != bytes(cls._START_BYTE):
            raise ValueError("Invalid start byte '0x%02x'" % start_byte[0])
        i += 1
        
        manufacturer = b[i : i + len(cls._MANUFACTURER_ALESIS)]
        if manufacturer != bytes(cls._MANUFACTURER_ALESIS):
            raise ValueError("Invalid manufacturer id")
        i += len(cls._MANUFACTURER_ALESIS)

        device_id = list(b[i : i + 2])
        model_class = AlesisModel.findModelByDeviceId(device_id)
        if model_class is None:
            raise ValueError("Invalid device id")
        i += len(device_id)
        
        t = b[i : i + 1]
        for k, v in cls._TYPES.items():
            if t == bytes(v):
                msg_type = k
                break
        else:
            raise ValueError("Unknown message type '0x%02x'" % t[0])
        i += 1
        
        message_length = b[i : i + 2]
        if message_length != bytes(cls.encodeWord(model_class.num_bytes())):
            raise ValueError("Invalid message length")
        i += len(message_length)
        
        if msg_type == "query":
            model = None
        else:
            model = model_class.deserialize(b[i : i + model_class.num_bytes()])
            i += model_class.num_bytes()
        
        end_byte = b[i : i+1]
        if end_byte != bytes(cls._END_BYTE):
            raise ValueError("Invalid end byte '0x%02x'" % end_byte[0])
        i += 1
        
        return SysexMessage(msg_type, model)
