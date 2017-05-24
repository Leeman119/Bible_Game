from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from random import randrange

from Ui import main_win, scripture_games, release_notes
from scripture_finder import ScriptureFinder

conn = sqlite3.connect('MemScript_E.db')
cur = conn.cursor()

find_script = ScriptureFinder()
book_index = find_script.bk_index

settings = {}
pop_dic = {}
highest_pop = 0


# Load the game settings data table into a dictionary for use. (Key = "game-setting_name")
def load_main_settings():
    global highest_pop

    # Fill 'pop_dic' with {scripture:popularity}, and assign the highest popularity value to 'highest_pop'.
    for bk in book_index:
        add_to_popularity_list = cur.execute("SELECT chap, ver, popularity FROM \'" + bk + "\' "
                                             "WHERE popularity >= 0").fetchall()
        for s in add_to_popularity_list:
            tup = (bk, s[0], s[1])
            pop = s[2]
            pop_dic[tup] = pop
            if pop > highest_pop:
                highest_pop = pop

    # Retrieve the rest of the settings from sql and store in the dictionary 'settings'.
    for setlist in cur.execute("SELECT game, setting_name, setting_value FROM Settings").fetchall():
        settings[str(setlist[0]) + "-" + str(setlist[1])] = setlist[2]

    # The custom list of scriptures is stored in the string format "Matthew/24/14|John/17/3|Mark/12/9|",
    # but needs to be a list of lists. "[['Matthew', '24', '14'], ['Mark', '12', '9'], ['John', '17', '3']]"
    if settings['name_that_scripture-custom_list'] != '':
        converting_list = settings['name_that_scripture-custom_list'].rstrip('|')
        converting_list = converting_list.split('|')
        settings['name_that_scripture-custom_list'] = []
        for item in converting_list:
            settings['name_that_scripture-custom_list'].append(item.split('/'))

    # And again for the "Quote that scripture" game.
    if settings['quote_that_scripture-custom_list'] != '':
        converting_list = settings['quote_that_scripture-custom_list'].rstrip('|')
        converting_list = converting_list.split('|')
        settings['quote_that_scripture-custom_list'] = []
        for item in converting_list:
            settings['quote_that_scripture-custom_list'].append(item.split('/'))
load_main_settings()


class MainWin(QtWidgets.QMainWindow, main_win.Ui_main_window):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.btn_quit.clicked.connect(self.quit_game)
        self.release_notes_btn.clicked.connect(self.show_release_notes)
        self.btn_g1.clicked.connect(self.game1_btn)
        self.btn_g2.clicked.connect(self.game2_btn)

    @staticmethod
    def quit_game():
        sys.exit()

    @staticmethod
    def show_release_notes():
        latest_release_notes.show()

    @staticmethod
    def game1_btn():
        name_scripture_game.show()

    @staticmethod
    def game2_btn():
        quote_scripture_game.show()


class ScriptureSettings(QtWidgets.QWidget, scripture_games.Ui_scripture_settings):
    def __init__(self, name):
        super(ScriptureSettings, self).__init__()
        self.name = name
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Variable declarations for class use. (And for keeping things straight in my head.)
        self.custom_list = []
        self.old_list = []
        self.scripture_list = []
        self.obscurity = int()
        self.popularity = int()

        self.load_settings()
        self.show_custom_list()
        self.generate_scripture_list()

        self.browse_file_btn.clicked.connect(self.pick_file)
        self.extract_file_btn.clicked.connect(self.extract)
        self.popular_sbox.valueChanged.connect(self.generate_scripture_list)
        self.obscure_sbox.valueChanged.connect(self.generate_scripture_list)
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.rejected.connect(self.cancel_settings)
        self.update_list_btn.clicked.connect(self.update_custom_list)
        self.custom_list_chk.clicked.connect(self.update_custom_list)

    def load_settings(self):
        self.obscurity = int(settings[self.name + '-obscure_setting'])
        self.popularity = int(settings[self.name + '-popular_setting'])

        if settings[self.name + '-use_custom_list'] == 'True':
            self.custom_list_setting = True
        else:
            self.custom_list_setting = False

        if settings[self.name + '-include_list'] == 'True':
            self.include_list_setting = True
        else:
            self.include_list_setting = False

        if settings[self.name + '-exclude_list'] == 'True':
            self.exclude_list_setting = True
        else:
            self.exclude_list_setting = False

        if settings[self.name + '-only_list'] == 'True':
            self.only_list_setting = True
        else:
            self.only_list_setting = False

        if settings[self.name + '-custom_list'] != '':
            self.custom_list = settings[self.name + '-custom_list']
        else:
            self.custom_list = []
        self.old_list = self.custom_list

        # Initialize the settings window to the saved settings
        self.obscure_slider.setMaximum(highest_pop - 1)
        self.obscure_sbox.setMaximum(highest_pop - 1)
        if self.obscurity > highest_pop - 1:
            self.obscure_sbox.setValue(highest_pop - 1)
        else:
            self.obscure_sbox.setValue(self.obscurity)

        self.popular_slider.setMaximum(highest_pop)
        self.popular_sbox.setMaximum(highest_pop)
        if self.popularity > highest_pop:
            self.popular_sbox.setValue(highest_pop)
        else:
            self.popular_sbox.setValue(self.popularity)

        self.custom_list_chk.setChecked(self.custom_list_setting)
        self.include_rdo.setChecked(self.include_list_setting)
        self.exclude_rdo.setChecked(self.exclude_list_setting)
        self.only_list_rdo.setChecked(self.only_list_setting)

    def generate_scripture_list(self):
        high = self.popular_sbox.value()
        low = self.obscure_sbox.value()
        self.scripture_list = []

        # Maybe add a limit so that visually the 2 sliders will not pass each other
        # self.obscure_sbox.setMaximum(high - 1)
        # self.obscure_slider.setMaximum(high - 1)
        # self.popular_sbox.setMinimum(low + 1)
        # self.popular_slider.setMinimum(low + 1)

        for k, v in pop_dic.items():
            if low < v < high:
                self.scripture_list.append([k[0], str(k[1]), str(k[2])])

        if self.custom_list_chk.isChecked():

            if self.include_rdo.isChecked():
                for custom in self.custom_list:
                    if custom in self.scripture_list:
                        continue
                    else:
                        self.scripture_list.append(custom)

            elif self.exclude_rdo.isChecked():
                for custom in self.custom_list:
                    if custom in self.scripture_list:
                        self.scripture_list.remove(custom)

            elif self.only_list_rdo.isChecked():
                self.scripture_list = []
                for scrip in self.custom_list:
                    if scrip not in self.scripture_list:
                        self.scripture_list.append(scrip)

        self.current_setting_lbl.setText("The current setting will present " + str(len(self.scripture_list))
                                         + " scriptures in the test.")

    def show_custom_list(self):
        display = []
        if self.custom_list == []:
            display.append('Enter your list or paste an article here.\n\n'
                           'Books can be abbreviated, but must be capitalized.\n\n'
                           'If entering scriptures manually, be sure to hit enter before clicking on "Update List".')
        else:
            for scrip in self.custom_list:
                text_to_display = scrip[0] + ' ' + scrip[1] + ':' + scrip[2] + '\n'
                display.append(text_to_display)
        self.custom_list_box.setPlainText(''.join(display))

    def update_custom_list(self):
        self.custom_list = []
        if self.custom_list_chk.isChecked():
            text = self.custom_list_box.toPlainText()
            raw_list = find_script.run(text)

            for item in raw_list:
                book = item.split('/')[0]
                chap = item.split('/')[1]
                verse = item.split('/')[2]
                self.custom_list.append([book, chap, verse])

            # CREATE LOOP TO CONFIRM VERSES IN THE LIST EXIST, MAKE EACH ENTRY UNIQUE, AND CONVERT TO TEXT FOR DISPLAY.
            self.show_custom_list()
        self.generate_scripture_list()

    def save_settings(self):
        self.update_custom_list()
        self.obscurity = self.obscure_sbox.value()
        self.popularity = self.popular_sbox.value()
        self.old_list = self.custom_list

        settings[self.name + '-obscure_setting'] = str(self.obscurity)
        settings[self.name + '-popular_setting'] = str(self.popularity)

        save_custom = []
        for scripture in self.custom_list:
            save_custom.append(scripture[0] + '/' + scripture[1] + '/' + scripture[2] + '|')
        save_custom = ''.join(save_custom)
        settings[self.name + '-custom_list'] = save_custom

        if self.custom_list_chk.isChecked():
            settings[self.name + '-use_custom_list'] = "True"
        else:
            settings[self.name + '-use_custom_list'] = "False"

        if self.include_rdo.isChecked():
            settings[self.name + '-include_list'] = "True"
        else:
            settings[self.name + '-include_list'] = "False"

        if self.exclude_rdo.isChecked():
            settings[self.name + '-exclude_list'] = "True"
        else:
            settings[self.name + '-exclude_list'] = "False"

        if self.only_list_rdo.isChecked():
            settings[self.name + '-only_list'] = "True"
        else:
            settings[self.name + '-only_list'] = "False"

        # Save new settings to the SQL Settings table
        for k, v in settings.items():
            game = k.split('-')[0]
            # Bug fix where an untouched custom list for another game was being re-saved in the wrong format.
            if str(game) != str(self.name):
                continue
            setting_name = k.split('-')[1]
            setting_value = str(v)
            cur.execute("UPDATE Settings SET setting_value = ? "
                        "WHERE game = ? AND setting_name =?", (setting_value, game, setting_name))
        conn.commit()
        name_scripture_game.restart()
        self.hide()

    def cancel_settings(self):
        self.obscure_sbox.setValue(self.obscurity)
        self.popular_sbox.setValue(self.popularity)
        self.custom_list_chk.setChecked(self.custom_list_setting)
        self.include_rdo.setChecked(self.include_list_setting)
        self.exclude_rdo.setChecked(self.exclude_list_setting)
        self.only_list_rdo.setChecked(self.only_list_setting)

        self.custom_list = self.old_list
        self.show_custom_list()
        self.generate_scripture_list()

        self.hide()

    def pick_file(self):

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            self.input_file.setText(fname[0])

    def extract(self):
        with open(self.input_file.text(), 'r') as file:
            lines = file.readlines()
            text = ''.join(lines)
            self.custom_list_box.setPlainText(text)
        self.update_custom_list()


class NameScriptureGame(QtWidgets.QWidget, scripture_games.Ui_name_scripture):
    def __init__(self):
        super(NameScriptureGame, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Variable declarations for class use. (And for keeping things straight in my head.)
        self.mistaken = False
        self.right_ans_list = ()
        self.right_ans = str()
        self.hint_progress = 0
        self.hint_count = 3
        self.score_good = 0
        self.score_bad = 0
        self.spread = (3, 3)  # Tuple defines how far on either side of the correct book to pull possible wrong answers

        self.choiceA_btn.clicked.connect(self.choice_a)
        self.choiceB_btn.clicked.connect(self.choice_b)
        self.choiceC_btn.clicked.connect(self.choice_c)
        self.choiceD_btn.clicked.connect(self.choice_d)
        self.settings_btn.clicked.connect(self.settings)
        self.hint_btn.clicked.connect(self.hint)
        self.mainmenu_btn.clicked.connect(self.back)
        self.restart_btn.clicked.connect(self.restart)

        self.hint_btn.setText('Hints: ' + str(self.hint_count))
        self.reset()

    @staticmethod
    def settings():
        name_scripture_settings.show()

    def choice_a(self):
        self.check_ans(self.choiceA_btn.text())

    def choice_b(self):
        self.check_ans(self.choiceB_btn.text())

    def choice_c(self):
        self.check_ans(self.choiceC_btn.text())

    def choice_d(self):
        self.check_ans(self.choiceD_btn.text())

    def check_ans(self, selection):
        if selection == self.right_ans:
            if self.mistaken:
                self.reset()
                self.mistaken = False
            else:
                self.reveal('Correct')
                self.hint_prog()
                self.score_good += 1
                self.reset()
        else:
            self.reveal('Incorrect')
            self.score_bad += 1
            self.mistaken = True

        self.good_lcd.setProperty("intValue", self.score_good)
        self.bad_lcd.setProperty("intValue", self.score_bad)

    def reveal(self, outcome):
        if self.choiceA_btn.text() != self.right_ans:
            self.choiceA_btn.setText('')
        # else:
        #     txt = self.choiceA_btn.text()
        #     self.choiceA_btn.setText(txt + '\nClick here to continue.')

        if self.choiceB_btn.text() != self.right_ans:
            self.choiceB_btn.setText('')
        # else:
        #     self.choiceB_btn.setText(self.choiceB_btn.text() + '\nClick here to continue.')

        if self.choiceC_btn.text() != self.right_ans:
            self.choiceC_btn.setText('')
        # else:
        #     self.choiceC_btn.setText(self.choiceC_btn.text() + '\nClick here to continue.')

        if self.choiceD_btn.text() != self.right_ans:
            self.choiceD_btn.setText('')
        # else:
        #     self.choiceD_btn.setText(self.choiceD_btn.text() + '\nClick here to continue.')

    def hint(self):
        self.hint_count -= 1
        buttons = [self.choiceA_btn, self.choiceB_btn, self.choiceC_btn, self.choiceD_btn]

        i = 2
        while i > 0:
            self.button = buttons[randrange(0, len(buttons))]
            if self.button.text() != self.right_ans:
                self.button.setText('')
                buttons.remove(self.button)
                i -= 1
                self.hint_btn.setText('Hints: ' + str(self.hint_count))

    def hint_prog(self):
        self.hint_progress += 1
        if self.hint_progress > 5:
            self.hint_progress = 0
            self.hint_count += 1
        self.hint_btn.setText('Hints: ' + str(self.hint_count))

    def back(self):
        self.hide()

    def restart(self):
        msg = QtWidgets.QMessageBox(self)
        reply = msg.question(self, 'Restart Game', "Would you like to reset the game and score?",
                             msg.Yes | msg.No, msg.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.reset()
            self.hint_progress = 0
            self.hint_count = 3
            self.hint_btn.setText('Hints: ' + str(self.hint_count))
            self.score_good = 0
            self.score_bad = 0
            self.good_lcd.setProperty("intValue", 0)
            self.bad_lcd.setProperty("intValue", 0)

    def reset(self):

        self.right_ans = self.retrieve('right')
        wrong_ans1 = self.retrieve('wrong1')
        wrong_ans2 = self.retrieve('wrong2')
        wrong_ans3 = self.retrieve('wrong3')
        ans_list = [self.right_ans, wrong_ans1, wrong_ans2, wrong_ans3]

        ans1 = ans_list[randrange(0, len(ans_list))]
        self.choiceA_btn.setText(ans1)
        ans_list.remove(ans1)

        ans2 = ans_list[randrange(0, len(ans_list))]
        self.choiceB_btn.setText(ans2)
        ans_list.remove(ans2)

        ans3 = ans_list[randrange(0, len(ans_list))]
        self.choiceC_btn.setText(ans3)
        ans_list.remove(ans3)

        ans4 = ans_list[randrange(0, len(ans_list))]
        self.choiceD_btn.setText(ans4)
        ans_list.remove(ans4)

    def retrieve(self, scripture):
        if len(name_scripture_settings.scripture_list) > 0:
            self.choiceA_btn.setEnabled(True)
            self.choiceB_btn.setEnabled(True)
            self.choiceC_btn.setEnabled(True)
            self.choiceD_btn.setEnabled(True)
            if scripture == 'right':
                self.right_ans_list = name_scripture_settings.scripture_list[
                    randrange(0, len(name_scripture_settings.scripture_list))]
                book = self.right_ans_list[0]
                chapter = self.right_ans_list[1]
                verse = self.right_ans_list[2]

                question = cur.execute("SELECT tex FROM \'" + book + "\' WHERE chap = ? AND ver =?",
                                       (chapter, verse)).fetchone()
                self.scripture_lbl.setText(question[0])
                return str(book) + ' ' + str(chapter) + ':' + str(verse)

            else:
                book_num = book_index.index(self.right_ans_list[0])
                wrong_list = []
                mini = book_num - self.spread[0]
                if mini < 0: mini = 0
                maxi = book_num + self.spread[1]
                if maxi > 65: maxi = 65
                for i in range(mini, maxi):
                    wrong_list.append(i)
                book = book_index[wrong_list[randrange(0, len(wrong_list))]]
                verse_id = cur.execute("SELECT id FROM \'" + book + "\'").fetchall()
                wrong = cur.execute("SELECT chap, ver FROM \'" + book + "\' WHERE id = ?",
                                    verse_id[randrange(0, len(verse_id))]).fetchone()
                return str(book) + ' ' + str(wrong[0]) + ':' + str(wrong[1])
        else:
            self.scripture_lbl.setText('The obscurity to popularity range is too narrow, there are no scriptures'
                                       ' to show.\n\nTry using the settings to broaden the list of scriptures used.')
            self.choiceA_btn.setEnabled(False)
            self.choiceB_btn.setEnabled(False)
            self.choiceC_btn.setEnabled(False)
            self.choiceD_btn.setEnabled(False)


class QuoteScriptureGame(QtWidgets.QWidget, scripture_games.Ui_quote_scripture):
    def __init__(self):
        super(QuoteScriptureGame, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Variable declarations for class use. (And for keeping things straight in my head.)
        self.mistaken = False
        self.right_ans_list = ()
        self.right_ans = str()
        self.hint_progress = 0
        self.hint_count = 3
        self.score_good = 0
        self.score_bad = 0
        self.spread = (3, 3)  # Tuple defines how far on either side of the correct book to pull possible wrong answers

        self.choiceA_btn.clicked.connect(self.choice_a)
        self.choiceB_btn.clicked.connect(self.choice_b)
        self.choiceC_btn.clicked.connect(self.choice_c)
        self.choiceD_btn.clicked.connect(self.choice_d)
        self.settings_btn.clicked.connect(self.settings)
        self.hint_btn.clicked.connect(self.hint)
        self.mainmenu_btn.clicked.connect(self.back)
        self.restart_btn.clicked.connect(self.restart)

        self.hint_btn.setText('Hints: ' + str(self.hint_count))
        self.reset()

    @staticmethod
    def settings():
        quote_scripture_settings.show()

    def choice_a(self):
        self.check_ans(self.textA_lbl.text())

    def choice_b(self):
        self.check_ans(self.textB_lbl.text())

    def choice_c(self):
        self.check_ans(self.textC_lbl.text())

    def choice_d(self):
        self.check_ans(self.textD_lbl.text())

    def check_ans(self, selection):
        if selection == self.right_ans:
            if self.mistaken:
                self.reset()
                self.mistaken = False
            else:
                self.reveal('Correct')
                self.hint_prog()
                self.score_good += 1
                self.reset()
        else:
            self.reveal('Incorrect')
            self.score_bad += 1
            self.mistaken = True

        self.good_lcd.setProperty("intValue", self.score_good)
        self.bad_lcd.setProperty("intValue", self.score_bad)

    def reveal(self, outcome):
        if self.textA_lbl.text() != self.right_ans:
            self.textA_lbl.setText('')
        # else:
        #     txt = self.choiceA_btn.text()
        #     self.choiceA_btn.setText(txt + '\nClick here to continue.')

        if self.textB_lbl.text() != self.right_ans:
            self.textB_lbl.setText('')
        # else:
        #     self.choiceB_btn.setText(self.choiceB_btn.text() + '\nClick here to continue.')

        if self.textC_lbl.text() != self.right_ans:
            self.textC_lbl.setText('')
        # else:
        #     self.choiceC_btn.setText(self.choiceC_btn.text() + '\nClick here to continue.')

        if self.textD_lbl.text() != self.right_ans:
            self.textD_lbl.setText('')
        # else:
        #     self.choiceD_btn.setText(self.choiceD_btn.text() + '\nClick here to continue.')

    def hint(self):
        self.hint_count -= 1
        buttons = [self.choiceA_btn, self.choiceB_btn, self.choiceC_btn, self.choiceD_btn]

        i = 2
        while i > 0:
            self.button = buttons[randrange(0, len(buttons))]
            if self.button.text() != self.right_ans:
                self.button.setText('')
                buttons.remove(self.button)
                i -= 1
                self.hint_btn.setText('Hints: ' + str(self.hint_count))

    def hint_prog(self):
        self.hint_progress += 1
        if self.hint_progress > 5:
            self.hint_progress = 0
            self.hint_count += 1
        self.hint_btn.setText('Hints: ' + str(self.hint_count))

    def back(self):
        self.hide()

    def restart(self):
        msg = QtWidgets.QMessageBox(self)
        reply = msg.question(self, 'Restart Game', "Would you like to reset the game and score?",
                             msg.Yes | msg.No, msg.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.reset()
            self.hint_progress = 0
            self.hint_count = 3
            self.hint_btn.setText('Hints: ' + str(self.hint_count))
            self.score_good = 0
            self.score_bad = 0
            self.good_lcd.setProperty("intValue", 0)
            self.bad_lcd.setProperty("intValue", 0)

    def reset(self):

        self.right_ans = self.retrieve('right')
        wrong_ans1 = self.retrieve('wrong1')
        wrong_ans2 = self.retrieve('wrong2')
        wrong_ans3 = self.retrieve('wrong3')
        ans_list = [self.right_ans, wrong_ans1, wrong_ans2, wrong_ans3]

        ans1 = ans_list[randrange(0, len(ans_list))]
        self.textA_lbl.setText(ans1)
        ans_list.remove(ans1)

        ans2 = ans_list[randrange(0, len(ans_list))]
        self.textB_lbl.setText(ans2)
        ans_list.remove(ans2)

        ans3 = ans_list[randrange(0, len(ans_list))]
        self.textC_lbl.setText(ans3)
        ans_list.remove(ans3)

        ans4 = ans_list[randrange(0, len(ans_list))]
        self.textD_lbl.setText(ans4)
        ans_list.remove(ans4)

    def retrieve(self, scripture):
        if len(quote_scripture_settings.scripture_list) > 0:
            self.choiceA_btn.setEnabled(True)
            self.choiceB_btn.setEnabled(True)
            self.choiceC_btn.setEnabled(True)
            self.choiceD_btn.setEnabled(True)
            if scripture == 'right':
                self.right_ans_list = name_scripture_settings.scripture_list[
                    randrange(0, len(name_scripture_settings.scripture_list))]
                book = self.right_ans_list[0]
                chapter = self.right_ans_list[1]
                verse = self.right_ans_list[2]

                question = cur.execute("SELECT tex FROM \'" + book + "\' WHERE chap = ? AND ver =?",
                                       (chapter, verse)).fetchone()
                self.scripture_lbl.setText(str(book) + ' ' + str(chapter) + ':' + str(verse))
                return question[0]

            else:
                book_num = book_index.index(self.right_ans_list[0])
                wrong_list = []
                mini = book_num - self.spread[0]
                if mini < 0: mini = 0
                maxi = book_num + self.spread[1]
                if maxi > 65: maxi = 65
                for i in range(mini, maxi):
                    wrong_list.append(i)
                book = book_index[wrong_list[randrange(0, len(wrong_list))]]
                verse_id = cur.execute("SELECT id FROM \'" + book + "\'").fetchall()
                wrong = cur.execute("SELECT tex FROM \'" + book + "\' WHERE id = ?",
                                    verse_id[randrange(0, len(verse_id))]).fetchone()
                return wrong[0]
        else:
            msg = 'The obscurity to popularity range is too narrow, there are no scriptures ' \
                  'to show.\n\nTry using the settings to broaden the list of scriptures used.'
            self.textA_lbl.setText(msg)
            self.textB_lbl.setText(msg)
            self.textC_lbl.setText(msg)
            self.textD_lbl.setText(msg)

            self.choiceA_btn.setEnabled(False)
            self.choiceB_btn.setEnabled(False)
            self.choiceC_btn.setEnabled(False)
            self.choiceD_btn.setEnabled(False)


class ReleaseNotes(QtWidgets.QWidget, release_notes.Ui_release_notes):
    def __init__(self):
        super(ReleaseNotes, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.ok_btn.clicked.connect(self.done)
        self.load_notes()

    def done(self):
        self.hide()

    def load_notes(self):
        updates = cur.execute("SELECT setting_value FROM Settings "
                              "WHERE setting_name = ?", ('release_notes', )).fetchone()
        self.update_lbl.setText(updates[0])


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main_win = MainWin()
    latest_release_notes = ReleaseNotes()

    name_scripture_settings = ScriptureSettings('name_that_scripture')
    quote_scripture_settings = ScriptureSettings('quote_that_scripture')

    name_scripture_game = NameScriptureGame()
    quote_scripture_game = QuoteScriptureGame()

    main_win.show()

    sys.exit(app.exec_())
