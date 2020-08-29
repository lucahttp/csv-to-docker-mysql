file = "c:/Users/Luca/Documents/GitHub/csv-to-docker-mysql/data/myquery.1.sql"
with open(file) as f:
    lines = f.readlines()

lines # ['This is the first line.\n', 'This is the second line.\n']

lines[0] = "DROP DATABASE IF EXISTS mydatabase;\nCREATE DATABASE mydatabase;\nUSE mydatabase;\n"

lines # ["This is the line that's replaced.\n", 'This is the second line.\n']

with open(file, "w") as f:
    f.writelines(lines)