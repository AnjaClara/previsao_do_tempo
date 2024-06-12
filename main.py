import tkinter as tk
from login import LoginCadastro

# Herança
class MainApp(LoginCadastro):
    def __init__(self, root):
        super().__init__(root)

def main():
    root = tk.Tk()
    MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
