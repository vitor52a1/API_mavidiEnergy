from flask import Flask, request, jsonify

app = Flask(__name__)

# Função para calcular o valor da tarifa sem desconto, incluindo bandeira e impostos
def calcular_tarifa(consumo_kwh, tarifa_kwh, bandeira, icms_percent, pis_percent, cofins_percent, tasa_distribuicao,
                    tasa_energia):
    valor_energia = consumo_kwh * tarifa_kwh

    # Aplicando a bandeira tarifária
    if bandeira == "verde":
        valor_bandeira = 0
        cor_bandeira = "Verde"
    elif bandeira == "amarela":
        valor_bandeira = 0.02 * consumo_kwh
        cor_bandeira = "Amarela"
    elif bandeira == "vermelha":
        valor_bandeira = 0.05 * consumo_kwh
        cor_bandeira = "Vermelha"
    else:
        raise ValueError("Bandeira tarifária inválida")

    # Cálculo dos impostos e taxas
    imposto_icms = valor_energia * (icms_percent / 100)
    imposto_pis = valor_energia * (pis_percent / 100)
    imposto_cofins = valor_energia * (cofins_percent / 100)

    valor_distribuicao = consumo_kwh * tasa_distribuicao
    valor_energia_total = consumo_kwh * tasa_energia

    valor_sem_desconto = (valor_energia + valor_bandeira + imposto_icms + imposto_pis + imposto_cofins +
                          valor_distribuicao + valor_energia_total)

    return round(valor_sem_desconto, 2), cor_bandeira

# Função para calcular economia
def calcular_economia(valor_sem_desconto, percentual_economia):
    economia = valor_sem_desconto * (percentual_economia / 100)
    valor_com_desconto = valor_sem_desconto - economia
    return round(economia, 2), round(valor_com_desconto, 2)

@app.route('/calcular_tarifa', methods=['GET'])
def calcular_tarifa_api():
    try:
        # Coletar os parâmetros da requisição
        cidade = request.args.get('cidade').strip()  # Nome da cidade
        bandeira = request.args.get('bandeira').strip().lower()  # Bandeira tarifária
        consumo = float(request.args.get('consumo'))  # O consumo em kWh

        # Validar bandeira
        if bandeira not in ['verde', 'amarela', 'vermelha']:
            return jsonify({"error": "Bandeira inválida. Deve ser 'verde', 'amarela' ou 'vermelha'."}), 400

        # Valores fixos para os cálculos
        tarifa = 0.60  # tarifa de energia em R$/kWh
        icms = 18  # ICMS de 18%
        pis = 1.65  # PIS de 1.65%
        cofins = 7.6  # Cofins de 7.6%
        distribuicao = 0.10  # Taxa de distribuição por kWh
        energia = 0.05  # Taxa de energia por kWh

        # Calcular o valor sem desconto e a cor da bandeira
        valor_sem_desconto, cor_bandeira = calcular_tarifa(consumo, tarifa, bandeira, icms, pis, cofins, distribuicao, energia)

        # Calcular a economia de 50% e o valor com desconto
        economia, valor_com_desconto = calcular_economia(valor_sem_desconto, 50)

        # Retornar o resultado como JSON
        return jsonify({
            "cidade": cidade,
            "bandeira": cor_bandeira,
            "consumo_kwh": consumo,
            "valor_sem_desconto": valor_sem_desconto,
            "economia_potencial": economia,
            "valor_com_desconto": valor_com_desconto
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

