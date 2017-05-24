import re
import os
import sqlite3

bk_abbrevs = {}
bk_alias = []
bk_index = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel',
            '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
            'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel',
            'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai',
            'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
            '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
            '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
            '1 John', '2 John', '3 John', 'Jude', 'Revelation')

conn = sqlite3.connect('MemScript_E.db')
cur = conn.cursor()
line = ''

# Populate the dict bk_abbrevs and list bk_alias variable with the 'Abbreviations' table.
abbrevs = cur.execute("SELECT key, value FROM Abbreviations").fetchall()
for abb in abbrevs:
    bk_alias.append(abb[0])
    bk_abbrevs[abb[0]] = abb[1]

print(bk_alias)
print(bk_abbrevs)
# This code should no longer be needed since migrating the "Books Dictionary" file into the database.
# print(bk_alias)
# print(bk_abbrevs)
# #
# with open('Books Dictionary', 'r') as dict_file:
#     for line in dict_file:
#         if line == '\n': continue
#         split_line = line.split('-')
#         alias = split_line[0]
#         if not alias.endswith('.'): bk_alias.append(alias)
#         bk_abbrevs[split_line[0]] = split_line[1].strip('\n')
#     print(bk_alias)
#     for k, v in bk_abbrevs.items():
# cur.execute("INSERT OR IGNORE INTO Abbreviations (key, value) VALUES (?, ?)", (k, v))
# conn.commit()

scrip_extracted = open('scrip_extracted', 'w')

count = 0
prev_scrips = list()
prev_line = str()

# This block of code is only for testing.
# with open('Extract Scriptures.txt', 'r') as file:  # <--------------------- Test file insertion.
#     file_lines = file.readlines()


def trim_scrip(text):
    result = text
    if len(text) < 23: return result
    if not text.split()[0] in bk_alias:
        return ''
    found_digits = False
    if text.isalpha() is True:
        return ''
    for index, char in enumerate(text):
        if char.isalpha() is True and found_digits is True:
            result = text[:index]
            break
        elif char.isdigit() is True:
            found_digits = True
        else:
            continue
    if result[-1] == ' ':
        result = result[:-1]
    return result


# Look through txt files in the Literature TXTs folder and put all text into a single string variable.
for filename in os.listdir('Literature TXTs'):
    if filename.endswith(".txt"):
        with open('Literature TXTs/'+filename, 'r') as file:
            file_lines = file.readlines()
        for l in file_lines:
            line += l


for alias in bk_alias:
    scrips = re.findall('('+alias+' [^a-z].+?)[)|.|\[]', line)
    if scrips == []: continue
    if scrips == prev_scrips: continue
    prev_scrips = scrips

    for scrip_group in scrips:
        scrip = scrip_group.split(';')
        cur_bk = str()
        for i in scrip:
            try:
                item = i
                if item[0] == ' ': item = item[1:]
                if item.startswith('read'): item = item[5:]
                if item.startswith('compare'): item = item[7:]
                if item[0].isdigit() and item[2].isalpha():  # This happens for numbered books like 1 Corinthians
                    cur_bk = item.split()[0] + ' ' + item.split()[1]
                    item = trim_scrip(item)
                    if item == '':
                        continue
                    scrip_extracted.write(item)
                elif item[0].isalpha():                      # This happens for all other books
                    cur_bk = item.split()[0]
                    item = trim_scrip(item)
                    if item == '':
                        continue
                    scrip_extracted.write(item)
                elif item[0].isdigit():                      # This takes care of multiple scriptures in a single book.
                    item = cur_bk + ' ' + item               # Example - Matthew 6:9, 10; 8:13-17; 12:11
                    item = trim_scrip(item)
                    if item == '':
                        continue
                    scrip_extracted.write(item)

            except IndexError:
                print('\n\nKeyError near ' + str(item) + '\nItem Skipped\n\n')
            except KeyError:
                print('\n\nKeyError near ' + str(item) + '\nItem Skipped\n\n')

            scrip_extracted.write('\n')
            count += 1
            print('Extracting scripture number: ' + str(count))


print('\n----Extraction Complete----\n\n')
scrip_extracted.close()

# if input("Save extracted as popular scriptures? [Y]es or [N]") == 'Y' or 'Yes' or 'y' or 'yes':
#     exec(open("pop_scrip_loader.py").read(), globals())



