from tkinter import *
from tkinter import messagebox
from random import randint, choice
from time import sleep
from numpy import loadtxt
from os.path import *
from sys import *

class Hangman_init:
    def __init__(self):
        self.word = choice(self.get_word())
        self.word_length = len(list(self.word))
        self.word_list = list(self.word)
        self.guessed_letters = ['_' for i in range(self.word_length)]
        self.guesses_left = 6
        self.init_letter(choice(self.word_list))
    def get_word(self):
        path = join(split(abspath(argv[0]))[0], 'common.txt')
        words = open(path, 'r').read().split('\n')
        return words
    def reload_word(self):
        return choice(self.get_word())
    def init_letter(self, letter):
        if letter in self.word_list and letter not in self.guessed_letters:
            for i in range(self.word_length):
                if self.word_list[i] == letter:
                    self.guessed_letters[i] = letter
        elif letter not in self.word_list:
            self.guesses_left -= 1
    def check_win(self):
        if self.guesses_left <=0 and self.guessed_letters != self.word_list:
            return False
        elif self.guessed_letters == self.word_list:
            return True
        else:
            return False

class Hangman_UI:
    def __init__(self, master: Tk):
        self.master = master
        self.master.title("Hangman")
        self.master.geometry("700x700")
        self.master.resizable(False, False)
        self.master.configure(bg='#2E2E2E')
        self.init_widgets()
        self.init_bindings()
        self.init_hangman()
        self.master.mainloop()
    def init_widgets(self):
        self.hangman_label = Label(self.master, text="Hangman", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.hangman_label.grid(row=0, column=0, columnspan=2, pady=20)
        self.word_label = Label(self.master, text="Từ:", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.word_label.grid(row=1, column=0, pady=20)
        self.word_display = Label(self.master, text="", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.word_display.grid(row=1, column=1, pady=20)
        self.guesses_label = Label(self.master, text="Lượt còn lại:", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.guesses_label.grid(row=2, column=0, pady=20)
        self.guesses_display = Label(self.master, text="", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.guesses_display.grid(row=2, column=1, pady=20)
        self.guessed_letters_label = Label(self.master, text="Chữ cái đã đoán:", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.guessed_letters_label.grid(row=3, column=0, pady=20)
        self.guessed_letters_display = Label(self.master, text="", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.guessed_letters_display.grid(row=3, column=1, pady=20)
        self.guess_entry = Entry(self.master, font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300")
        self.guess_entry.grid(row=4, column=0, columnspan=2, pady=20)
        self.guess_button = Button(self.master, text="Đoán", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300", command=self.guess_letter)
        self.guess_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.reload_button = Button(self.master, text="Đổi từ", font=("Segoe UI", 20), bg="#2E2E2E", fg="#FFC300", command=self.reload_word)
        self.reload_button.grid(row=5, column=1, columnspan=2, pady=20, padx=20)
    def init_bindings(self):
        self.master.bind('<Return>', self.guess_letter)
    def init_hangman(self):
        self.hangman = Hangman_init()
        self.update_word()
        self.update_guesses()
        self.update_guessed_letters()
    def update_word(self):
        self.word_display.configure(text=" ".join(self.hangman.guessed_letters))
    def update_guesses(self):
        self.guesses_display.configure(text=self.hangman.guesses_left)
    def update_guessed_letters(self):
        data = [x for x in list(set(self.hangman.guessed_letters)) if x != "_"]
        lettered = ','.join(data)
        self.guessed_letters_display.configure(text=lettered)
    def guess_letter(self, event=None):
        letter = self.guess_entry.get()
        if letter == '':
            messagebox.showwarning("Warning", "Bạn chưa nhập chữ cái")
            return
        self.guess_entry.delete(0, 'end')
        self.hangman.init_letter(letter)
        self.update_word()
        self.update_guesses()
        self.update_guessed_letters()
        if self.hangman.check_win():
            self.win_game()
        elif self.hangman.guesses_left <= 0:
            self.lose_game()
    def win_game(self):
        messagebox.showinfo("Bạn thắng", "Từ là: {}".format(self.hangman.word))
        self.init_hangman()
    def lose_game(self):
        messagebox.showinfo("Bạn thua", "Từ là: {}".format(self.hangman.word))
        self.init_hangman()
    def reload_word(self):
        self.hangman = Hangman_init()
        self.update_word()
        self.update_guesses()
        self.update_guessed_letters()
        self.guess_entry.delete(0, 'end')
        
Hangman_UI(Tk())