import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
import re

# Import pour la gestion d'images (pip install pillow)
try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("ATTENTION: Installez 'pillow' pour les images (pip install pillow)")

# --- PALETTE COULEURS PRO ---
COLOR_BG = "#0b1120"        # Noir bleuté profond
COLOR_LOGIN_BG = "#050a14"  # Plus sombre pour le login
COLOR_SIDEBAR = "#151e32"   # Sidebar sombre
COLOR_ACCENT = "#00f2ea"    # Cyan Neon
COLOR_SIGNAL = "#39ff14"    # Vert Oscilloscope
COLOR_GRID = "#233554"      # Grille discret
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_DIM = "#94a3b8"
PASSWORD = "pwm"          # <-- MOT DE PASSE

# ==============================================================================
# CLASSE PRINCIPALE : GÈRE LA NAVIGATION
# ==============================================================================
class STM32App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("STM32 PROJECT | SECURE ACCESS")
        self.geometry("1150x700")
        self.configure(bg=COLOR_BG)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, DashboardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "DashboardPage":
            self.title("ENIT | PWM SIGNAL ANALYZER - DASHBOARD")

# ==============================================================================
# PAGE 1 : LOGIN ET PRÉSENTATION
# ==============================================================================
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLOR_LOGIN_BG)
        self.controller = controller

        # --- 1. AJOUT DE L'IMAGE DE FOND (BACKDROP) ---
        if HAS_PILLOW:
            try:
                # Charger l'image enit.png
                full_bg_img = Image.open("enit.png")
                # Redimensionner à la taille de la fenêtre (1150x700)
                full_bg_img = full_bg_img.resize((1150, 700), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(full_bg_img)
                
                # Créer un label pour l'image de fond
                bg_label = tk.Label(self, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                # Référence pour éviter le Garbage Collector
                bg_label.image = self.bg_photo
            except Exception as e:
                print(f"Erreur chargement fond : {e}")

        # --- 2. CONTENU (Superposé à l'image) ---
        # Note : On utilise des fonds transparents ou sombres pour les frames de texte
        
        # -- Header --
        header_frame = tk.Frame(self, bg=COLOR_LOGIN_BG) # Option: mettre un fond si illisible
        header_frame.pack(pady=(40, 10))
        tk.Label(header_frame, text="PROJET STM32", font=("Montserrat", 35, "bold"), fg="white", bg=COLOR_LOGIN_BG).pack()
        tk.Label(header_frame, text="Système d'Analyse PWM Sécurisé", font=("Arial", 14), fg=COLOR_ACCENT, bg=COLOR_LOGIN_BG).pack(pady=(5,0))
        tk.Frame(self, bg=COLOR_ACCENT, height=2, width=200).pack(pady=(0, 30))

        # -- Section Présentation --
        creators_frame = tk.Frame(self, bg=COLOR_LOGIN_BG)
        creators_frame.pack(expand=True)

        def create_profile_card(parent_frame, image_path, name, role):
            # On garde un fond pour les cartes pour qu'elles ressortent du background
            card = tk.Frame(parent_frame, bg=COLOR_SIDEBAR, bd=2, relief="ridge")
            card.pack(side="left", padx=30, ipadx=10, ipady=10)
            
            photo_frame = tk.Frame(card, bg=COLOR_ACCENT, padx=2, pady=2)
            photo_frame.pack(pady=(15, 10))
            
            img_label = tk.Label(photo_frame, text="PHOTO\nMANQUANTE", bg="#000", fg="white", width=20, height=10)
            
            if HAS_PILLOW:
                try:
                    pil_img = Image.open(image_path)
                    pil_img = pil_img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo_ref = ImageTk.PhotoImage(pil_img)
                    img_label.config(image=photo_ref, width=150, height=150, text="")
                    img_label.image = photo_ref
                except Exception:
                    pass
            
            img_label.pack()
            tk.Label(card, text=name, font=("Segoe UI", 18, "bold"), fg="white", bg=COLOR_SIDEBAR).pack(pady=(5,0))
            tk.Label(card, text=role, font=("Arial", 10, "italic"), fg=COLOR_TEXT_DIM, bg=COLOR_SIDEBAR).pack(pady=(0, 15))

        create_profile_card(creators_frame, "wael.png", "Wael GUESMI", "Étudiant ENIT")
        create_profile_card(creators_frame, "maha.png", "Maha ROMDHANI", "Étudiante ENIT")

        # -- Login Section --
        login_frame = tk.Frame(self, bg=COLOR_SIDEBAR, pady=20, padx=40)
        login_frame.pack(side="bottom", fill="x")

        tk.Label(login_frame, text="AUTHENTIFICATION REQUISE", font=("Arial", 11), fg=COLOR_TEXT_DIM, bg=COLOR_SIDEBAR).pack(pady=(0, 10))
        
        entry_frame = tk.Frame(login_frame, bg=COLOR_ACCENT, padx=1, pady=1)
        entry_frame.pack()
        self.password_entry = tk.Entry(entry_frame, show="•", font=("Arial", 16), width=20, bg="#0f1623", fg="white", bd=0, justify="center")
        self.password_entry.pack(ipady=5)
        self.password_entry.bind('<Return>', self.check_password)

        btn_login = tk.Button(login_frame, text="ACCÉDER AU DASHBOARD ➤", font=("Arial", 12, "bold"), 
                              bg=COLOR_ACCENT, fg="black", activebackground="#33fffd", relief="flat", 
                              command=self.check_password, padx=20, pady=10)
        btn_login.pack(pady=15)

    def check_password(self, event=None):
        if self.password_entry.get() == PASSWORD:
            self.controller.show_frame("DashboardPage")
            self.password_entry.delete(0, 'end')
        else:
            messagebox.showerror("Accès Refusé", "Mot de passe incorrect.")
            self.password_entry.delete(0, 'end')

# ==============================================================================
# PAGE 2 : LE DASHBOARD
# ==============================================================================
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLOR_BG)
        self.controller = controller

        self.serial_port = None
        self.is_reading = False
        self.current_duty = 50 
        self.current_freq = 1000 

        # --- SIDEBAR ---
        self.create_sidebar()

        # --- ZONE PRINCIPALE ---
        self.main_area = tk.Frame(self, bg=COLOR_BG)
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # En-tête
        tk.Label(self.main_area, text="DASHBOARD DE CONTROLE", bg=COLOR_BG, fg=COLOR_ACCENT, 
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Frame(self.main_area, bg=COLOR_ACCENT, height=2).pack(fill="x", pady=(5, 20))

        # --- INDICATEURS ---
        self.create_kpi_cards()

        # --- OSCILLOSCOPE ---
        self.create_oscilloscope()

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="ENIT", bg=COLOR_SIDEBAR, fg="white", font=("Impact", 45)).pack(pady=(40, 5))
        tk.Label(sidebar, text="GÉNIE ÉLECTRIQUE", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, font=("Arial", 10, "bold", "italic")).pack()

        tk.Frame(sidebar, bg=COLOR_GRID, height=2).pack(fill="x", padx=20, pady=20)

        tk.Label(sidebar, text="RÉALISÉ PAR :", bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack(pady=(10,5))
        tk.Label(sidebar, text="Wael GUESMI", bg=COLOR_SIDEBAR, fg="white", font=("Segoe UI", 18, "bold")).pack()
        tk.Label(sidebar, text="&", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, font=("Segoe UI", 12)).pack()
        tk.Label(sidebar, text="Maha ROMDHANI", bg=COLOR_SIDEBAR, fg="white", font=("Segoe UI", 18, "bold")).pack()

        tk.Frame(sidebar, bg=COLOR_GRID, height=2).pack(fill="x", padx=20, pady=20)

        tk.Label(sidebar, text="ENCADRÉ PAR :", bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack()
        tk.Label(sidebar, text="Mr. Khaled JLASSI", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, font=("Segoe UI", 14, "bold")).pack(pady=5)

        conn_frame = tk.Frame(sidebar, bg="#0f1623", pady=15)
        conn_frame.pack(side="bottom", fill="x")
        
        tk.Label(conn_frame, text="Port Série:", bg="#0f1623", fg="white").pack()
        self.port_combo = ttk.Combobox(conn_frame, state="readonly")
        self.port_combo.pack(fill="x", padx=20, pady=5)
        
        self.btn_connect = tk.Button(conn_frame, text="ACTIVER SYSTÈME", bg="#22c55e", fg="white", 
                                     font=("Arial", 11, "bold"), command=self.toggle_connection, relief="flat", pady=8)
        self.btn_connect.pack(fill="x", padx=20, pady=5)
        self.refresh_ports()

    def create_kpi_cards(self):
        kpi_frame = tk.Frame(self.main_area, bg=COLOR_BG)
        kpi_frame.pack(fill="x", pady=(0, 20))

        f_card = tk.LabelFrame(kpi_frame, text=" Fréquence (Hz) ", bg=COLOR_BG, fg="white", font=("Segoe UI", 12))
        f_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.lbl_freq = tk.Label(f_card, text="0000", bg=COLOR_BG, fg=COLOR_ACCENT, font=("Digital-7", 50, "bold"))
        self.lbl_freq.pack(pady=10)

        d_card = tk.LabelFrame(kpi_frame, text=" Rapport Cyclique (%) ", bg=COLOR_BG, fg="white", font=("Segoe UI", 12))
        d_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.lbl_duty = tk.Label(d_card, text="00 %", bg=COLOR_BG, fg="#facc15", font=("Digital-7", 50, "bold"))
        self.lbl_duty.pack(pady=10)

    def create_oscilloscope(self):
        tk.Label(self.main_area, text="VISUALISATION SIGNAL PWM", bg=COLOR_BG, fg="white", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 5))
        scope_frame = tk.Frame(self.main_area, bg="black", bd=5, relief="sunken")
        scope_frame.pack(fill="both", expand=True)
        self.canvas_scope = tk.Canvas(scope_frame, bg="black", height=300, highlightthickness=0)
        self.canvas_scope.pack(fill="both", expand=True)
        self.after(100, self.draw_grid_and_signal)

    def draw_grid_and_signal(self):
        try:
            w = self.canvas_scope.winfo_width()
            h = self.canvas_scope.winfo_height()
        except tk.TclError: return

        self.canvas_scope.delete("all")
        step = 50
        for i in range(0, w, step): self.canvas_scope.create_line(i, 0, i, h, fill=COLOR_GRID, dash=(2, 4))
        for i in range(0, h, step): self.canvas_scope.create_line(0, i, w, i, fill=COLOR_GRID, dash=(2, 4))
        
        if self.current_freq > 0:
            period_width = 250000 / self.current_freq
            period_width = max(10, min(500, period_width))
            
            amplitude = 80
            base_y = h/2 + 40
            top_y = base_y - amplitude * 2
            duty_ratio = self.current_duty / 100.0
            
            x = 10
            points = []
            while x < w:
                points.extend([x, base_y, x, top_y])
                x += period_width * duty_ratio
                points.extend([x, top_y, x, base_y])
                x += period_width * (1 - duty_ratio)
                points.extend([x, base_y])

            if len(points) > 2:
                self.canvas_scope.create_line(points, fill=COLOR_SIGNAL, width=3)

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports: self.port_combo.current(0)

    def toggle_connection(self):
        if not self.is_reading:
            port = self.port_combo.get()
            if not port: return
            try:
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.is_reading = True
                self.btn_connect.config(text="DÉCONNECTER", bg="#ef4444")
                threading.Thread(target=self.read_serial, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        else:
            self.is_reading = False
            if self.serial_port: self.serial_port.close()
            self.btn_connect.config(text="ACTIVER SYSTÈME", bg="#22c55e")

    def read_serial(self):
        while self.is_reading:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                    if line: self.after(0, self.parse_data, line)
            except: pass
            time.sleep(0.01)

    def parse_data(self, line):
        m_freq = re.search(r"Freq.*:\s*(\d+)", line)
        m_duty = re.search(r"Duty.*:\s*(\d+)", line)
        if m_freq:
            self.current_freq = int(m_freq.group(1))
            self.lbl_freq.config(text=f"{self.current_freq}")
        if m_duty:
            self.current_duty = int(m_duty.group(1))
            self.lbl_duty.config(text=f"{self.current_duty} %")
        self.draw_grid_and_signal()

if __name__ == "__main__":
    app = STM32App()
    app.mainloop()
