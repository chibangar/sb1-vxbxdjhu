import os
import subprocess
import platform
import sys
from typing import List, Optional

class WindowsOptimizer:
    def __init__(self):
        self.check_os()
        
    def check_os(self) -> None:
        """Verify that the script is running on Windows."""
        if platform.system() != "Windows":
            print("Este script só pode ser executado em sistemas Windows.")
            sys.exit(1)

    def clean_temp_files(self) -> None:
        """Clean temporary files from Windows temp directories."""
        print("\n[1/3] Limpando arquivos temporários...")
        temp_paths = [
            os.getenv("TEMP"),
            os.path.join(os.getenv("SystemRoot", ""), "Temp")
        ]
        
        for path in temp_paths:
            if path and os.path.exists(path):
                try:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                            except Exception as e:
                                print(f"  ⚠️ Não foi possível remover {file}: {e}")
                except Exception as e:
                    print(f"  ⚠️ Erro ao acessar {path}: {e}")
        
        print("✅ Limpeza de arquivos temporários concluída")

    def disable_services(self) -> None:
        """Disable unnecessary Windows services."""
        print("\n[2/3] Desativando serviços desnecessários...")
        services = [
            "DiagTrack",  # Connected User Experiences and Telemetry
            "SysMain",    # Superfetch
            "WSearch",    # Windows Search
            "XboxGipSvc", # Xbox Peripheral Service
            "XblAuthManager", # Xbox Live Auth Manager
            "XblGameSave",    # Xbox Live Game Save
            "XboxNetApiSvc"   # Xbox Live Networking Service
        ]

        for service in services:
            try:
                subprocess.run(
                    ["sc", "config", service, "start=disabled"],
                    capture_output=True,
                    check=True
                )
                subprocess.run(
                    ["sc", "stop", service],
                    capture_output=True,
                    check=True
                )
                print(f"  ✅ Serviço {service} desativado")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Erro ao desativar {service}: {e}")

        print("✅ Desativação de serviços concluída")

    def optimize_registry(self) -> None:
        """Apply Windows Registry optimizations."""
        print("\n[3/3] Otimizando registro do Windows...")
        
        registry_commands = [
            # Desativar animações de menu
            'reg add "HKCU\\Control Panel\\Desktop" /v "MenuShowDelay" /t REG_SZ /d "0" /f',
            
            # Otimizar desempenho visual
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d "2" /f',
            
            # Desativar Cortana
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "AllowCortana" /t REG_DWORD /d "0" /f',
            
            # Otimizar cache do sistema de arquivos
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d "1" /f',
            
            # Melhorar resposta do menu iniciar
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "Start_ShowRun" /t REG_DWORD /d "1" /f'
        ]

        for command in registry_commands:
            try:
                subprocess.run(command, shell=True, check=True, capture_output=True)
                print(f"  ✅ Comando de registro executado com sucesso")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Erro ao executar comando de registro: {e}")

        print("✅ Otimização do registro concluída")

    def run(self) -> None:
        """Execute all optimization tasks."""
        print("🚀 Iniciando otimização do Windows...")
        
        try:
            self.clean_temp_files()
            self.disable_services()
            self.optimize_registry()
            
            print("\n✨ Otimização concluída com sucesso!")
            print("💡 Recomenda-se reiniciar o computador para aplicar todas as alterações.")
            
        except Exception as e:
            print(f"\n❌ Erro durante a otimização: {e}")
            print("Por favor, execute o script como administrador e tente novamente.")

if __name__ == "__main__":
    try:
        optimizer = WindowsOptimizer()
        optimizer.run()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")