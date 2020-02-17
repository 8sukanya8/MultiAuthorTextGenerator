class Document:
    """
    Document class represents an input text written by an author
    """
    def __init__(self, doc_name, publishing_year, file_path, text):
        """
        :param doc_name: name of the document
        :param publishing_year: year of publishing
        :param file_path: local path of the document
        :param text: text of the document
        """
        self.doc_name = doc_name
        self.file_path = file_path
        self.publishing_year = publishing_year
        self.text = text