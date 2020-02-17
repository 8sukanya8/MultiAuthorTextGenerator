import preprocess_NLP_pkg
from src.Author import Author
from src.Document import Document
import re
import datetime

class AuthorCollection:
    """
    A collection of Author objects in a list form. It can find texts written by a single author or filter out texts
    from withing a certain time period
    """
    def __init__(self,folder_path):
        author_names_list = preprocess_NLP_pkg.load_files_from_dir(folder_path, "* *")
        print("Number of Authors", len(author_names_list))
        self.author_list = []
        for author_name in author_names_list:
            text_files = preprocess_NLP_pkg.load_files_from_dir(folder_path+author_name, "*")
            document_list = []
            for file in text_files:
                document_list.append(self.__create_doc(file, folder_path, author_name))
            self.author_list.append(Author(author_name, document_list))

    def __create_doc(self, file, folder_path, author_name):
        """
        creates and returns a document object
        :param file: name of the document
        :param folder_path: location of folder containing the document
        :param author_name: name of the author
        :return: document object
        """
        document_name, year = re.sub(".txt", "", file).split("_")
        date = datetime.datetime(int(year), 1, 1)
        print(author_name, year, document_name)
        file_path = folder_path + author_name + "/" + file
        text = preprocess_NLP_pkg.read_file(file_path, mode='rb', ignore_comments=False)
        return Document(document_name,date,file_path, text.decode("utf-8")) #.decode('ascii')

    def __len__(self):
        return len(self.author_list)

    def __getitem__(self, position):
        return self.author_list[position]

    def get_author_with_name(self, name):
        for author in self.author_list:
            if author.name == name:
                return author

    def filter_author_with_period(self, start_date = datetime.datetime(1850,1,1), end_date = datetime.datetime(1950,1,1)):
        """
        Filters out and returns texts from withing a certain time period
        :param start_date: date of start of filter period
        :param end_date: date of ending of filter period
        :return: a list of auth
        """
        for author in self.author_list:
            items_to_remove = []
            for document in author.documents:
                if document.publishing_year < start_date or document.publishing_year > end_date:
                    items_to_remove.append(document)
            if items_to_remove is not None:
                for item in items_to_remove:
                    author.del_item(item)
