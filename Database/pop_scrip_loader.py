import re
import sqlite3


bk_abbrevs = {}
bk_alias = []
bk_index = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel',
            '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
            'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel',
            'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai',
            'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
            '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
            '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
            '1 John', '2 John', '3 John', 'Jude', 'Revelation']

# Populate the dict bk_abbrevs and list bk_alias variable with the dictionary file Books Dictionary.
# Add new abbreviations to that file, not hard code.
with open('Books Dictionary', 'r') as dict_file:
    for line in dict_file:
        if line == '\n': continue
        split_line = line.split('-')
        alias = split_line[0]
        if not alias.endswith('.'): bk_alias.append(alias)
        bk_abbrevs[split_line[0]] = split_line[1].strip('\n')

conn = sqlite3.connect('Database/MemScript_E.db')
cur = conn.cursor()

curr_book = str()
curr_chap = str()
curr_verse = str()
updated_count = 0
commit_count = 0
verses_to_parse = str()


def save_to_sql(b, c, v):
    global updated_count
    global commit_count

    print('Updating popularity: ' + b + ' ' + c + ':' + v)

    try:
        book = bk_abbrevs[b]
        pop_value = cur.execute("SELECT popularity FROM \'" + book + "\' WHERE chap = ? AND ver =?", (c, v)).fetchone()

        new_pop = int(pop_value[0]) + 1
        cur.execute("UPDATE \'" + book + "\' SET popularity = ? WHERE chap = ? AND ver =?", (new_pop, c, v))

        if commit_count > 50:
            commit_count = 0
            conn.commit()
        else:
            commit_count += 1

        print('New Popularity Value is ' + str(new_pop))
        updated_count += 1

    except IndexError:
        print('\n\n----Index Error near ' + book + ' ' + c + ' ' + v + ' in "save_to_sql"! Scripture skipped.----\n\n')
    except KeyError:
        print('\n\n----Key Error near ' + book + ' ' + c + ' ' + v + ' in "save_to_sql"! Scripture skipped.----\n\n')
    except TypeError:
        print('\n\n----Type Error near ' + book + ' ' + c + ' ' + v + ' in "save_to_sql"! Scripture skipped.----\n\n')


def split_verse(bk, v):
    global curr_chap
    verse = list()
    verses = v.split(',')
    for m in range(len(verses)):
        badtxt = verses[-1]
        if not str(badtxt[-1]).isdigit():
            del verses[-1]
        else:
            break
    for n in verses:
        num = n.lstrip()
        if num.count(':') > 1:
            verse = split_long(bk, num)
            separator = verse[-1].find(':')
            curr_chap = verse[-1][:separator]
            continue
        elif '-' in num:
            if ':' in num:
                start = num.find(':')
                separator = num.find('-')
                curr_chap = num[:start]
                scrip_start = int(num[start + 1:separator])
            else:
                separator = num.find('-')
                scrip_start = int(num[:separator])
            scrip_end = int(num[separator + 1:])
            number_of_verses = scrip_end - scrip_start + 1
            for items in range(number_of_verses):
                verse.append(curr_chap + ':' + str(scrip_start + items))
        else:
            if ':' in num:
                verse.append(str(num))
            else:
                verse.append(curr_chap + ':' + str(num))
    return verse


def split_long(bk, v):
    list_of_verses = list()
    beg_end = v.split('-')
    beg_chap = int(beg_end[0].split(':')[0])
    beg_vers = int(beg_end[0].split(':')[1])
    end_chap = int(beg_end[1].split(':')[0])
    end_vers = int(beg_end[1].split(':')[1])
    mid_chap = int()
    chaps_inbetween = end_chap - beg_chap - 1

    vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (beg_chap, )).fetchall()
    len_of_chap = len(vrs_in_chap)
    for iteration in range(beg_vers, len_of_chap + 1):
        list_of_verses.append(str(beg_chap) + ':' + str(iteration))
    for _ in range(0, chaps_inbetween):
        mid_chap = beg_chap + (_ + 1)
        vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (mid_chap,)).fetchall()
        len_of_chap = len(vrs_in_chap)
        for iteration in range(1, len_of_chap + 1):
            list_of_verses.append(str(mid_chap) + ':' + str(iteration))
    for iteration in range(0, end_vers):
        list_of_verses.append(str(end_chap) + ':' + str(iteration + 1))
    return list_of_verses


def assign_globals(l):
    global curr_book
    global curr_chap
    global verses_to_parse
    global expression

    expression = re.findall('^(\S.\S*)\s[0-9]*', l)
    curr_book = bk_abbrevs[expression[0]]
    expression = re.findall('^\S.\S*\s([0-9]*)', l)
    curr_chap = expression[0]
    expression = re.findall('^\S.\S*\s([0-9]*:.*)', l)
    if expression == []:
        if curr_book != 'Obadiah' and curr_book != 'Philemon' and curr_book != '2 John' and curr_book != '3 John' and curr_book != 'Jude':
            vrs_in_chap = cur.execute("SELECT ver FROM \'" + curr_book + "\' WHERE chap = ? ", (curr_chap,)).fetchall()
            verses_to_parse = curr_chap + ':'
            for _ in range(0, len(vrs_in_chap)):
                verses_to_parse += str(_ + 1) + ', '
        else:
            verses_to_parse = '1:' + str(curr_chap)
            curr_chap = 1
    else:
        verses_to_parse = expression[0]


def assign_solomon_globals(l):
    global curr_book
    global curr_chap
    global verses_to_parse
    global expression

    curr_book = 'Song of Solomon'
    expression = re.findall('^Song\sof\sSolomon\s([0-9]*)', l)
    curr_chap = expression[0]
    expression = re.findall('^Song\sof\sSolomon\s([0-9]*:.*)', l)
    verses_to_parse = expression[0]

with open('scrip_extracted', 'r') as scriplist:
    scrip_list = scriplist.readlines()


for l in scrip_list:
    try:
        line = l.strip()
        line = line.rstrip(',').rstrip(':').rstrip('-')  # <---------------POSSIBLE TROUBLE----------------
        if line.startswith('Song'):  # Determine if this is the one multi-word book (Song of Solomon)
            assign_solomon_globals(line)
        else:
            assign_globals(line)              # Numbered and single word books. (Exodus or 1 Corinthians)
        try:
            chap_verse_list = split_verse(curr_book, verses_to_parse)
        except IndexError:
            print('\n\n----Index Error near ' + curr_book + ' ' + curr_chap + ' ' + curr_verse +
                  ' in "split_verse"! Scripture skipped.----\n\n')

        for s in chap_verse_list:
            curr_chap = str(s.split(':')[0])
            curr_verse = str(s.split(':')[1])
            save_to_sql(curr_book, curr_chap, curr_verse)  # Variables to send to sql

    except ValueError:
        print('\n\n---ValueError---\nScripture skipped.\n\n')
    except TypeError:
        print('\n\n---TypeError---\nScripture skipped.\n\n')
    except KeyError:
        print('\n\n---KeyError---\nScripture skipped.\n\n')
    except IndexError:
        print('\n\n---IndexError---\nScripture skipped.\n\n'
              'Error is near ' + curr_book + ' ' + curr_chap + ' ' + curr_verse)


conn.commit()
conn.close()
print('\n\n' + str(updated_count) + ' Scripture popularity updated.')