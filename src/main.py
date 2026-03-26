import tkinter as tk
from ui import HandCricketUI

def main():
    root = tk.Tk()
    root.title("Hand Cricket Game")
    app = HandCricketUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
