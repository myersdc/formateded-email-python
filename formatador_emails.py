import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, font
import os
import webbrowser

def animate_text(label, text, delay=100):
    def loop_text():
        if label.winfo_exists():
            nonlocal index
            index = (index + 1) % (len(text) + 1)
            label.config(text=text[:index])
            label.after(delay, loop_text)

    index = 0
    loop_text()

def create_gradient_frame(app):
    canvas = tk.Canvas(app, height=300, width=400)
    canvas.pack(fill="both", expand=True)
    
    gradient_color1 = "#6e48aa"
    gradient_color2 = "#9d50bb"
    canvas.create_rectangle(0, 0, 400, 300, fill=gradient_color1, outline="")
    
    for i in range(0, 400, 4):
        color = "#" + "".join([hex(int(gradient_color1[j:j+2], 16) + int((int(gradient_color2[j:j+2], 16) - int(gradient_color1[j:j+2], 16)) * i / 400))[2:] for j in (1, 3, 5)])
        canvas.create_rectangle(i, 0, i + 4, 300, fill=color, outline="")
    
    return canvas

def processar_arquivo(input_path, log_area):
    try:
        with open(input_path, 'r') as file:
            linhas = file.readlines()

        linhas_processadas = []
        for linha in linhas:
            if '|' in linha:
                conta_formatada = linha.split(' | ')[0].strip()
                linhas_processadas.append(conta_formatada)
                log_area.insert(tk.END, f"Processado: {conta_formatada}\n")
                log_area.update_idletasks()

        output_dir = filedialog.askdirectory(title="Selecione a pasta para salvar o arquivo formatado")

        if not output_dir:
            messagebox.showwarning("Aviso", "Nenhum diretório selecionado. O processo foi cancelado.")
            return

        output_name = os.path.basename(input_path).replace(".txt", "_formatado.txt")
        output_path = os.path.join(output_dir, output_name)

        with open(output_path, 'w') as file:
            for linha in linhas_processadas:
                file.write(linha + '\n')

        messagebox.showinfo("Concluído", f"Processamento concluído. Emails formatados salvos em: {output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo(log_area):
    initial_dir = 'C:/' if os.name == 'nt' else os.path.expanduser('~')
    caminho_arquivo = filedialog.askopenfilename(
        initialdir=initial_dir, 
        filetypes=[("Text files", "*.txt")], 
        title="Selecione um arquivo .txt"
    )
    if caminho_arquivo:
        processar_arquivo(caminho_arquivo, log_area)

def alternar_tema(app, log_area, widgets, botao_tema, tema_atual):
    cores = {
        "claro": {"bg": "white", "fg": "black", "botao": "🌙"},
        "escuro": {"bg": "gray20", "fg": "white", "botao": "🌞"}
    }

    novo_tema = "escuro" if tema_atual == "claro" else "claro"
    app.config(bg=cores[novo_tema]["bg"])
    log_area.config(bg=cores[novo_tema]["bg"], fg=cores[novo_tema]["fg"])
    
    estilo_botao = {'font': ("Segoe UI", 12), 'bg': "#D6D6D6" if novo_tema == "claro" else "gray20", 'fg': "black" if novo_tema == "claro" else "white", 'activebackground': "#A0A0A0", 'borderwidth': 1, 'highlightthickness': 1, 'highlightcolor': "#D6D6D6", 'highlightbackground': "#D6D6D6", 'relief': 'raised'}

    for widget in widgets.values():
        widget.config(bg=cores[novo_tema]["bg"], fg=cores[novo_tema]["fg"])
        if isinstance(widget, tk.Button):
            widget.config(**estilo_botao)

    botao_tema.config(text=cores[novo_tema]["botao"], command=lambda: alternar_tema(app, log_area, widgets, botao_tema, novo_tema))

def abrir_discord():
    webbrowser.open("https://discord.gg/FWN8PNAywt")

def criar_barra_menu(app):
    menubar = tk.Menu(app)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Sobre", command=lambda: messagebox.showinfo("Sobre", "Formatador de Emails v1.0\nDesenvolvido por Myers Vasiliev"))
    helpmenu.add_command(label="Discord", command=abrir_discord)
    menubar.add_cascade(label="Ajuda", menu=helpmenu)

    app.config(menu=menubar)

def criar_janela_principal(app):
    app.title("Formatador de Emails - Myers Vasiliev")
    app.geometry("650x500")  
    app.config(bg="#F0F0F0") 

    criar_barra_menu(app) 

    msg_bem_vindo = tk.Label(app, text="Bem-vindo ao Formatador de Emails", font=("Segoe UI", 16), bg="#F0F0F0")
    msg_bem_vindo.pack(pady=20)

    estilo_botao = {'font': ("Segoe UI", 12), 'bg': "#D6D6D6", 'fg': "black", 'activebackground': "#A0A0A0", 'borderwidth': 1, 'highlightthickness': 1, 'highlightcolor': "#D6D6D6", 'highlightbackground': "#D6D6D6", 'relief': 'raised'}

    def on_enter(e, btn):
        btn['background'] = '#A0A0A0'

    def on_leave(e, btn):
        btn['background'] = estilo_botao['bg']

    botao_formatar = tk.Button(app, text="Formatar Emails", height=2, width=20, **estilo_botao)
    botao_formatar.pack(pady=10)
    botao_formatar.bind("<Enter>", lambda e, btn=botao_formatar: on_enter(e, btn))
    botao_formatar.bind("<Leave>", lambda e, btn=botao_formatar: on_leave(e, btn))

    botao_sair = tk.Button(app, text="❌ Sair", command=app.quit, height=2, width=20, **estilo_botao)
    botao_sair.pack(pady=10)
    botao_sair.bind("<Enter>", lambda e, btn=botao_sair: on_enter(e, btn))
    botao_sair.bind("<Leave>", lambda e, btn=botao_sair: on_leave(e, btn))

    github_label = tk.Label(app, text="Visite meu GitHub: github.com/myersdc", font=("Segoe UI", 10), bg="#F0F0F0")
    github_label.pack(side="bottom", pady=10)

    log_area = scrolledtext.ScrolledText(app, height=12, width=58, font=("Segoe UI", 10))
    log_area.pack(pady=10)

    botao_formatar.config(command=lambda: selecionar_arquivo(log_area))

    botao_tema = tk.Button(app, text="🌙", height=1, width=3, **estilo_botao)
    botao_tema.place(relx=0.95, rely=0.95)

    widgets = {"msg_bem_vindo": msg_bem_vindo, "botao_formatar": botao_formatar, "botao_sair": botao_sair, "github_label": github_label}
    botao_tema.config(command=lambda: alternar_tema(app, log_area, widgets, botao_tema, "claro"))

def mostrar_boas_vindas():
    welcome_app = tk.Tk()
    welcome_app.title("Myers Vasiliev")
    welcome_app.geometry("400x300")
    welcome_app.configure(bg="#345")

    gradient_canvas = create_gradient_frame(welcome_app)

    mensagem = tk.Label(welcome_app, text="", font=("Helvetica", 16, "bold"), bg="#6e48aa", fg="white")
    mensagem.place(relx=0.5, rely=0.4, anchor="center")
    animate_text(mensagem, "Starting engine...")

    progress = ttk.Progressbar(welcome_app, orient="horizontal", length=300, mode="determinate")
    progress.place(relx=0.5, rely=0.6, anchor="center")
    progress.start(10) 

    welcome_app.after(5000, lambda: [welcome_app.destroy(), criar_janela_principal(tk.Tk())])
    welcome_app.mainloop()

if __name__ == "__main__":
    mostrar_boas_vindas()
