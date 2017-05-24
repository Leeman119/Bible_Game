import sqlite3
import re
import sys

fname = 'test.txt'
fhandle = open(fname)
wfname = 'temp_file'
wfhandle = open(wfname, 'w')

curr_book = fhandle.readline().strip('\n').capitalize()
if curr_book[0].isdigit():
   curr_book = curr_book[:2] + curr_book[2:].capitalize()
elif curr_book.startswith('The'):
    print("REFORMAT ORIGIN FILE TITLE")
    sys.exit("FIX THE ORIGIN FILE")
wfhandle.write(curr_book)
wfhandle.write('\n')

conn = sqlite3.connect('MemScript_E.db')
cur = conn.cursor()


for line in fhandle:
    lin = str(line).strip('\n')
    if lin == '[Footnotes]': break
    verse = re.split('([0-9]*?\?)', lin)
    if verse is None: continue
    if verse[0] == '': del(verse[0])
    for i in verse:
        # print(i)
        wfhandle.write(i)
        wfhandle.write('\n')

wfhandle.close()
fhandle.close()


fhandle = open('book_to_save')
curr_book = fhandle.readline().strip('\n')
wfhandle = open(curr_book, 'w')

sql_commit_iter = int()
curr_chap = int(0)
curr_verse = int(0)
prev_text = str()
curr_text = str()


def sav_file():
    wfhandle.write(str(curr_book) + ' ')
    wfhandle.write(str(curr_chap) + ':')
    wfhandle.write(str(curr_verse) + '\n')
    wfhandle.write(str(curr_text) + '\n')


def sav_sql():
    global sql_commit_iter
    sql_commit_iter += 1
    cur.execute("INSERT INTO \'" + curr_book + "\' (chap, ver, tex, popularity) VALUES (?, ?, ?, 0) ",
                (curr_chap, curr_verse, curr_text))
    if sql_commit_iter > 50:
        sql_commit_iter = 0
        conn.commit()



def advance():
    global curr_verse
    global prev_text
    global curr_text

    curr_verse += 1

    print(curr_chap)
    print(curr_verse)
    print(curr_text)
    if curr_chap != 0:
        sav_file()
        sav_sql()

    prev_text = curr_text
    curr_text = str()



for l in fhandle:
    line = str(l)
    if line[0] == ' ': line = line[1:]

    if line[0] == '\"' or line[0] == '?':
        curr_text = curr_text.strip('\n')
        curr_text += line
        continue

    try:
        if line[1] == '?' or line[2] == '?' or line[3] == '?':
            advance()
            continue
        else:
            if line[0].isdigit():
                num_digits = 2
                if line[1].isdigit():
                    num_digits = 3
                    if line[2].isdigit():
                        num_digits = 4
                        if line[3].isdigit():
                            num_digits = 5
                            if line[4].isdigit():
                                num_digits = 6
                                if line[5].isdigit():
                                    num_digits = 7
                                    if line[6].isdigit():
                                        num_digits = 8
                                        if line[7].isdigit():
                                            num_digits = 9
                                            if line[8].isdigit():
                                                num_digits = 10

                reg_num = int(line[:num_digits - 1])
                if reg_num != curr_chap + 1:
                    curr_text += line
                else:
                    advance()
                    curr_chap += 1
                    curr_verse = 0
                    curr_text = line[num_digits:]

            else:
                curr_text += line

    except IndexError:
        curr_text = curr_text.strip('\n')
        curr_text += line
        continue


advance()
conn.commit()
conn.close()
fhandle.close()
wfhandle.close()
