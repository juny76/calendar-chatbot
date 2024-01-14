from langchain_community.document_loaders import PyPDFLoader


def pdf_parser(filename):
    text_list = []
    loader = PyPDFLoader(filename)
    pages = loader.load_and_split()
    num = len(pages)
    return pages
