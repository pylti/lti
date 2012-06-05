from uuid import uuid1

def generate_identifier():
    return uuid1().__str__()
