class Tweet:
    def __init__(self, text: str, score: int, url:str, votes: int):
        self.text = text
        self.score = score
        self.url = url
        self.votes = votes
