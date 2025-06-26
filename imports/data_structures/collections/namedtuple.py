from collections import namedtuple

Book = namedtuple("Book", ["title", "author", "year"])
brw = Book("Brave New World", "Aldous Huxley", 1931)

print(f"{brw.title} was written by {brw.author} in {brw.year}")
print(f"{brw[0]} was written by {brw[1]} in {brw[2]}")
print(brw._asdict())
