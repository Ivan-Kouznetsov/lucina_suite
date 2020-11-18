class ContextExample:
    """
    Example of the context in which a collocation is used
    """
    def __init__(self, text: str, desc: str, url:str, score:str):        
        self.text = text
        self.desc = desc
        self.url = url
        self.score = score

    def __str__(self):
        return "{} - {}\n{}\n{}\n".format(self.score, self.desc, self.text, self.url)
