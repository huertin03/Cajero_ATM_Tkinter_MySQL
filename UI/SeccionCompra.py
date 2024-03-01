from tkinter import ttk, Text

from UI.Table import TablaDinero
from actions.Comparar import comparar_pago
from actions.Evaluar import *
from actions.Vueltas import Vueltas


class SeccionCompra:

    def __init__(self, root, conn, tabla_dinero):
        self.root = root
        self.conn = conn
        self.banco = None
        self.TablaDinero = tabla_dinero
        self.ui_frame = self.crear_ui_frame()
        self.compra_entry = self.crear_spinbox_con_label(self.ui_frame, "Compra: ", 1, 1)
        self.pago_entry = self.crear_entry_con_label(self.ui_frame, "Pago: ", 2, 1)
        self.vueltas_entry = self.crear_text_con_label(self.ui_frame, "Vueltas: ", 3, 1)
        self.efectuar_compra = self.create_button(self.ui_frame, "Efectuar compra", 4, 1)
        self.compra = None
        self.pago = None
        self.vueltas = None

    def crear_ui_frame(self):
        ui_frame = ttk.Frame(self.root)
        ui_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        return ui_frame

    @staticmethod
    def create_spinbox(parent, row, column):
        spinbox = ttk.Spinbox(parent, from_=0.0, to=99999.99, increment=0.01, format="%.2f")
        spinbox.grid(row=row, column=column, pady=5)
        return spinbox

    def crear_text_con_label(self, parent, texto, row, column):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=column, columnspan=2, pady=(0, 5))
        self.create_label(frame, texto, 0, 0)
        return self.create_text(frame, 1, 0)

    @staticmethod
    def create_text(parent, row, column):
        text = Text(parent, height=5, width=45)
        text.grid(row=row, column=column)
        text.config(state='disabled')
        return text

    def crear_spinbox_con_label(self, parent, texto, row, column):
        self.create_label(parent, texto, row, column)
        return self.create_spinbox(parent, row, column + 1)

    def create_button(self, parent, text, row, column):
        button = ttk.Button(parent, text=text, command=self.efectuar_compra)
        button.grid(row=row, column=column, columnspan=2, pady=10)
        return button

    @staticmethod
    def create_entry(parent, row, column):
        placeholder = '"1-200#1-100" = 300€'
        entry = ttk.Entry(parent)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end') if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda args: entry.insert(0, placeholder) if entry.get() == "" else None)
        entry.grid(row=row, column=column, pady=5)
        return entry

    def crear_entry_con_label(self, parent, texto, row, column):
        self.create_label(parent, texto, row, column)
        return self.create_entry(parent, row, column + 1)

    @staticmethod
    def create_label(parent, texto, row, column):
        label = ttk.Label(parent, text=texto)
        label.grid(row=row, column=column)
        return label

    def efectuar_compra(self):
        self.evaluar_entradas()
        self.TablaDinero.cambio_tabla(self.banco)
        if self.vueltas_entry.get(1.0, 'end-1c').startswith("Pago realizado"):
            self.limpiar_entradas()

    def evaluar_entradas(self):
        self.compra = self.compra_entry.get()
        self.pago = self.pago_entry.get()

        if not evaluar_importe(self.compra):
            self.set_vueltas_entry("Importe incorrecto! Vuelva a intentarlo.")
            return

        pago_correcto = evaluar_pago(self.pago)

        if not pago_correcto:
            self.set_vueltas_entry(f"Pago incorrecto! Vuelva a intentarlo.")
            return

        vueltas = comparar_pago(self.pago, float(self.compra))

        if vueltas < 0:
            self.set_vueltas_entry(f"El pago no es suficiente! Faltan {abs(vueltas)} €.")
            return

        vu = Vueltas(self.conn, self.banco)

        if vueltas == 0:
            vu.llenar_tb(self.pago)
            self.set_vueltas_entry("Pago realizado con éxito!")
            return
        else:
            if vu.devolver_vueltas(round(vueltas, 2)):
                vu.llenar_tb(self.pago)
                self.set_vueltas_entry(f"Pago realizado con éxito!" +
                                       "\n" + f"No olvide coger el cambio: {round(vueltas, 2)} €.")
                return
            else:
                self.set_vueltas_entry("Cajero no dispone de los fondos necesarios para devolverte las vueltas." +
                                       "\n" + "No olvidé su pago.")
                return

    def set_vueltas_entry(self, text):
        self.vueltas_entry.config(state='normal')
        self.vueltas_entry.delete(1.0, 'end')
        self.vueltas_entry.insert(1.0, text)
        self.vueltas_entry.config(state='disabled')

    def limpiar_entradas(self):
        self.compra_entry.delete(0, 'end')
        self.pago_entry.delete(0, 'end')

    def set_banco(self, banco):
        self.banco = banco
