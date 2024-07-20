import wikipedia


def loadWikiData(page, sentences):
    ''' Load data from wikipedia page
        Args: page: str - wikipedia page name
              tokens: int - number of tokens to load
    '''
    page = wikipedia.page(page)
    text = page.content
    text = text.split(".")[0:sentences]
    text = " ".join(text)
    return text


def loadText(fileName):
    pass

def loadCSV(fileName):
    pass

def loadPdf(fileName):
    pass

