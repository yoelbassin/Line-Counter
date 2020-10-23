from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import sys


def get_files(filename):
    """
    returns the files and directories from a specific directory

    :param filename: github rep url
    :return: tuple - (file or directory path, file type directory or file)
    """
    # generate connection
    url_ = Request(filename)
    u_client = urlopen(url_)
    page_html = u_client.read()
    u_client.close()

    # parse page
    parsed_page = soup(page_html, "html.parser")
    con = parsed_page.find("div", {"class": "Box mb-3"})
    files = con.findAll("div", {"role": "row"})
    files = files[1:]
    try:  # checks if the current directory is not the main directory, for the deletion of the 'go to parent
        # directory row', for prevention of an infinite loop
        if files[0].find("a")["title"] == "Go to parent directory":
            files = files[1:]  # deletion of the "go to parent directory" row
    except:  # if the directory is the main directory there is no <a title> tag so an exception will be thrown
        pass
    paths = list()
    for i in files:  # creates a tuple (path, file_type) for every file in the directory
        title = i.find("div", {"role": "rowheader"}).find("a")['href']
        file_type = i.find("div", {"role": "gridcell"}).find("svg")['aria-label']
        paths.append((title, file_type))
    return paths


def file_header_data(filename):
    """
    return the github code box header, i.e. '__ lines (__ sloc) | __ KB' in the specified file
    :param filename: github file path
    :return: string containing the github code box header
    """
    # generate connection
    url_ = Request(filename)
    u_client = urlopen(url_)
    page_html = u_client.read()
    u_client.close()

    # parse page
    parsed_page = soup(page_html, "html.parser")
    box = parsed_page.find("div", {"class": "Box mt-3 position-relative"})
    lines = box.find("div", {"class": "text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0"})
    return lines.text


def file_num_lines(filename):
    """
    return the number of lines in the specified file
    :param filename: github file path
    :return: integer representing the number of the lines
    """
    data = file_header_data(filename)  # get the github code box header
    if "lines" in data:
        data = data.split(" ")
        # lines index:
        lines_idx = data.index("lines")  # find the index of the string "lines"
        return data[lines_idx - 1]  # return the data before the string "lines", i.e. the number of the lines
    return '0'  # return 0 if the file doesn't contain code lines


def create_filename(filepath):
    """
    generates a url from the path in the repository
    :param filepath: the repository path
    :return: the github.com/path url
    """
    return 'https://github.com' + filepath


def count_lines(filename):
    """
    counts the number of lines in all the directories and files
    :param filename: github directory url
    :return: integer representing the total number of the lines in the directory
    """
    num_lines = 0
    files = get_files(filename)
    for i in files:  # for every object in the directory, check if it is a file or a directory:
        # If it is a directory, recursively call the function with the directory path.
        # If it is a file, count the number of the lines in the file.
        # Finally return the total number of lines counted in the directory
        name = create_filename(i[0])
        print(name)
        if i[1] == "Directory":
            num_lines += count_lines(name)
        else:
            num_lines += int(file_num_lines(name))
    return num_lines


def main(filename):
    """
    main function, calls the applicable functions for counting the total number of the lines in the directory or file
    :param filename: github directory or file url
    :return: None, prints the total number of lines in the github directory or file
    """
    try:
        print(count_lines(filename))
    except:
        print(file_num_lines(filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(input("Please enter repository url: "))
