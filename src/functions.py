def formatar_cpf(cpf_sem_formatacao):
    # cpf_numeros = ''.join(filter(str.isdigit, cpf_sem_formatacao))  # remove caracteres não numéricos
    # if len(cpf_numeros) != 11:
    #     raise ValueError("CPF deve conter 11 dígitos")
    # return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    numeros = ''.join(filter(str.isdigit, cpf_sem_formatacao))
    if len(numeros) == 11:
        # CPF: 999.999.999-99
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    elif len(numeros) == 14:
        # CNPJ: 99.999.999/9999-99
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
    else:
        raise ValueError("CPF deve conter 11 (CPF) ou 14 (CNPJ) dígitos")
