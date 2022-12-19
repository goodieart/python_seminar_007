import view
import db
import model

db.create_connection('directory.db')
db.get_cursor()
#db.db_import('import.csv', 'csv')
view.print_entries(10)
#db.db_export('output.txt', 'txt')
model.get_entry('Васильева Виктория Александровна')