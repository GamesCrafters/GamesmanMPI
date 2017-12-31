import src.utils

@src.utils.encode_int
def one():
    return 1

@src.utils.encode_int
def six():
    return 6

@src.utils.encode_int
def zero():
    return 0
