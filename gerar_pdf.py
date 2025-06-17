from flask import Flask, current_app
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Logo
        app = current_app._get_current_object()
        logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 33)
            
        # Informações da empresa
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, 'Sergio Eduardo Padilha Corazzim', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 4, 'Avenida Pedro Botesi, 2352 - Jd Scomparim - Mogi Mirim - SP', 0, 1, 'C')
        self.cell(0, 4, 'WhatsApp: (19) 99676-0164', 0, 1, 'C')
        self.cell(0, 4, 'CNPJ: 08.101.093/0001-52', 0, 1, 'C')
        self.ln(5)
