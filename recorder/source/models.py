class Data(object):
    def __init__(self, timestamp, feature, identifier, value):
        self.timestamp = timestamp
        self.feature = feature
        self.identifier = identifier
        self.value = value

    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=data['HD_TIMESTAMP'],
            feature=data['HD_FEATURE'],
            identifier=data['HD_IDENTIFIER'],
            value=data['HD_VALUE']
        )

    @classmethod
    def from_database(cls, data):
        return cls(
            timestamp=data[0],
            feature=data[1],
            identifier=data[2],
            value=data[3]
        )

    def get_dict(self):
        return {
            "timestamp": self.timestamp,
            "feature": self.feature,
            "identifier": self.identifier,
            "value": self.value
        }

    def get_database_tuple(self):
        return (
            self.timestamp,
            self.feature,
            self.identifier,
            self.value
        )
