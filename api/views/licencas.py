import customtkinter as ctk
from tkinter import messagebox

from controllers.licenca_controller import (
    ativar_licenca,
    bloquear_licenca,
    validar_licenca
)


class TelaLicencas(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Controle de Licenças",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(self, text="Empresa").pack()
        self.entry_empresa = ctk.CTkEntry(self, width=300)
        self.entry_empresa.pack(pady=5)

        ctk.CTkLabel(self, text="Administrador").pack()
        self.entry_admin = ctk.CTkEntry(self, width=300)
        self.entry_admin.pack(pady=5)

        ctk.CTkLabel(self, text="Senha da Licença").pack()
        self.entry_codigo = ctk.CTkEntry(self, width=300, show="*")
        self.entry_codigo.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Ativar Licença",
            command=self.ativar
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Validar Licença",
            command=self.validar
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Bloquear Licença",
            command=self.bloquear
        ).pack(pady=10)

    def ativar(self):
        empresa = self.entry_empresa.get()
        codigo = self.entry_codigo.get()

        resposta = ativar_licenca(codigo, empresa)
        messagebox.showinfo("Licença", str(resposta))

    def validar(self):
        codigo = self.entry_codigo.get()

        resposta = validar_licenca(codigo)
        messagebox.showinfo("Licença", str(resposta))

    def bloquear(self):
        codigo = self.entry_codigo.get()

        resposta = bloquear_licenca(codigo)
        messagebox.showinfo("Licença", str(resposta))