import os

from GUI import Application

os.environ.update(MIC='0')

if __name__ == '__main__':
    root = Application()
    root.mainloop()