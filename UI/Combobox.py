from tkinter import ttk, PhotoImage, Toplevel

from services.NuevaTB import crear_tb


class ComboboxUI:
    def __init__(self, root, bancos, conn):
        self.root = root
        self.bancos = bancos if bancos else ["Agregue un banco ->"]
        self.conn = conn
        self.combobox = self.crear_combobox_bancos(0, 0)

    def crear_combobox_bancos(self, row, column):
        frame = ttk.Frame(self.root)
        frame.grid(row=row, column=column, columnspan=2, padx=20, pady=20)

        bienvenido_label = ttk.Label(frame, text="Bienvenido al cajero de ")
        bienvenido_label.pack(side="left")

        combobox = ttk.Combobox(frame, values=self.bancos, state="readonly")
        combobox.pack(side="left")
        combobox.current(0)

        plus_image = PhotoImage(file="src/circle_plus_button.png")
        plus_image = plus_image.subsample(75, 75)
        plus_button = ttk.Button(frame, image=plus_image, command=lambda: self.crear_ventana_nueva_tabla())
        plus_button.image = plus_image
        plus_button.pack(side="left", padx=10)

        return combobox

    def crear_ventana_nueva_tabla(self):
        nueva_ventana = Toplevel(self.root)
        nueva_ventana.title("Nuevo banco")
        nueva_ventana.resizable(False, False)
        nueva_ventana.grab_set()

        window_width = nueva_ventana.winfo_reqwidth()
        window_height = nueva_ventana.winfo_reqheight()
        position_right = int(self.root.winfo_x() + self.root.winfo_width() / 2 - window_width / 2)
        position_down = int(self.root.winfo_y() + self.root.winfo_height() / 2 - window_height / 2)
        nueva_ventana.geometry("+{}+{}".format(position_right, position_down))

        frame = ttk.Frame(nueva_ventana, padding="20")
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text=f"Introduzca el nombre del nuevo banco:")
        label.pack(pady=5)

        entry = ttk.Entry(frame)
        entry.insert(0, "Nombre del banco")
        entry.bind("<FocusIn>", lambda event: entry.delete(0, "end") if entry.get() == "Nombre del banco" else None)
        entry.bind("<FocusOut>", lambda event: entry.insert(0, "Nombre del banco") if entry.get() == "" else None)
        entry.pack(padx=20, pady=20)

        aceptar_button = ttk.Button(frame, text="Aceptar", command=lambda: self.agregar_banco(entry.get(), nueva_ventana))
        aceptar_button.pack(side="right", padx=10)

        cancelar_button = ttk.Button(frame, text="Cancelar", command=nueva_ventana.destroy)
        cancelar_button.pack(side="left", padx=10)

    def agregar_banco(self, banco, nueva_ventana):
        crear_tb(banco, self.conn)
        if "Agregue un banco ->" in self.bancos:
            self.bancos.remove("Agregue un banco ->")
        self.bancos.append(banco)
        self.combobox["values"] = self.bancos
        self.combobox.current(len(self.bancos) - 1)
        self.combobox.update()
        nueva_ventana.destroy()
