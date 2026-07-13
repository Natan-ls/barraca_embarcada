# 🎪 Barraca Embarcada - Sistema de Gestão de Pedidos (Edge POS & Digital Signage)

Sistema web de ponto de venda e sinalização digital desenvolvido para gerenciar filas e atendimento em barracas de eventos de alta demanda. O projeto foi arquitetado especificamente para rodar como um servidor local de borda (*Edge Server*) em hardware com recursos limitados (TV Box ARM com 1GB de RAM).

## 🚀 Arquitetura e Solução de Embarcados

Em eventos com grande público, a dependência de internet externa ou roteadores distantes gera gargalos no atendimento. Esta solução transforma uma TV Box genérica em um nó autônomo de rede e processamento:

* **Backend Ultra-Leve:** Desenvolvido em Python com Flask e SQLite puro, consumindo menos de 40MB de RAM e operando sem necessidade de ORMs ou servidores de banco de dados externos.
* **Sinalização Digital (Kiosk Mode):** A saída HDMI da TV Box renderiza um painel assíncrono que consulta a API local via AJAX, eliminando recarregamentos de tela e poupando a CPU ARMv7.
* **Conectividade Local (Zero-Config):** A API descobre automaticamente o IP da placa na rede e gera um QR Code na tela de administração. Atendentes conectam seus smartphones à mesma rede e acessam os painéis de Caixa e Cozinha instantaneamente.

## 🛠️ Hardware Alvo

* **Dispositivo:** TV Box MXQ Pro 4G / Rockchip RK322x
* **Arquitetura:** ARM Cortex-A7 Quad-Core 32-bit
* **Memória:** 1GB RAM / 8GB eMMC
* **Sistema Operacional:** Linux Armbian (Debian/Ubuntu Server)

## 📋 Funcionalidades

1. **Painel TV (`/painel`):** Display público para tela HDMI em modo Kiosk exibindo senhas prontas em destaque e pedidos em preparo.
2. **Caixa/Vendas (`/vendas`):** Interface otimizada para o smartphone do caixa com cardápio dinâmico, cálculo de total e geração de senha contínua.
3. **Cozinha/Bar (`/status`):** Painel estilo Kanban para avanço de status em tempo real (`Criado` ➔ `Em Preparo` ➔ `Finalizado` ➔ `Entregue`).
4. **Admin (`/admin`):** CRUD completo de itens do cardápio e usuários operadores, além de gerador automático de QR Code para conexão de dispositivos.

## ⚙️ Como Executar na Placa

```bash
# 1. Clonar o repositório e acessar a pasta
git clone [https://github.com/SEU_USUARIO/barraca-embarcada.git](https://github.com/SEU_USUARIO/barraca-embarcada.git)
cd barraca-embarcada

# 2. Criar ambiente virtual e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 3. Iniciar o servidor de borda
python3 run.py
```
