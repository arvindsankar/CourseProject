class Tweet:
    def __init__(self, _id, created_at, text):
        self.id = _id
        self.created_at = created_at
        self.text = text

    def str(self):
        return ",".join([self.id, self.created_at, str(self.text)])
