

class ApiSuccess():
    def __init__(self, msg = None, data = None) :
        self.msg = msg
        self.data = data
        self.success = True
        
class ApiError():
    def __init__(self, msg = None, data = None) :
        self.msg = msg
        self.data = data
        self.success = False
    