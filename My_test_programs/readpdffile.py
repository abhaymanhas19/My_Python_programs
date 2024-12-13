import pymupdf4llm
path="/home/jarvis/Documents/s10551-015-2689-y.pdf"

f= open(path)

a=pymupdf4llm.to_markdown(f.read())
print(a)