import tkinter as tk

from Components import RootApp


def main():
    root = tk.Tk()
    app = RootApp.Root(root)
    root.mainloop()


if __name__ == "__main__":
    main()
