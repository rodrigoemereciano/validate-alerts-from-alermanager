import subprocess

def get_modified_files():
    """Obtém uma lista dos arquivos modificados no último commit."""
    result = subprocess.run(["git", "diff", "HEAD~1", "--name-only"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.split()
    else:
        raise RuntimeError("Falha ao obter arquivos modificados.")

def search_term_in_files(files, term):
    """Procura um termo nos arquivos fornecidos."""
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            if term in f.read():
                return True, file
    return False, None

# Executa as funções
try:
    modified_files = get_modified_files()
    term_found, file_with_term = search_term_in_files(modified_files, 'email_router')

    if term_found:
        print(f"O termo 'email_router' foi encontrado no arquivo: {file_with_term}")
    else:
        print("O termo 'email_router' não foi encontrado nos arquivos do último commit.")
except Exception as e:
    print(f"Erro: {e}")
