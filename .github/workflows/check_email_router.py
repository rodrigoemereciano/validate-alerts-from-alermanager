import subprocess
import sys

# Executa o comando Git para obter a lista de arquivos modificados no último commit que contêm o termo 'email_router'
result = subprocess.run(["git", "diff", "HEAD~1", "--name-only", "|", "xargs", "grep", "-l", "email_router"], capture_output=True, text=True, shell=True)

# Verifica se o comando encontrou arquivos com o termo
if result.stdout:
    print("O termo 'email_router' foi encontrado nos seguintes arquivos do último commit:")
    print(result.stdout)
else:
    print("O termo 'email_router' não foi encontrado nos arquivos do último commit.")
    sys.exit(1)  # Sai com erro se o termo não for encontrado
