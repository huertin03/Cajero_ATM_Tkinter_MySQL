from UI.Combobox import ComboboxUI
from UI.SeccionCompra import SeccionCompra
from UI.Table import TablaDinero


class GUI:
    def __init__(self, root, bancos, conn):
        self.root = root
        self.bancos = bancos if bancos else ["Agregue un banco ->"]
        self.comboboxUI = ComboboxUI(root, bancos, conn)
        self.TablaDinero = TablaDinero(root, conn)
        self.SeccionCompra = SeccionCompra(root, conn, self.TablaDinero)
        self.conn = conn

        self.comboboxUI.combobox.bind("<<ComboboxSelected>>", lambda event: (self.TablaDinero.cambio_tabla(self.comboboxUI.combobox.get()), self.SeccionCompra.set_banco(self.comboboxUI.combobox.get())))

    def start(self):
        combobox = self.comboboxUI.combobox
        self.TablaDinero.cambio_tabla(combobox.get())
        self.SeccionCompra.set_banco(combobox.get())
        self.root.mainloop()
