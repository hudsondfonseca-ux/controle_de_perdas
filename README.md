# Sistema de Controle de Perdas Industrial

Uma aplicação desktop para gestão, rastreabilidade e auditoria de qualidade em linhas de produção. O sistema automatiza o cálculo de porcentagem de perda de materiais, valida critérios de qualidade em tempo real, mantém um histórico em banco de dados local e gera gráficos e relatórios para a tomada de decisão.

---

## 💡 Problemas que o Sistema Resolve

Em ambientes fabris e operacionais, a falta de padronização na medição de desperdícios gera prejuízos financeiros e atrasos na tomada de decisão. Este software resolve diretamente as seguintes dores:

* **Erros de cálculo manual:** Elimina falhas humanas na conversão de quilos para porcentagens de perda, garantindo precisão matemática constante.
* **Demora no isolamento de lotes com defeito:** O sistema emite um alerta imediato quando a perda ultrapassa a tolerância máxima (**0.30%**), evitando que lotes defeituosos avancem na linha de produção.
* **Falta de rastreabilidade (Auditabilidade):** Associa cada medição ao **nome do operador** e à **máquina responsável**, permitindo identificar gargalos operacionais ou necessidade de manutenção preventiva.
* **Perda de histórico operacional:** Substitui anotações em papel ou planilhas descentralizadas por um **banco de dados SQLite local**, imune a perda de arquivos.
* **Demora na prestação de contas:** Gera dashboards gráficos instantâneos e permite exportar relatórios prontos para o Excel em apenas um clique.

---

## ⚙️ Funcionalidades Principais

* **Interface Visual Moderna:** Desenvolvida em modo escuro com biblioteca `CustomTkinter`.
* **Mecanismo de Validação Automática:**
  * **≤ 0.30%:** Status **APROVADA** (Sinal verde — Produção pode continuar).
  * **> 0.30%:** Status **SEGREGADA** (Sinal vermelho — Requer paralisação/análise).
* **Banco de Dados Local (SQLite):** Registra automaticamente cada consulta com data e hora exatas.
* **Dashboard Gráfico:** Exibe as últimas 15 medições em formato de barras, com identificação por cores e linha indicadora do limite de tolerância.
* **Exportação para Excel:** Gera um arquivo `.csv` formatado nativamente no padrão brasileiro (separador `;` e codificação UTF-8).

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x** (Linguagem base)
* **CustomTkinter** (Interface gráfica do usuário)
* **SQLite3** (Banco de dados relacional embutido)
* **Matplotlib** (Geração de gráficos de desempenho)
* **CSV / Datetime** (Exportação de dados e tratamento de marcação temporal)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado em seu computador.

### 1. Clonar o repositório ou baixar o código
```bash
git clone [https://github.com/hudsondfonseca-ux/controle-de-perdas.git](https://github.com/hudsondfonseca-ux/controle-de-perdas.git)
cd controle-de-perdas
