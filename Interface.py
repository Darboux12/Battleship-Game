from tkinter import *

class Graphics:

    def __init__(self, MyWindow):

        self.message_text = StringVar()
        self.message_text.set("Witam w grze Okręty! \n Naciśnij START, aby rozpocząć!")
        self.komunikat = Label(MyWindow, textvariable=self.message_text, font="Times 17", relief="ridge", bd=10,
                               width=28, padx=2, pady=2, height=3).place(x=375, y=535)

        self.previous_text = ''

        self.ship_prefix = ['jedno', 'dwu', 'trzy', 'cztero']

        self.title_one = Label(MyWindow, font="Times 20", text="GRACZ 1", fg="blue").place(x=185, y=25)
        self.title_two = Label(MyWindow, font="Times 20", text="GRACZ 2", fg="blue").place(x=688, y=25)

    #    self.ship_image = PhotoImage(file="warship.png")
    #    self.ship_image2 = PhotoImage(file="warship2.png")

        self.ship_label = Label(MyWindow,  bg='green').place(x=10, y=500)
        self.ship_labe2 = Label(MyWindow,  bg='green').place(x=800, y=500)

    def reset(self,start = False):
        if start == False:
            self.message_text.set("Witam w grze Okręty! \n Nacisnij START, aby rozpocząć")
        else:
            self.message_text.set('')

class MyWindow(Tk):

    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Okręty")
        self.configure(bg="green")

class MyFrame(Frame):

    def __init__(self, window):
        super().__init__(window)


