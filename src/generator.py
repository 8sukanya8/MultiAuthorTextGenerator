import random
import preprocess_NLP_pkg
import numpy as np
import json
import re

def generate_dataset(author_collection, output_folder, output_doc_num, min_num_of_authors, max_num_of_authors,
              min_num_of_windows, max_num_of_windows, seed = 1234, window_size = 10000,
              allow_window_variation = False, variation_scaling_factor = 1/10):
    """
    scramble manages the creation of an output dataset
    :param author_collection: an AuthorCollection object
    :param output_folder: folder containing output files
    :param output_doc_num: number of artifical texts to create
    :param min_num_of_authors: minimum number of authors to be contained in an artifical text
    :param max_num_of_authors: maximum number of authors to be contained in an artifical text
    :param min_num_of_windows: minimum number of windows to be contained in an artifical text
    :param max_num_of_windows: maximum number of windows to be contained in an artifical text
    :param seed: seed value
    :param window_size: number of characters to be contained in a window
    :param allow_window_variation: whether window sizes should be changed with respect to variation_scaling_factor
    :param variation_scaling_factor: window size variation of this factor is allowed. 1/10 allows 10% change in window size
    :return:
    """
    random.seed = seed

    for i in range(output_doc_num):
        problem_file_name = "problem-"+str(i)+".txt"
        truth_file_name = "problem-"+str(i)+".truth"
        num_of_windows = random.choice(range(min_num_of_windows,max_num_of_windows))
        num_of_authors = random.choice(range(min_num_of_authors,max_num_of_authors))
        print(problem_file_name, ", number of authors:", num_of_authors, ", number of windows:",num_of_windows)
        selected_author_collection = random.sample(set(author_collection), k = num_of_authors)#random.choices(author_collection, k=num_of_authors) # random.choice(range_of_authors_allowed)
        problem_text,truth_json_data = compose_problem(selected_author_collection,
                                                       total_num_of_windows=num_of_windows,
                                                       num_of_authors= num_of_authors, window_size=window_size,
                                                       allow_window_variation = allow_window_variation,
                                                       variation_scaling_factor = variation_scaling_factor)
        with open(output_folder+"/"+truth_file_name, "w") as write_file:
            json.dump(truth_json_data, write_file, indent=4)
        preprocess_NLP_pkg.write_file(output_folder+"/"+problem_file_name, problem_text.encode(), mode='wb')
        print(truth_json_data)
        #preprocess_NLP_pkg.write_file(output_folder + "/" + truth_file_name, truth_text)

# need to segment into windows with author names
# scramble only from one document per author? or multiple document per author? continuity or non continuity
def compose_problem(author_collection, total_num_of_windows, num_of_authors, window_size,
                    allow_window_variation = False, variation_scaling_factor = 1/10):
    """
    creates the artificial text
    :param author_collection: a collection of Author objects in a list form
    :param total_num_of_windows: number of windows in the artificial text
    :param num_of_authors: number of authors in the artificial text
    :param window_size: size of each window
    :param allow_window_variation: whether window sizes should be changed with respect to variation_scaling_factor
    :param variation_scaling_factor: window size variation of this factor is allowed. 1/10 allows 10% change in window size
    :return:
    """
    num_of_windows_per_author = allocate_windows_to_authors(total_num_of_windows, num_of_authors)
    print("num_of_windows_per_author", num_of_windows_per_author)
    window_order = set_window_order(num_of_windows_per_author,author_collection)
    print("window_order: ",window_order)
    author_text_tuple_list = create_author_text_tuple(author_collection, num_of_authors)
    author_window = {}
    problem_text_list = []
    for i in range(0, len(author_text_tuple_list)):
        entry = author_text_tuple_list[i]
        print("i=", i, "   len(author_text_tuple_list)",  len(author_text_tuple_list))
        number_of_windows = num_of_windows_per_author[i]
        author_name = entry[0]
        document = entry[1]
        windows = split_text_into_windows(text=document.text, number_of_windows=number_of_windows,
                                          window_size=window_size, allow_window_variation=allow_window_variation,
                                          variation_scaling_factor=variation_scaling_factor)
        author_window[author_name] = (document.doc_name, windows)
        print("Window sizes before allocation:", [len(i) for i in windows])
        print(author_name, author_window[author_name])
    switches = []
    count = 0
    for author in window_order:
        print(author)
        window_details = author_window.get(author)
        if window_details is None:
            print("Error! Window details is None")
        else:
            doc_name = window_details[0]
            window = author_window.get(author)[1].pop()
            if window is None:
                print("Error! No window present for this author, skipping this")
            else:
                print(author, doc_name, count,":", count+len(window))
                problem_text_list.append(window)
                count = count + len(window)
                switches.append(count)
    truth_json_data = {
        "authors":num_of_authors,
        "structure":window_order,
        "switches":switches
    }
    print("\nWindow sizes:", [len(i) for i in problem_text_list])
    problem_text = "".join(problem_text_list)
    return problem_text,truth_json_data


def set_window_order(num_of_windows_per_author, author_collection):
    """
    Shuffles the window by each author randomly. For eg. Author1, Author2, Author1, Author3 ....etc
    :param num_of_windows_per_author: window allocations of each author in a list form
    :param author_collection: a collection of Author objects in a list form
    :return:
    """
    print(num_of_windows_per_author)
    number_of_authors = len(num_of_windows_per_author)
    if len(num_of_windows_per_author) > len(author_collection):
        print("Error! Length of num_of_windows_per_author must be equal to that of author_collection. "
              "Check if author collection has at least as many authors as sent for setting window order") # Why? because you have asked to allocate more authors than available in your author collection
        return None
    window_order = ["" for x in range(int(num_of_windows_per_author.sum()))]
    index_range_exclude = []
    total_windows = int(num_of_windows_per_author.sum())
    for i in range(0,number_of_authors):
        author_name = author_collection[i].name
        number_of_windows = int(num_of_windows_per_author[i])
        if number_of_windows>0:
            print(author_name, "number of windows:", number_of_windows)
            for j in range(number_of_windows):
                available_indices = [val for val in range(0, total_windows) if val not in index_range_exclude]
                print(available_indices)
                index_choice = random.choice(available_indices)
                print(author_name, ":", index_choice)
                window_order[index_choice] = author_name
                index_range_exclude.append(index_choice)
    return window_order


def split_text_into_windows(text, number_of_windows, window_size, allow_window_variation, variation_scaling_factor=1/10, start = 0, buffer_space_between_windows =0):
    """
    splits the text into required windows
    :param variation_scaling_factor:
    :param allow_window_variation:
    :param text: given text
    :param number_of_windows: desired number of windows
    :param window_size: size of each window
    :param start: start position
    :param buffer_space_between_windows: buffer space between windows
    :return: windows of text as a list
    """
    windows = []
    if window_size < 200:
        print("Error! Window size of ", window_size, " is too small! Window size should be greater than 200")
        return
    if window_size >= len(text):
        return [text]
    else:
        for i in range(1, int(number_of_windows) + 1):
            end = start+ window_size
            var_length = 0
            if allow_window_variation:
                var_length_limit = int(window_size * variation_scaling_factor) #random.choice(range(1,10))
                print("var_length_limit: ", var_length_limit)
                if var_length_limit<11:
                    print("Warning! since variation character length is too small, no variation is performed")
                else:
                    print("random choice between: ", int(var_length_limit/2), " and ", var_length_limit )
                    var_length = random.choice(range(0, var_length_limit)) #int(var_length_limit/2)
                    print("\nvar_length: ", var_length)
            print("\n\nSTART: ",start, ", window size: ", window_size, ", end: ", end)
            end = end + var_length
            print("end+var_length", end)
            sentence_completion = re.search('[.?!]', text[end:])
            if sentence_completion is not None:
                var_end = sentence_completion.end()
            else:
                var_end = 0
            #print("end+var_length+sentence_completion", text[start:end+var_end])
            window_text = text[start:end+var_end]
            #print("\n\nTEXT: ", window_text)
            windows.append(window_text)
            print(start, len(text[start:end]), len(window_text))
            start = start + len(text[start:end]) + var_end
    return windows


def create_author_text_tuple(author_collection, number_of_authors):
    """
    Returns a tuple of an author with one of his/her document
    :param author_collection:
    :return:
    """
    text_tuple = []
    for i in range(0, number_of_authors):
        author = author_collection[i]
        selected_document = random.choice(author.documents)
        text_tuple.append((author.name, selected_document))
    return text_tuple


def allocate_windows_to_authors(total_num_of_windows, num_of_authors):
    """
    Randomly allocates to each author a fixed number of windows, returns a list of windows to be allocated to
    each author
    :param total_num_of_windows:
    :param num_of_authors:
    :return: a list of windows to be allocated to each author
    """
    if total_num_of_windows < num_of_authors:
        print("Warning! total_num_of_windows should be greater than or equal to num_of_authors. Setting total_num_of_windows to num_of_authors")
        total_num_of_windows = num_of_authors
    num_of_windows_per_author = np.ones(num_of_authors)
    for i in range(0, num_of_authors-1):
        if total_num_of_windows - int(num_of_windows_per_author.sum())>1:
            n = num_of_authors
            if total_num_of_windows - int(num_of_windows_per_author.sum()) < num_of_authors:
                n = total_num_of_windows - int(num_of_windows_per_author.sum())
            seq = range(1,n)
            print("seq", seq.__repr__())
            choice = random.choice(seq)
            print(choice)
            num_of_windows_per_author[i]=choice
    num_of_windows_per_author[len(num_of_windows_per_author)-1]=total_num_of_windows-sum(num_of_windows_per_author)+1
    random.shuffle(num_of_windows_per_author)
    return num_of_windows_per_author