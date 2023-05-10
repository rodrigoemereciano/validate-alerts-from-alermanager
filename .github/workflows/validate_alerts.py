import os
import re
import sys
import yaml

def validate_alerts(directory):
    # Verifica se o diretório possui um sufixo válido
    # print(directory)
    if any(directory.endswith(suffix) for suffix in ['-dev', '-hom', '-pro']):

        # Obtém a lista de arquivos YAML no diretório
        yaml_files = [file for file in os.listdir(directory) if re.match(r'.*\.(yaml|yml)$', file)]
        # print(yaml_files)
        # Variável para rastrear se ocorreu algum erro durante a validação
        error_found = False

        for file_name in yaml_files:
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                try:
                    alerts = yaml.safe_load(file)

                    for group in alerts.get('groups', []):
                        for rule in group.get('rules', []):
                            # print(rule)
                            expr = rule.get('expr', '')
                            severity = rule.get('labels', {}).get('severity', '')
                            channel = rule.get('labels', {}).get('channel', '')
                            annotations = rule.get('annotations', {})
                            labels = rule.get('labels', {})
                            alert_group = annotations.get('alert_group', '')
                            alert_type = annotations.get('alert_type', '')

                            # Verificar se o channel que tem valor service_now ou service_now_dev tem KB no Labels
                            if channel in ['service_now', 'service_now_dev'] and not any('kb' in key.lower() for key in labels.keys()):
                                # print(labels.keys())
                                print(
                                    f"Erro: O alerta {rule['alert']} no arquivo {file_name} não contém a chave 'kb' no campo 'labels'.")
                                error_found = True
                                continue

                            # Verifica se o parâmetro 'expr' começa com 'aws_' ou '(aws_' e contém '{account_id}'
                            if expr.startswith(('aws_', '(aws_')) and not re.search(r'(?i).*account_id.*', expr):
                                print(f"Erro: O alerta {rule['alert']} no arquivo {file_name} não contém o termo 'account_id' na expressão.")
                                error_found = True
                                continue

                            # Verifica se o parâmetro 'channel' possui um valor válido
                            if channel == 'email_router':
                                if 'email_to' not in rule.get('labels', {}):
                                    print(f"Erro: O alerta {rule['alert']} no arquivo {file_name} que usa 'email_router' precisa incluir 'email_to' no parâmetro 'labels'.")
                                    error_found = True
                                    continue

                            # Verificar se o parâmetro 'channel' possui um valor válido email_router, service_now ou service_now_dev
                            if channel not in ['email_router', 'service_now', 'service_now_dev']:
                                print(f"Erro: O alerta {rule['alert']} no arquivo {file_name} possui um valor inválido para o parâmetro 'channel'.")
                                error_found = True
                                continue

                            # Verificar se o channel que tem valor service_now ou service_now_dev tem no annotations o alert_group e o alert_type
                            if 'service_now' in channel or 'service_now_dev' in channel:
                                if not alert_group or not alert_type:
                                    print(f"Erro: O alerta {rule['alert']} no arquivo {file_name} que usa 'service_now' ou 'service_now_dev' precisa incluir 'alert_group' e 'alert_type' nos parâmetros 'annotations'.")
                                    error_found = True
                                    continue
                                    # Verifica se o parâmetro 'severity' possui um valor válido

                            # Verificar se o channel que tem valor service_now ou service_now_dev tem na severidade o valor critical ou major
                            if channel in ['service_now', 'service_now_dev'] and severity not in ['critical', 'major']:
                                print(f"Erro: O alerta {rule['alert']} no arquivo {file_name} tem uma gravidade inválida: {severity}")
                                error_found = True
                                continue


                except yaml.YAMLError as e:
                    print(f"Erro ao carregar o arquivo YAML {file_name}: {e}")
                    error_found = True

        # Verificação concluída sem erros
        if not error_found:
            print(f"Verificação concluída sem erros no diretorio: {directory}.")
        else:
            sys.exit(1)

#if __name__ == "__main__":
    # Exemplo de uso

directory = os.getcwd()
directories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
for dir_name in directories:
    validate_alerts(os.path.join(directory, dir_name))
