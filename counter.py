from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import sys


def get_files(filename):
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
    try:
        if files[0].find("a")["title"] == "Go to parent directory":
            files = files[1:]
    except:
        pass
    tags = list()
    for i in files:
        title = i.find("div", {"role": "rowheader"}).find("a")['href']
        file_type = i.find("div", {"role": "gridcell"}).find("svg")['aria-label']
        tags.append((title, file_type))
    return tags


def file_header_data(filename):
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


def file_lines(filename):
    data = file_header_data(filename)
    if "lines" in data:
        data = data.split(" ")
        # lines index:
        lines_idx = data.index("lines")
        return data[lines_idx - 1]
    return '0'


def create_filename(filename):
    return 'https://github.com' + filename


def count_lines(filename):
    num_lines = 0
    files = get_files(filename)
    for i in files:
        name = create_filename(i[0])
        print(name)
        if i[1] == "Directory":
            num_lines += count_lines(name)
        else:
            num_lines += int(file_lines(name))
    return num_lines


def main(filename):
    try:
        print(count_lines(filename))
    except:
        print(file_lines(filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(input("Please enter repository url: "))
