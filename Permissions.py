class Permission:
    def __init__(self):
        self.permission = None

    def checkPermission(self, check_value):
        permissions_dict = {1: 'ADMIN', 0: 'USER'}
        if check_value == 1:
            self.permission = permissions_dict.get(check_value)
        elif check_value == 0:
            self.permission = permissions_dict.get(check_value)
        else:
            print("No permission matches for this value.")
            return
