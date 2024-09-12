import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import font
import psutil
import subprocess
import threading
import os
import win32com.client
import pythoncom
import requests
import tempfile

def open_windows_update_settings():
    os.system("start ms-settings:windowsupdate")

def run_windows_defender_scan(progress_bar, progress_label, output_text, root):
    try:
        progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        progress_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        progress_bar.start(10)
        progress_label.config(text="Verificando Malware...")

        output_text.delete(1.0, tk.END)

        command = "powershell.exe Start-MpScan -ScanType QuickScan"
        process = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = process.stdout
        error = process.stderr

        if process.returncode == 0:
            result = "Verificação rápida concluída com sucesso.\n"
            result += output
            if "Threat" in output or "threat" in output:
                result += "\nMalware detectado!"
            else:
                result += "\nNenhum malware detectado."
        else:
            result = f"Erro durante a verificação. Código de retorno: {process.returncode}\nErro: {error}"

        output_text.insert(tk.END, result + "\n", "center")

    except Exception as e:
        output_text.insert(tk.END, f"Ocorreu um erro ao tentar executar a verificação de malware: {str(e)}\n", "center")

    finally:
        progress_bar.stop()
        progress_label.config(text="Verificação Concluída")
        progress_bar.place_forget()
        progress_label.place_forget()

def check_windows_updates(progress_bar, progress_label, output_text, root, settings_button):
    try:
        progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        progress_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        progress_bar.start(10)
        progress_label.config(text="Verificando Atualizações...")

        output_text.delete(1.0, tk.END)

        command = "powershell.exe (New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search('IsInstalled=0')"
        process = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = process.stdout
        error = process.stderr

        if process.returncode == 0:
            result = "Verificação de atualizações concluída com sucesso.\n"
            result += output
            if "Updates" in output or "updates" in output:
                result += "\nAtualizações disponíveis!"
            else:
                result += "\nNenhuma atualização disponível."
        else:
            result = f"Erro durante a verificação de atualizações. Código de retorno: {process.returncode}\nErro: {error}"

        output_text.insert(tk.END, result + "\n", "center")

    except Exception as e:
        output_text.insert(tk.END, f"Ocorreu um erro ao tentar verificar atualizações: {str(e)}\n", "center")

    finally:
        progress_bar.stop()
        progress_label.config(text="Verificação Concluída")
        progress_bar.place_forget()
        progress_label.place_forget()
        settings_button.pack(pady=5)

def system_info(progress_bar, progress_label, output_text, root):
    try:
        pythoncom.CoInitialize()

        progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        progress_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        progress_bar.start(10)
        progress_label.config(text="Coletando Informações do Sistema...")

        output_text.delete(1.0, tk.END)

        result = "Informações básicas do sistema:\n"

        cpu_usage = psutil.cpu_percent(interval=1)
        result += f"Uso de CPU: {cpu_usage}%\n"

        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024 ** 3)
        available_memory = memory.available / (1024 ** 3)
        memory_usage = memory.percent
        result += f"Memória total: {total_memory:.2f} GB\n"
        result += f"Memória disponível: {available_memory:.2f} GB\n"
        result += f"Uso de memória: {memory_usage}%\n"

        disk = psutil.disk_usage('/')
        total_disk = disk.total / (1024 ** 3)
        used_disk = disk.used / (1024 ** 3)
        free_disk = disk.free / (1024 ** 3)
        disk_usage = disk.percent
        result += f"Disco total: {total_disk:.2f} GB\n"
        result += f"Disco usado: {used_disk:.2f} GB\n"
        result += f"Disco livre: {free_disk:.2f} GB\n"
        result += f"Uso de disco: {disk_usage}%\n"

        try:
            w = win32com.client.GetObject("winmgmts://./root/wmi")
            temperature_info = w.ExecQuery("Select * from MSAcpi_ThermalZoneTemperature")
            for sensor in temperature_info:
                temperature = sensor.CurrentTemperature / 10.0 - 273.15
                result += f"Temperatura do sensor: {temperature:.2f} °C\n"
        except Exception as e:
            result += f"Não foi possível obter a temperatura da CPU: {str(e)}\n"

        output_text.insert(tk.END, result + "\n", "center")

    finally:
        progress_bar.stop()
        progress_label.config(text="Informações do Sistema Coletadas")
        progress_bar.place_forget()
        progress_label.place_forget()

def install_google_chrome(output_text):
    try:
        chrome_installer_url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"

        # Baixa o instalador com acompanhamento do progresso
        response = requests.get(chrome_installer_url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as f:
                chunk_size = 8192
                downloaded = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_percentage = (downloaded / total_size) * 100
                    output_text.delete(1.0, tk.END)
                    output_text.insert(tk.END, f"Baixando Google Chrome: {progress_percentage:.2f}% concluído\n", "center")
                    output_text.update_idletasks()
                installer_path = f.name

            output_text.insert(tk.END, "Instalador do Google Chrome baixado com sucesso. Iniciando a instalação...\n", "center")
            
            # Executa o instalador
            process = subprocess.run(installer_path, shell=True)
            if process.returncode == 0:
                output_text.insert(tk.END, "Google Chrome instalado com sucesso!\n", "center")
            else:
                output_text.insert(tk.END, "Erro durante a instalação do Google Chrome.\n", "center")
            
            # Limpa o instalador após a instalação
            os.remove(installer_path)
        else:
            output_text.insert(tk.END, "Erro ao baixar o instalador do Google Chrome.\n", "center")

    except Exception as e:
        output_text.insert(tk.END, f"Ocorreu um erro ao tentar instalar o Google Chrome: {str(e)}\n", "center")

def install_visual_studio_code(output_text):
    try:
        vscode_installer_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"

        # Baixa o instalador com acompanhamento do progresso
        response = requests.get(vscode_installer_url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as f:
                chunk_size = 8192
                downloaded = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_percentage = (downloaded / total_size) * 100
                    output_text.delete(1.0, tk.END)
                    output_text.insert(tk.END, f"Baixando Visual Studio Code: {progress_percentage:.2f}% concluído\n", "center")
                    output_text.update_idletasks()
                installer_path = f.name

            output_text.insert(tk.END, "Instalador do Visual Studio Code baixado com sucesso. Iniciando a instalação...\n", "center")
            
            # Executa o instalador
            process = subprocess.run(installer_path, shell=True)
            if process.returncode == 0:
                output_text.insert(tk.END, "Visual Studio Code instalado com sucesso!\n", "center")
            else:
                output_text.insert(tk.END, "Erro durante a instalação do Visual Studio Code.\n", "center")
            
            # Limpa o instalador após a instalação
            os.remove(installer_path)
        else:
            output_text.insert(tk.END, "Erro ao baixar o instalador do Visual Studio Code.\n", "center")

    except Exception as e:
        output_text.insert(tk.END, f"Ocorreu um erro ao tentar instalar o Visual Studio Code: {str(e)}\n", "center")

def run_in_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Verificação do Sistema")
    root.geometry("1000x800")  # Definindo a geometria inicial maior

    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

    output_text = scrolledtext.ScrolledText(root, width=100, height=30, font=custom_font)
    output_text.pack(pady=10)
    output_text.tag_configure("center", justify='center')

    progress_label = tk.Label(root, text="", font=custom_font)
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")

    settings_button = tk.Button(root, text="Abrir Configurações do Windows Update", command=open_windows_update_settings)

    btn_malware = tk.Button(root, text="Verificar Malware", 
                            command=lambda: run_in_thread(run_windows_defender_scan, progress_bar, progress_label, output_text, root))
    btn_malware.pack(pady=5)

    btn_updates = tk.Button(root, text="Verificar Atualizações", 
                            command=lambda: run_in_thread(check_windows_updates, progress_bar, progress_label, output_text, root, settings_button))
    btn_updates.pack(pady=5)

    btn_system_info = tk.Button(root, text="Informações do Sistema", 
                                command=lambda: run_in_thread(system_info, progress_bar, progress_label, output_text, root))
    btn_system_info.pack(pady=5)

    btn_install_chrome = tk.Button(root, text="Instalar Google Chrome", 
                                   command=lambda: run_in_thread(install_google_chrome, output_text))
    btn_install_chrome.pack(pady=5)

    btn_install_vscode = tk.Button(root, text="Instalar Visual Studio Code", 
                                   command=lambda: run_in_thread(install_visual_studio_code, output_text))
    btn_install_vscode.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
