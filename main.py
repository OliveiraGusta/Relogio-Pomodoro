import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

TEMPO_TAREFA = 25 * 60
PAUSA_CURTA = 5 * 60
PAUSA_LONGA = 15 * 60

class RelogioPomodoro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x250")
        self.root.title("Relógio Pomodoro")
        self.style = Style(theme="minty")
        self.style.theme_use()


        self.tempo_label = tk.Label(self.root, text="25:00", font=("TkDefaultFont", 60))
        self.tempo_label.pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.iniciar_button = ttk.Button(button_frame, text="Iniciar", command=self.iniciar_relogio)
        self.iniciar_button.pack(side=tk.LEFT, padx=5)

        self.pausar_button = ttk.Button(button_frame, text="Pausar", command=self.pausar_relogio, style="secondary", state=tk.DISABLED)
        self.pausar_button.pack(side=tk.LEFT, padx=5)

        self.mais_5_min_button = ttk.Button(button_frame, text="+5 Min", command=self.adicionar_tempo)
        self.mais_5_min_button.pack(side=tk.LEFT, padx=5)

        self.menos_5_min_button = ttk.Button(button_frame, text="-5 Min", style="secondary",  command=self.subtrair_tempo)
        self.menos_5_min_button.pack(side=tk.LEFT, padx=5)

        self.tempo_tarefa, self.tempo_pausado = TEMPO_TAREFA, PAUSA_CURTA
        self.tarefa_esta_ativa, self.pomodoros_completo, self.esta_rodando = True, 0, False

        self.root.mainloop()

    
    def iniciar_relogio(self):
        self.iniciar_button.config(state=tk.DISABLED)
        self.pausar_button.config(state=tk.NORMAL)
        self.mais_5_min_button.config(state=tk.DISABLED)
        self.menos_5_min_button.config(state=tk.DISABLED)
        self.esta_rodando = True
        self.atualizar_relogio()

    def pausar_relogio(self):
        self.iniciar_button.config(state=tk.NORMAL)
        self.pausar_button.config(state=tk.DISABLED)
        self.mais_5_min_button.config(state=tk.NORMAL)
        self.menos_5_min_button.config(state=tk.NORMAL)
        self.esta_rodando = False

    def atualizar_relogio(self):
        if self.esta_rodando:
            if self.tarefa_esta_ativa:
                self.tempo_tarefa -= 1
                if self.tempo_tarefa == 0:
                    self.tarefa_esta_ativa = False
                    self.pomodoros_completo += 1
                    self.tempo_pausado = PAUSA_LONGA if self.pomodoros_completo % 4 == 0 else PAUSA_CURTA                
                    
                    messagebox.showinfo("Tarefa Concluida" if self.tarefa_esta_ativa % 2 == 0
                                        else "Bom Trabalho", "Tenha uma pausa longa descansar sua mente."
                                        if self.pomodoros_completo % 4 == 0
                                        else "Tenha uma pausa curta para esticar as pernas.")
            else:
                self.tempo_pausado -= 1
                if self.tempo_pausado == 0:
                   
                    self.tarefa_esta_ativa, self.tempo_tarefa = True, TEMPO_TAREFA

                    messagebox.showinfo("Hora de Trabalhar", "Volte para seu foco")      

            minutos, segundos = divmod(self.tempo_tarefa if self.tarefa_esta_ativa else self.tempo_pausado, 60)
            self.tempo_label.config(text="{:02d}:{:02d}".format(minutos, segundos))
            self.root.after(1000, self.atualizar_relogio)

    def adicionar_tempo(self):
        if not self.esta_rodando:
            if not self.tarefa_esta_ativa:
                self.tempo_pausado += 5 * 60
                self.atualizar_label()
            else:
                self.tempo_tarefa += 5 * 60
                self.atualizar_label()
        

    def subtrair_tempo(self):
        if not self.esta_rodando:
            if not self.tarefa_esta_ativa:
                self.tempo_pausado -= 5 * 60
                self.atualizar_label()
            else:
                self.tempo_tarefa -= 5 * 60
                if self.tempo_tarefa < 0:
                    self.tempo_tarefa = 0
                self.atualizar_label()

        
    
    def atualizar_label(self):
        if not self.tarefa_esta_ativa:
            minutos, segundos = divmod(self.tempo_pausado, 60)
            self.tempo_label.config(text="{:02d}:{:02d}".format(minutos, segundos))
        else:
            minutos, segundos = divmod(self.tempo_tarefa, 60)
            self.tempo_label.config(text="{:02d}:{:02d}".format(minutos, segundos))
     
RelogioPomodoro()