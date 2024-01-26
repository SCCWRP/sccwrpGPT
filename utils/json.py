import json
from datetime import datetime
from pandas import Timestamp

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, Timestamp)):
            # You can format the datetime in any format you prefer
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)