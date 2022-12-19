import db

def print_entries(number:int = 2):
    e = db.get_entries('directory', number)
    print(e)