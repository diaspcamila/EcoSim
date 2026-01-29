# EcoSim
Equipe: Camila, Leticia, Marina. 
Simulação 2D de ecossistema (plantas, presas e predadores) feita em **Python + Pygame**.

A simulação roda em *ticks*. Em cada tick:
- seres vivos gastam energia;
- podem morrer ou se reproduzir;
- animais se movem e podem predar;
- plantas realizam “fotossíntese” para recuperar energia.

---

## Sumário

- [Visão geral](#visão-geral)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como executar](#como-executar)
  - [Executar com menu](#executar-com-menu)
- [Controles e interação](#controles-e-interação)
- [Configuração rápida](#configuração-rápida)
- [Como funciona (alto nível)](#como-funciona-alto-nível)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Regras da simulação (detalhes do modelo)](#regras-da-simulação-detalhes-do-modelo)

---

## Visão geral

Ao executar, abre uma janela do Pygame com:

- **Menu** (`Menu.py`) com botões para escolher **bioma** e **quantidade de entidades**;
- **Mundo principal** (renderizado por `Mundo.py`) onde plantas e animais são desenhados;
- **Mini-viewport/minimapa** no canto superior esquerdo (um “mapa” com marcadores).

Biome:
- **Floresta** (`bioma = 0`)
- **Mar** (`bioma = 1`)

Assets:
- `titulo.png` é usado como imagem do título no menu.

---

## Requisitos

- **Python 3.10+** (o projeto já foi usado com Python 3.11/3.12 também)
- **pygame**

> Observação: não há arquivo `requirements.txt`/`pyproject.toml` neste repositório; por enquanto a dependência principal é o `pygame`.

---

## Instalação 

Baixe/clone o repositório e, dentro da pasta do projeto, crie um ambiente virtual e instale dependências.

Exemplo (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pygame
```

---

## Como executar

### Executar com menu 

Roda a UI com botões.

```powershell
python .\Menu.py
```

No menu:
- **INICIO**: fecha o menu e chama `Inicializacao.main(qtd_entidades, bioma)`.
- **BIOMA**: alterna FLORESTA/MAR.
- **ANIMAIS**: alterna a quantidade inicial (21/35/49).
- **SAIR**: fecha o programa.

---

## Controles e interação

- **Zoom**: clique nos botões **+** e **-** desenhados no canto do minimapa.
  - Código: `Mundo.click_zoom()` e `Mundo.desenhar_zoom()` em `Mundo.py`.
- **Fechar**: botão de fechar da janela (evento `pygame.QUIT`).

---

## Configuração rápida

Esses valores estão centralizados em `Inicializacao.py` (no início da função `main`):

- `largura, altura, escala = 1000, 800, 20`
- FPS/ticks: `clock.tick(10)`

Parâmetros de zoom ficam em `Mundo.py`:
- `self.zoom_min`, `self.zoom_max`, `self.zoom_passo`.

População inicial (em `Inicializacao.py`):
- plantas: `(qtd_entidades//7) * 4`
- presas: `(qtd_entidades//7) * 2`
- predadores: `qtd_entidades//7`

---

## Como funciona (alto nível)

- **Entrada**:
  - `Menu.py` → chama `Inicializacao.main(qtd_entidades, bioma)`.

- **Loop principal** (`Inicializacao.main()`):
  1. processa eventos (fechar janela; clique para zoom);
  2. chama `mundo.tick()` para avançar a simulação;
  3. chama `mundo.desenhar()` para renderizar;
  4. limita o FPS.

- **Tick do mundo** (`Mundo.tick()`):
  - plantas: gastam energia → podem reproduzir/morrer → fotossíntese → atualizar
  - animais: gastam energia → podem reproduzir/morrer → atualizar → mover → predar

---

## Estrutura do projeto

### Entrada / UI

- `Menu.py`
  - Menu em Pygame com botões.

- `Inicializacao.py`
  - Inicializa Pygame, cria `Mundo`, popula entidades aleatórias e executa o loop.

### Simulação

- `Mundo.py`
  - Classe `Mundo`: mantém listas de `plantas` e `animais`.
  - `tick()`: avança 1 passo da simulação.
  - `desenhar()`: desenha mundo + minimapa + botões de zoom.
  - `spawn_filho(pai)`: cria um ser do mesmo tipo e tenta deslocá-lo.

- `SerVivo.py`
  - Classe base `SerVivo`: posição, energia, regras de reprodução/morte e movimento.

- `Animal.py`
  - Classe base `Animal(SerVivo)`.

- `Planta.py`
  - `Planta(SerVivo)`: define `fotossintese()` e `desenhar()`.

- `Presa.py`
  - `Presa(Animal)`: implementa `predar()` (come plantas quando está com fome).

- `Predador.py`
  - `Predador(Animal)`: implementa `predar()` (come presas quando está com fome).

- `Energia.py`
  - Enum `EnergiaStatus` (`VIVO`, `MORTO`, `REPRODUZINDO`) e dataclass `StatusEnergia`.

### Gráficos e utilitários

- `Graficos.py`
  - Primitivas de desenho e sprites “na unha” (ex.: `setPlanta`, `setSapo`, etc.).

- `Fonte.py`
  - Fonte bitmap e helper `draw_text()`.

- `Transformacoes.py`
  - Transformações para mapear coordenadas do mundo → minimapa e util `dentro()`.

- `Clipping.py`, `Formas.py`
  - Rotinas de clipping e geometria usadas pelo render.

---

## Regras da simulação (detalhes do modelo)

### Energia, reprodução e morte

A regra é centralizada em `SerVivo.gastarEnergia()`:

- **Reprodução**: se `energia > energia_reproducao`
  - o ser perde `energia_padrao` e retorna status `REPRODUZINDO`.
  - o `Mundo` cria um filho com `type(pai)(pai.x, pai.y)`.

- **Vivo**: se `energia > 0`
  - perde `custo_energetico` por tick.

- **Morte**: se `energia <= 0`
  - retorna status `MORTO` e o `Mundo` remove o ser da lista.

### Movimento e colisão

- Movimento é em grade (passo fixo): `SerVivo.escala`.
- A cada tick, o ser tenta mover para uma das direções `N/S/E/W` em ordem aleatória.
- Restrições:
  - não pode sair dos limites do mundo;
  - não pode ocupar uma célula já ocupada por planta/animal.

### Plantas: fotossíntese

Em `Planta.fotossintese(plantas, animais)`:
- conta plantas vizinhas;
- se tiver muitos vizinhos, ganha menos/nenhuma energia;
- ganha mais energia se houver muitos animais no mundo.

### Presas e predadores: predação

- `Presa.predar()`:
  - se `energia < energia_fome`, procura uma planta adjacente e come.

- `Predador.predar()`:
  - se `energia < energia_fome`, procura uma presa adjacente e come.

---

