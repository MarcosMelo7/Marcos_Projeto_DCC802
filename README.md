# Marcos_Projeto_DCC802
Repositório destinado a matéria: Projeto e Implementação de Sistemas - DCC802 

Este projeto é um utilitário de verificação e gerenciamento de sistema, basicamente um script desenvolvido em Python, que combina funcionalidades de verificação de malware, verificação de atualizações do Windows, visualização de informações do sistema e instalação de softwares populares (Google Chrome e Visual Studio Code) em uma interface gráfica amigável.

## Funcionalidades
Verificação de Malware: Executa uma verificação rápida de malware usando o Windows Defender.
Verificação de Atualizações do Windows: Verifica se há atualizações pendentes para o Windows.
Informações do Sistema: Exibe informações detalhadas sobre o uso de CPU, memória, disco e temperatura.
Instalação do Google Chrome: Verifica se o Google Chrome está instalado; caso contrário, baixa e instala.
Instalação do Visual Studio Code: Verifica se o Visual Studio Code está instalado; caso contrário, baixa e instala.
Interface Gráfica Intuitiva: Uma interface gráfica fácil de usar, construída com tkinter, que exibe o progresso de cada ação.

## Pré-requisitos
Python 3.6 ou superior
pip para gerenciar pacotes Python

## Como Usar
### Bibliotecas Python Necessárias
Certifique-se de instalar as bibliotecas Python necessárias executando o seguinte comando:
pip install psutil pywin32 wmi requests

Abra o arquivo: script.py no seu editor de código como o VSCode por exemplo e rode-o

## Documentação do Código
### Funções Principais
### 1. open_windows_update_settings()
- Abre as configurações do Windows Update para o usuário.

### 2. run_windows_defender_scan(progress_bar, progress_label, output_text, root)
- Executa uma verificação rápida de malware usando o Windows Defender.
- Exibe uma barra de progresso enquanto a verificação está em andamento.
- Atualiza a interface com o resultado da verificação.
  
### 3. check_windows_updates(progress_bar, progress_label, output_text, root, settings_button)
- Verifica atualizações disponíveis para o Windows usando comandos PowerShell.
- Exibe uma barra de progresso durante a verificação.
- Ao final, permite ao usuário abrir as configurações do Windows Update.
  
### 4. system_info(progress_bar, progress_label, output_text, root)
- Coleta e exibe informações detalhadas do sistema: CPU, memória, disco, temperatura.
- Utiliza as bibliotecas psutil e wmi para obter dados.
  
### 5. install_google_chrome(output_text)
- Verifica se o Google Chrome está instalado.
- Se não estiver, baixa o instalador do Google Chrome e realiza a instalação.
- Exibe o progresso do download e o resultado da instalação.

### 6. install_visual_studio_code(output_text)
- Semelhante ao instalador do Chrome; verifica, baixa e instala o Visual Studio Code.
- Exibe o progresso do download e o resultado da instalação.
  
## Funções de Suporte

### 7. run_in_thread(function, *args)
- Executa qualquer função em um novo thread para evitar que a GUI congele durante operações demoradas.

### 8. create_gui()
- Cria a interface gráfica usando tkinter.
- Configura botões, barras de progresso e campos de texto para exibição de informações.
- Configurações iniciais da janela (como tamanho) são definidas aqui.

## Fluxo Principal
- if __name__ == "__main__": create_gui()
- Ponto de entrada do script, inicializando a interface gráfica ao executar o script.
  
Essa documentação cobre todos os detalhes necessários para entender, instalar, usar e contribuir para o projeto!
