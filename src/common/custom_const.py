class Status:
    UNKNOWN = -1
    OFF = 0
    STARTING = 1
    ON = 2
    STOPPING = 3
    KILLED = 4

    ENABLE_STOP = [ON]
    ENABLE_START = [UNKNOWN, OFF]
