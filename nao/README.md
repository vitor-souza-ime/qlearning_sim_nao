# Q-Learning para Controle de Articulação do Robô NAO

Este projeto utiliza o algoritmo de **Q-Learning** para treinar o robô NAO a ajustar o ângulo de uma articulação específica (por padrão, o `LShoulderPitch`) até atingir um valor alvo. O treinamento considera interações reais com o robô, aplicando ações discretas e avaliando a recompensa com base na proximidade do ângulo atingido em relação ao alvo.

## 🚀 Tecnologias Utilizadas

* Python 2.7
* Naoqi SDK
* NumPy
* Robô NAO (físico ou simulado)
* Comunicação via IP

## 🧠 Descrição do Algoritmo

O agente utiliza o **Q-Learning**, uma técnica de aprendizado por reforço que busca aprender uma política ótima através da exploração e atualização de uma tabela Q.
Durante o processo:

1. A articulação começa em um ângulo atual.
2. O agente escolhe uma ação (movimento) com base em ε-greedy.
3. A ação é aplicada no robô, movendo a articulação.
4. A nova posição é avaliada e uma recompensa é atribuída.
5. A tabela Q é atualizada com base na recompensa e no melhor valor futuro estimado.

## ⚙️ Parâmetros

* `alpha`: Taxa de aprendizado (0.2)
* `gamma`: Fator de desconto (0.9)
* `epsilon`: Probabilidade de exploração (0.2)
* `n_actions`: Número de ações possíveis (5)
* `n_states`: Discretização do espaço de estados (100)
* `ANGLE_LIMIT`: Limite de movimento da articulação em radianos (±90°)
* `EPISODES`: Número de episódios de treinamento (100)
* `MAX_STEPS`: Passos por episódio (1)

## 📁 Arquivos

* `main.py`: Código principal com a lógica de conexão, execução e aprendizado.
* `qlearning_log_NAO.csv`: Log de cada episódio (recompensa, posição, etc.).
* `q_table.txt`: Arquivo onde a tabela Q pode ser salva (atualmente desabilitado).

## 📝 Como Usar

1. Conecte o robô NAO na mesma rede do seu computador.

2. Instale o SDK `naoqi` compatível com Python 2.7.

3. Edite a linha com o IP do seu robô:

   ```python
   robot_ip = "172.15.0.136"
   ```

4. Execute o script:

   ```bash
   python main.py
   ```

5. Acompanhe o log em `qlearning_log_NAO.csv`.

## 📊 Saída Esperada

Durante o treinamento, o terminal mostrará:

* Episódio atual
* Recompensa total
* Posição normalizada e em radianos
* Ângulo em graus
* Recompensa daquele passo
* Alerta se o alvo foi atingido

## ✅ Critério de Parada

O treinamento termina automaticamente se o ângulo da articulação atingir o valor alvo com uma tolerância de `±0.05 rad`.

## 📌 Observações

* Ajuste o nome da articulação (`joint_name`) caso queira treinar outra parte do robô.
* Os limites de ângulo podem ser refinados conforme os limites físicos do NAO.
* O código foi testado com a articulação `LShoulderPitch`.

