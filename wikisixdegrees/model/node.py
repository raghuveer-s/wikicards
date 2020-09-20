class Node:
    '''
    Individual node in wikidb
    '''

    def __init__(self, id, url, title, content, date_visited):
        self.id = id
        self.url = url
        self.title = title
        self.content = content
        self.date_visited = date_visited