from ttkthemes.themed_tk import ThemedTk

from services.Database import Database
from UI.Gui import GUI
from services.TBExistentes import get_tables


def main(conn):
    root = ThemedTk(theme="breeze")
    root.title("Cajero")
    bancos = get_tables(conn)
    gui = GUI(root, bancos, conn)

    gui.start()


if __name__ == "__main__":
    db = Database()
    conn = db.connect()
    main(conn)
