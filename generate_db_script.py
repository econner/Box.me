import os

TEXTFILES_DIRECTORY = 'notes_for_db/'
SCRIPT_NAME = 'build_db.sql'

insert_note_cmd = 'insert into icebox_note values(%(note_id)s, \'2\', %(user_id)s, \'2011-06-07 04:15:41.352064\', \'2011-06-07 04:15:41.352100\', 0);'
insert_noterev_cmd = 'insert into icebox_noterevision values(%(rev_id)s, \'2\', \'2011-06-07 04:15:55.068508\', \'2011-06-07 04:15:55.068547\', \'%(title)s\', \'%(body)s\', 0, %(note_id)s);'

f = open(SCRIPT_NAME, 'w')
index = 1
for filename in os.listdir(TEXTFILES_DIRECTORY):
    note_file = open(TEXTFILES_DIRECTORY + filename)
    note = note_file.read()
    note = note.replace('\'', '\'\'')
    note_parts = note.split('\n', 1)
    f.write(insert_note_cmd % {'note_id': index, 'user_id': 2})
    f.write('\n')
    f.write(insert_noterev_cmd % {'rev_id': index, 'title': note_parts[0], 'body': note_parts[1], 'note_id': index})
    f.write('\n\n')
    note_file.close()
    index = index + 1
    
f.close()