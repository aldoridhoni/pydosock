class ConfigReader():
    def __init__(self):
        self.socket = '/var/run/docker.sock'
        self.host = 'localhost'
        self.port = 4125

    def __getattr__(self):
        pass
