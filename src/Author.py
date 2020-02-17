class Author:
    """
    Class Author represents all the documents in the input dataset written by the same author.
    """
    def __init__(self, name, documents):
        self.name = name
        self.documents = documents

    def __delitem__(self, key):
        """
        deletes books from author collection
        :param key:
        :return:
        """
        self.documents = [item for item in self.documents if not (item.doc_name == key.doc_name and
                                                                  item.publishing_year == key.publishing_year)]

    def del_item(self, key):
        self.__delitem__(key)

