from tkinter import ttk, Toplevel, IntVar

from services.ReadTB import read_tb
from services.UpdateTB import update_cantidad


class TablaDinero:

    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.tabla = self.crear_tabla([], 1, 0)
        self.banco = None

    def crear_tabla(self, datos, start_row, column):
        tree = ttk.Treeview(self.root, columns=("moneda", "cantidad"), show="headings", height=len(datos) - 1)
        tree.heading("moneda", text="Moneda")
        tree.heading("cantidad", text="Cantidad")
        tree.grid(row=start_row, column=column, columnspan=2, padx=20, pady=(0, 10))
        for moneda, cantidad in datos:
            tree.insert("", "end", values=(f"{moneda} €", cantidad))
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightblue")

        for i, item in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.item(item, tags=("evenrow",))
            else:
                tree.item(item, tags=("oddrow",))
        tree.bind("<<TreeviewSelect>>", lambda event: self.editar_cantidad())

        return tree

    def editar_cantidad(self):
        selection = self.tabla.selection()
        if not selection:
            return

        item = selection[0]
        moneda, cantidad = self.tabla.item(item, "values")

        nueva_ventana = Toplevel(self.root)
        nueva_ventana.title("Modificar cantidad de {moneda}€")
        nueva_ventana.resizable(False, False)
        nueva_ventana.grab_set()

        window_width = nueva_ventana.winfo_reqwidth()
        window_height = nueva_ventana.winfo_reqheight()
        position_right = int(self.root.winfo_x() + self.root.winfo_width() / 2 - window_width / 2)
        position_down = int(self.root.winfo_y() + self.root.winfo_height() / 2 - window_height / 2)
        nueva_ventana.geometry("+{}+{}".format(position_right, position_down))

        frame = ttk.Frame(nueva_ventana, padding="20")
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text=f"Modificar cantidad de {moneda}")
        label.pack(pady=5)

        cantidad_original = cantidad
        entry_var = IntVar()
        entry_var.set(cantidad)
        entry_var.trace("w", lambda name, index, mode, sv=entry_var: self.actualizar_cantidad(item, sv.get()))

        spinbox = ttk.Spinbox(frame, from_=0, to=99999, textvariable=entry_var)
        spinbox.pack(padx=20, pady=20)

        aceptar_button = ttk.Button(frame, text="Aceptar",
                                    command=nueva_ventana.destroy)
        aceptar_button.pack(side="right", padx=10)

        cancelar_button = ttk.Button(frame, text="Cancelar", command=lambda: self.cancelar_cambio_cantidad(item, cantidad_original, nueva_ventana))
        cancelar_button.pack(side="left", padx=10)

    def actualizar_cantidad(self, item, cantidad):
        self.tabla.set(item, "cantidad", cantidad)
        moneda = self.tabla.item(item, "values")[0]
        moneda = moneda.split(" ")[0]
        moneda = float(moneda)
        update_cantidad(moneda, cantidad, self.banco, self.conn)

    def cancelar_cambio_cantidad(self, item, cantidad_original, nueva_ventana):
        self.tabla.set(item, "cantidad", cantidad_original)
        moneda = self.tabla.item(item, "values")[0]
        moneda = moneda.split(" ")[0]
        moneda = float(moneda)
        update_cantidad(moneda, cantidad_original, self.banco, self.conn)
        nueva_ventana.destroy()

    def cambio_tabla(self, banco):
        self.banco = banco
        datos = read_tb(banco, self.conn)

        self.tabla.destroy()
        self.tabla = self.crear_tabla(datos, 1, 0)
