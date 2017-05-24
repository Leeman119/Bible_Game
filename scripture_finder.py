import sqlite3

conn = sqlite3.connect('MemScript_E.db')
cur = conn.cursor()


class ScriptureFinder(object):
    def __init__(self):
        self.bk_abbrevs = {'2 Pe': '2 Peter', '1Ti': '1 Timothy', 'Ga': 'Galatians', '2Chr': '2 Chronicles',
                           'Zep': 'Zephaniah', '2Jo': '2 John', '2The.': '2 Thessalonians', 'Joel': 'Joel',
                           '1Timothy': '1 Timothy', 'Mat.': 'Matthew', '2Thessalonians': '2 Thessalonians',
                           'Jer': 'Jeremiah', 'Es.': 'Esther', 'Isaiah': 'Isaiah', 'Dan': 'Daniel', 'Na': 'Nahum',
                           '2 Ki.': '2 Kings', '1Thessalonians': '1 Thessalonians', '1 Ti': '1 Timothy',
                           '2Pe.': '2 Peter', 'Ro.': 'Romans', '2 Th.': '2 Thessalonians', 'Jas.': 'James',
                           'La.': 'Lamentations', 'Jonah': 'Jonah', '2 Tim.': '2 Timothy', 'De.': 'Deuteronomy',
                           '1 Ch': '1 Chronicles', '1 The': '1 Thessalonians', 'Mark': 'Mark', 'Nu.': 'Numbers',
                           'Mic.': 'Micah', 'Canticles': 'Song of Solomon', '2 Sam.': '2 Samuel',
                           '2 The': '2 Thessalonians', '2Ki.': '2 Kings', '2Samuel': '2 Samuel', '1 Ki': '1 Kings',
                           '2Thes': '2 Thessalonians', '2Cor.': '2 Corinthians', 'Galatians': 'Galatians',
                           'Est.': 'Esther', 'He': 'Hebrews', '2Th': '2 Thessalonians', '1 Chr.': '1 Chronicles',
                           '3Jo.': '3 John', 'Re': 'Revelation', 'Am': 'Amos', 'Jon.': 'Jonah', 'Romans': 'Romans',
                           'Est': 'Esther', '1Samuel': '1 Samuel', '2 Peter': '2 Peter', '1The': '1 Thessalonians',
                           '1King': '1 Kings', 'Act': 'Acts', 'Ge.': 'Genesis', '2 Kings': '2 Kings',
                           'Numbers': 'Numbers', '2 Chr': '2 Chronicles', 'Jg.': 'Judges', 'Na.': 'Nahum', 'Ac': 'Acts',
                           'Ne.': 'Nehemiah', '3Joh': '3 John', 'Ge': 'Genesis', 'Ez': 'Ezra', '2Sam': '2 Samuel',
                           'Col': 'Colossians', '2 Jo.': '2 John', 'Ez.': 'Ezra', 'Rev': 'Revelation',
                           'Proverbs': 'Proverbs', '1Ch': '1 Chronicles', 'Joe': 'Joel', 'Ru.': 'Ruth',
                           '1 Cor': '1 Corinthians', '2 Cor': '2 Corinthians', 'Isa.': 'Isaiah', '1Pe.': '1 Peter',
                           'Ob.': 'Obadiah', 'Ruth': 'Ruth', '1 Th.': '1 Thessalonians', 'Jud': 'Judges',
                           'Nah': 'Nahum', '2 Ch.': '2 Chronicles', 'Jos': 'Joshua', '2 Corinthians': '2 Corinthians',
                           'Colossians': 'Colossians', '1Pet.': '1 Peter', '1The.': '1 Thessalonians', 'Rom.': 'Romans',
                           'Da': 'Daniel', '1 Timothy': '1 Timothy', 'Ezra': 'Ezra', 'Philippians': 'Philippians',
                           '2Ch': '2 Chronicles', 'Haggai': 'Haggai', 'Phm.': 'Philemon',
                           '1 Corinthians': '1 Corinthians', '1Joh': '1 John', '3 Jo': '3 John', 'Hag.': 'Haggai',
                           '2 The.': '2 Thessalonians', '1 Tim.': '1 Timothy', '2Ti': '2 Timothy', 'Luk': 'Luke',
                           '2Cor': '2 Corinthians', 'Neh.': 'Nehemiah', 'Ec.': 'Ecclesiastes', 'Ro': 'Romans',
                           '1Ki': '1 Kings', 'Joh': 'John', '1John': '1 John', 'Jeremiah': 'Jeremiah',
                           '2Thes.': '2 Thessalonians', 'Daniel': 'Daniel', 'Mar.': 'Mark', '2Co.': '2 Corinthians',
                           '1 Thessalonians': '1 Thessalonians', 'Deuteronomy': 'Deuteronomy', 'Ecc': 'Ecclesiastes',
                           'Exodus': 'Exodus', 'Jos.': 'Joshua', 'Joh.': 'John', 'Dan.': 'Daniel', '3 Joh': '3 John',
                           'Hosea': 'Hosea', 'Oba.': 'Obadiah', '2 John': '2 John', 'Leviticus': 'Leviticus',
                           'Genesis': 'Genesis', '2 Ti.': '2 Timothy', '1Th.': '1 Thessalonians',
                           '1 Samuel': '1 Samuel', 'Mr.': 'Mark', 'Isa': 'Isaiah', 'Mar': 'Mark', 'Num.': 'Numbers',
                           'Lu': 'Luke', 'Song': 'Song of Solomon', '2Pet': '2 Peter', 'Judg.': 'Judges',
                           'Obadiah': 'Obadiah', '1 Jo': '1 John', 'Am.': 'Amos', '1 Joh.': '1 John',
                           '1Chronicles': '1 Chronicles', '2 Co.': '2 Corinthians', '1 Ti.': '1 Timothy',
                           'Hag': 'Haggai', '1 Thes': '1 Thessalonians', 'Revelation': 'Revelation', 'Pr.': 'Proverbs',
                           '2 Cor.': '2 Corinthians', '2 Pet.': '2 Peter', 'Luke': 'Luke', '2Joh.': '2 John',
                           'Jas': 'James', '2Tim': '2 Timothy', '1Th': '1 Thessalonians', 'Jude': 'Jude',
                           'Zec.': 'Zechariah', 'Ga.': 'Galatians', 'Jon': 'Jonah', 'Matthew': 'Matthew',
                           '1Cor.': '1 Corinthians', 'Deut': 'Deuteronomy', '1 Pe.': '1 Peter', 'Judges': 'Judges',
                           'Ob': 'Obadiah', '3 Jo.': '3 John', '1 Co': '1 Corinthians', '2Pet.': '2 Peter',
                           'Song ': 'Song of Solomon', 'Malachi': 'Malachi', '2 Ti': '2 Timothy', 'Ezr': 'Ezra',
                           '2Peter': '2 Peter', '1Peter': '1 Peter', '1 Chronicles': '1 Chronicles',
                           'Song of Solomon': 'Song of Solomon', 'Zechariah': 'Zechariah', '1Chr': '1 Chronicles',
                           '1 Pet.': '1 Peter', '2 Chr.': '2 Chronicles', 'Num': 'Numbers', 'Habakkuk': 'Habakkuk',
                           'Col.': 'Colossians', '2Pe': '2 Peter', '1 Sa': '1 Samuel', 'James': 'James',
                           '1Sam': '1 Samuel', '3 John': '3 John', 'Nehemiah': 'Nehemiah', '1Sam.': '1 Samuel',
                           'Ca': 'Song of Solomon', '1 Thes.': '1 Thessalonians', 'Joshua': 'Joshua',
                           '2Sam.': '2 Samuel', '2 Pet': '2 Peter', 'Matt.': 'Matthew', '2Chr.': '2 Chronicles',
                           'Gal.': 'Galatians', '2Corinthians': '2 Corinthians', '2Timothy': '2 Timothy',
                           '1Sa.': '1 Samuel', 'Tit': 'Titus', 'Ex': 'Exodus', '2Th.': '2 Thessalonians',
                           '1Chr.': '1 Chronicles', 'Esther': 'Esther', 'Hab': 'Habakkuk', '1 Cor.': '1 Corinthians',
                           'Matt': 'Matthew', 'Micah': 'Micah', 'Ezekiel': 'Ezekiel', '1Cor': '1 Corinthians',
                           'Oba': 'Obadiah', 'Apo': 'Revelation', 'Ecclesiastes': 'Ecclesiastes',
                           '2 Thessalonians': '2 Thessalonians', '1Sa': '1 Samuel', '2 Timothy': '2 Timothy',
                           '1 Pe': '1 Peter', 'Jg': 'Judges', '2 Samuel': '2 Samuel', '2 King': '2 Kings',
                           'Mt.': 'Matthew', 'De': 'Deuteronomy', '2Co': '2 Corinthians', 'Mt': 'Matthew',
                           'Ecc.': 'Ecclesiastes', 'Heb.': 'Hebrews', 'Hab.': 'Habakkuk', '2Chronicles':
                               '2 Chronicles', 'Nahum': 'Nahum', 'Ap.': 'Revelation', 'Zephaniah': 'Zephaniah',
                           '2 Tim': '2 Timothy', 'Ec': 'Ecclesiastes', '1Thes.': '1 Thessalonians', 'Eph': 'Ephesians',
                           'He.': 'Hebrews', '1 The.': '1 Thessalonians', '1 Co.': '1 Corinthians', 'Re.': 'Revelation',
                           'Mr': 'Mark', '2 Ch': '2 Chronicles', 'Ps': 'Psalms', 'Titus': 'Titus', 'Eze': 'Ezekiel',
                           '1Thes': '1 Thessalonians', 'Ru': 'Ruth', '2The': '2 Thessalonians', 'Le.': 'Leviticus',
                           'Acts': 'Acts', '2Ki': '2 Kings', 'Amos': 'Amos', 'Job': 'Job', 'Ca.': 'Song of Solomon',
                           '2 Thes': '2 Thessalonians', 'Neh': 'Nehemiah', 'Ps.': 'Psalms', '1 Sam.': '1 Samuel',
                           'Phm': 'Philemon', 'Hebrews': 'Hebrews', 'Zec': 'Zechariah', '2 Joh': '2 John',
                           '2Sa': '2 Samuel', '2King': '2 Kings', 'Jer.': 'Jeremiah', '1Corinthians': '1 Corinthians',
                           'Lu.': 'Luke', 'Psalm': 'Psalms', 'Joe.': 'Joel', 'Jud.': 'Judges', 'Mic': 'Micah',
                           '1 Jo.': '1 John', 'Nah.': 'Nahum', '2 Th': '2 Thessalonians', '2Jo.': '2 John',
                           'Ne': 'Nehemiah', '3Jo': '3 John', '2 Thes.': '2 Thessalonians', '2 Joh.': '2 John',
                           '3Joh.': '3 John', '1 Sa.': '1 Samuel', '1 Joh': '1 John', 'Php': 'Philippians',
                           '2 Jo': '2 John', '1Jo': '1 John', 'Hos.': 'Hosea', '1 Peter': '1 Peter', 'Pr': 'Proverbs',
                           'Le': 'Leviticus', 'Mat': 'Matthew', 'Ho.': 'Hosea', 'Mal': 'Malachi', '2Sa.': '2 Samuel',
                           'Tit.': 'Titus', '1Jo.': '1 John', '1 Sam': '1 Samuel', 'Rev.': 'Revelation',
                           'Ex.': 'Exodus', '1Ch.': '1 Chronicles', 'Nu': 'Numbers', 'Jam': 'James',
                           'Lamentations': 'Lamentations', '2 Pe.': '2 Peter', 'Apo.': 'Revelation',
                           '1Co.': '1 Corinthians', 'Jam.': 'James', '2Kings': '2 Kings', '1Pe': '1 Peter',
                           '1 John': '1 John', 'Eze.': 'Ezekiel', '1Tim.': '1 Timothy', '1Tim': '1 Timothy',
                           'Rom': 'Romans', 'Philemon': 'Philemon', '1Pet': '1 Peter', 'Ac.': 'Acts', 'Es': 'Esther',
                           '2 Ki': '2 Kings', '1 King': '1 Kings', '2Tim.': '2 Timothy', '2John': '2 John', '2Joh':
                               '2 John', 'Mal.': 'Malachi', 'Luk.': 'Luke', 'Gen': 'Genesis', '1Kings': '1 Kings',
                           'John': 'John', 'Gen.': 'Genesis', 'Zep.': 'Zephaniah', 'Psalms': 'Psalms', 'Heb': 'Hebrews',
                           'Ephesians': 'Ephesians', '1Ti.': '1 Timothy', 'Deut.': 'Deuteronomy',
                           '1 Ch.': '1 Chronicles', 'Proverb': 'Proverbs', 'Judg': 'Judges', '3John': '3 John',
                           '3 Joh.': '3 John', 'Php.': 'Philippians', 'La': 'Lamentations', '2 Sa.': '2 Samuel',
                           'Ap': 'Revelation', '2 Sam': '2 Samuel', '2Ch.': '2 Chronicles', '1Joh.': '1 John',
                           '1 Ki.': '1 Kings', 'Hos': 'Hosea', '2 Chronicles': '2 Chronicles', 'Ho': 'Hosea',
                           'Ezr.': 'Ezra', '1Co': '1 Corinthians', 'Eph.': 'Ephesians', '1 Th': '1 Thessalonians',
                           '2 Sa': '2 Samuel', 'Gal': 'Galatians', '1 Chr': '1 Chronicles', '1 Kings': '1 Kings',
                           '2 Co': '2 Corinthians', 'Da.': 'Daniel', '1Ki.': '1 Kings', '1 Pet': '1 Peter',
                           '2Ti.': '2 Timothy', '1 Tim': '1 Timothy', 'Apocalipse': 'Revelation'}
        self.bk_aliases = [
            'Genesis', 'Gen.', 'Gen', 'Ge.', 'Ge', 'Exodus', 'Ex.', 'Ex', 'Leviticus', 'Le.', 'Le', 'Numbers', 'Num.',
            'Num', 'Nu.', 'Nu', 'Deuteronomy', 'Deut.', 'Deut', 'De.', 'De', 'Joshua', 'Jos.', 'Jos', 'Judges',
             'Judg.', 'Judg', 'Jud.', 'Jud', 'Jg.', 'Jg', 'Ruth', 'Ru.', 'Ru', '1 Samuel', '1 Sam.', '1 Sam', '1 Sa.',
            '1 Sa', '1Samuel','1Sam.', '1Sam', '1Sa.',  '1Sa', '2 Samuel', '2 Sam.', '2 Sam', '2 Sa.', '2 Sa',
            '2Samuel', '2Sam.', '2Sam', '2Sa.', '2Sa', '1 Kings', '1 King', '1 Ki.', '1 Ki', '1Kings', '1King', '1Ki.',
            '1Ki', '2 Kings', '2 King', '2 Ki.', '2 Ki', '2Kings', '2King', '2Ki.', '2Ki', '1 Chronicles', '1 Chr.',
            '1 Chr', '1 Ch.', '1 Ch', '1Chronicles', '1Chr.', '1Chr', '1Ch.', '1Ch', '2 Chronicles', '2 Chr.', '2 Chr',
            '2 Ch.', '2 Ch', '2Chronicles', '2Chr.', '2Chr', '2Ch.', '2Ch', 'Ezra', 'Ezr.', 'Ezr', 'Ez.', 'Ez',
            'Nehemiah', 'Neh.', 'Neh', 'Ne.', 'Ne', 'Esther', 'Est.', 'Est', 'Es.', 'Es', 'Job', 'Psalms', 'Psalm',
            'Ps.', 'Ps', 'Proverbs', 'Proverb', 'Pr.', 'Pr', 'Ecclesiastes', 'Ecc.', 'Ecc', 'Ec.', 'Ec',
            'Song of Solomon', 'Song', 'Canticles', 'Ca.', 'Ca', 'Isaiah', 'Isa.', 'Isa', 'Jeremiah', 'Jer.',
            'Jer', 'Lamentations', 'La.', 'La', 'Ezekiel', 'Eze.', 'Eze', 'Daniel', 'Dan.', 'Dan', 'Da.', 'Da',
            'Hosea', 'Hos.', 'Hos', 'Ho.', 'Ho', 'Joel', 'Joe.', 'Joe', 'Amos', 'Am.', 'Am', 'Obadiah', 'Oba.', 'Oba',
            'Ob.', 'Ob', 'Jonah', 'Jon.', 'Jon', 'Micah', 'Mic.', 'Mic', 'Nahum', 'Nah.', 'Nah', 'Na.', 'Na',
            'Habakkuk', 'Hab.', 'Hab', 'Zephaniah', 'Zep.', 'Zep', 'Haggai', 'Hag.', 'Hag', 'Zechariah', 'Zec.',
            'Zec', 'Malachi', 'Mal.', 'Mal', 'Matthew', 'Matt.', 'Matt', 'Mat.', 'Mat', 'Mt.', 'Mt', 'Mark', 'Mar.',
            'Mar', 'Mr.', 'Mr', 'Luke', 'Luk.', 'Luk', 'Lu.', 'Lu', 'John', 'Joh.', 'Joh', 'Acts', 'Act', 'Ac.', 'Ac',
            'Romans', 'Rom.', 'Rom', 'Ro.', 'Ro', '1 Corinthians', '1 Cor.', '1 Cor', '1 Co.', '1 Co', '1Corinthians',
            '1Cor.', '1Cor', '1Co.', '1Co', '2 Corinthians', '2 Cor.', '2 Cor', '2 Co.', '2 Co', '2Corinthians',
            '2Cor.', '2Cor', '2Co.', '2Co', 'Galatians', 'Gal.', 'Gal', 'Ga.', 'Ga', 'Ephesians', 'Eph.', 'Eph',
            'Philippians', 'Php.', 'Php', 'Colossians', 'Col.', 'Col', '1 Thessalonians', '1 Thes.', '1 Thes', '1 The.',
            '1 The', '1 Th.', '1 Th', '1Thessalonians', '1Thes.', '1Thes', '1The.', '1The', '1Th.', '1Th',
            '2 Thessalonians', '2 Thes.', '2 Thes', '2 The.', '2 The', '2 Th.', '2 Th', '2Thessalonians', '2Thes.',
            '2Thes', '2The.', '2The', '2Th.', '2Th', '1 Timothy', '1 Tim.', '1 Tim', '1 Ti.', '1 Ti', '1Timothy',
            '1Tim.', '1Tim', '1Ti.', '1Ti', '2 Timothy', '2 Tim.', '2 Tim', '2 Ti.', '2 Ti', '2Timothy', '2Tim.',
            '2Tim', '2Ti.', '2Ti', 'Titus', 'Tit.', 'Tit', 'Philemon', 'Phm.', 'Phm', 'Hebrews', 'Heb.', 'Heb', 'He.',
            'He', 'James', 'Jam.', 'Jam', 'Jas.', 'Jas', '1 Peter', '1 Pet.', '1 Pet', '1 Pe.', '1 Pe', '1Peter',
            '1Pet.', '1Pet', '1Pe.', '1Pe', '2 Peter', '2 Pet.', '2 Pet', '2 Pe.', '2 Pe', '2Peter', '2Pet.', '2Pet',
            '2Pe.', '2Pe', '1 John', '1 Joh.', '1 Joh', '1 Jo.', '1 Jo', '1John', '1Joh.', '1Joh', '1Jo.', '1Jo',
            '2 John', '2 Joh.', '2 Joh', '2 Jo.', '2 Jo', '2John', '2Joh.', '2Joh', '2Jo.', '2Jo', '3 John', '3 Joh.',
            '3 Joh', '3 Jo.', '3 Jo', '3John', '3Joh.', '3Joh', '3Jo.', '3Jo', 'Jude', 'Revelation', 'Rev.', 'Rev',
            'Re.', 'Re', 'Apocalipse', 'Apo.', 'Apo', 'Ap.', 'Ap'
        ]
        self.bk_index = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
                         '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
                         'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
                         'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah',
                         'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark',
                         'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
                         'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy',
                         'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
                         'Jude', 'Revelation')
        self.one_chap_books = ['Obadiah', 'Philemon', '2 John', '3 John', 'Jude']
        self.numbered_books = ['1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
                               '1 Corinthians', '2 Corinthians', '1 Thessalonians', '2 Thessalonians',
                               '1 Timothy', '2 Timothy', '1 Peter', '2 Peter', '1 John', '2 John', '3 John']
        self.count_retrieved = 0
        self.count_verses = 0
        self.scripture_list = []
        self.failed = []

    # Main extraction. Creates a list of scriptures.
    def run(self, source):
        # Make sure the source is a single string, or convert a list source into a string.
        if type(source) == list():
            line = str()
            for _ in source:
                line += _
        else:
            line = source

        # Variables declared for use here, so they are reset with each run.
        self.count_retrieved = 0
        self.scripture_list = []
        self.failed = []

        # Search for each alias of a book. (Ex: Genesis, Gen, Ge, Gen., Ge.)
        for alias in self.bk_aliases:
            curr_bk = self.bk_abbrevs[alias]
            # print('Searching for: ' + alias)

            while line.find(alias) != -1:
                retrieved = ''
                try:
                    index = line.find(alias)
                    chap_ver_beg = index + len(alias)
                    chap_ver_end = chap_ver_beg

                    # Starting with the first index number after the len(alias), look at each character to determine
                    # the end of the of the expression. Below, we see the first char after the alias is 1, and the last
                    # that would pass the while statement is the 8.
                    # "sent, Jesus Christ. (Obadiah17, 18) Yes, the Bible teaches that..."
                    while line[chap_ver_end].isdigit() or line[chap_ver_end] == ' ' or line[chap_ver_end] == ',' \
                            or line[chap_ver_end] == ':' or line[chap_ver_end] == ';' or line[chap_ver_end] == '-':
                        chap_ver_end += 1
                    retrieved = alias + line[chap_ver_beg:chap_ver_end]

                    # Remove the found scripture from the line so it won't be found multiple times.
                    line = line[:index] + line[chap_ver_beg:]

                    # Ignore cases where the book is mentioned without a chapter or verse.
                    while retrieved[-1].isdigit() is False:
                        retrieved = retrieved[:-1]
                        if len(retrieved) < len(alias):
                            break
                    if len(retrieved) < len(alias):
                        continue

                    # If the book retrieved is a single-chapter book, change the format. ('Jude 3' becomes '1:3')
                    if curr_bk in self.one_chap_books and ':' not in retrieved:
                        retrieved = '1:' + retrieved[len(alias) + 1:].strip()
                    # Otherwise, just trim out the expression so it only contains the verses. ('Rom 5:8' becomes '5:8')
                    else:
                        retrieved = retrieved[len(alias):]

                    # Remove whitespace.
                    retrieved = retrieved.replace(' ', '')

                    # Parse the scriptures into individual book/chapter/verse entries. Create the final scripture list.
                    parsed = self.split_verse(curr_bk, retrieved)
                    for scripture in parsed:
                        self.scripture_list.append(scripture)

                except ValueError:
                    self.failed.append(['ValueError', alias, retrieved,
                                        'Last success was ' + self.scripture_list[-1]])
                except IndexError:
                    self.failed.append(['IndexError', alias, retrieved,
                                        'Last success was ' + self.scripture_list[-1]])

        self.count_retrieved = len(self.scripture_list)
        print(str(self.failed) + '\n')

        return self.scripture_list

    def split_verse(self, bk, v):
        to_parse = v.split(';')
        collection = []
        for vrs in to_parse:
            # If there's no ':', then these are full chapters. (Something like either 'Mark 5' or 'Mark 7-9')
            if ':' not in vrs:
                parsed = self.get_full_chap(bk, vrs)  # Gets all verses in those chapters, verified to exist.
                for p in parsed:
                    collection.append(p)
                continue

            # This will take care of ranges of verses spanning multiple chapters. (Like 'Isaiah 3:4-5:7')
            elif vrs.count(':') > 1:
                parsed = self.split_long(bk, vrs)
                for p in parsed:
                    collection.append(p)
                continue

            # This will handle simple verses and range of verses. (Like 3:4 or 3:4,5,6 or 3:4-9)
            else:
                curr_chap = vrs.split(':')[0]
                verses = vrs.split(':')[1].split(',')
                for v in verses:
                    if '-' in v:
                        beg_ver = int(v.split('-')[0])
                        end_ver = int(v.split('-')[1])
                        for ver in range(beg_ver, end_ver + 1):
                            scrip = bk + '/' + curr_chap + '/' + str(ver)
                            collection.append(scrip)

                    else:
                        scrip = bk + '/' + curr_chap + '/' + v
                        collection.append(scrip)

        return collection

    @staticmethod
    def split_long(bk, v):
        # Split multi-chapter ranges into individual verses. Genesis 5:3-7:5 becomes:
        # [Genesis/5/4, Genesis/5/5, Genesis/5/6, ..., Genesis/6/1, Genesis/6/2, ..., Genesis/7/4, Genesis/7/5]
        list_of_verses = list()
        beg_end = v.split('-')
        beg_chap = int(beg_end[0].split(':')[0])
        beg_vers = int(beg_end[0].split(':')[1])
        end_chap = int(beg_end[1].split(':')[0])
        end_vers = int(beg_end[1].split(':')[1])
        chaps_inbetween = end_chap - beg_chap - 1

        # Retrieve verses from the first chapter, starting with the referenced verse till the end of the chapter.
        vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (beg_chap,)).fetchall()
        len_of_chap = len(vrs_in_chap)
        for iteration in range(beg_vers, len_of_chap + 1):
            list_of_verses.append(bk + '/' + str(beg_chap) + '/' + str(iteration))

        # Retrieve all the verses from all the chapters in between
        for _ in range(0, chaps_inbetween):
            mid_chap = beg_chap + (_ + 1)
            vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (mid_chap,)).fetchall()
            len_of_chap = len(vrs_in_chap)
            for iteration in range(1, len_of_chap + 1):
                list_of_verses.append(bk + '/' + str(mid_chap) + '/' + str(iteration))

        # Retrieve verses in the last referenced chapter, from the beginning till the last verse referenced.
        for iteration in range(0, end_vers):
            list_of_verses.append(bk + '/' + str(end_chap) + '/' + str(iteration + 1))
        return list_of_verses

    @staticmethod
    def get_full_chap(bk, ch):
        parsed = []
        # If retrieving an entire chapter, fetch the number of verses in that chapter.
        # Genesis 7 becomes ['Genesis/7/1', 'Genesis/7/2' ,'Genesis/7/3', 'Genesis/7/4','...']
        if '-' in ch:
            chaps = ch.split('-')
            beg_chap = chaps[0]
            end_chap = chaps[1]
            num_of_chaps = int(end_chap) - int(beg_chap) + 1
            for i in range(num_of_chaps):
                chap = int(beg_chap) + i
                vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (chap, )).fetchall()
                for vrs in vrs_in_chap:
                    parsed.append(bk + '/' + str(chap) + '/' + str(vrs[0]))
        else:
            vrs_in_chap = cur.execute("SELECT ver FROM \'" + bk + "\' WHERE chap = ? ", (ch,)).fetchall()
            for v in vrs_in_chap:
                parsed.append(bk + '/' + str(ch) + '/' + str(v[0]))
        return parsed


# test = ScriptureFinder()
#
# with open('D:\\PythonProjects\\Bible_Game\\Experimental\\test_extract.txt', 'r') as file:
#     lines = file.readlines()
#     temp = ''
#     for l in lines:
#         temp += str(l)
#
#     test.run(temp)

