
# Sistema de controlo de temperatura

Simula um sistema composto por um sensor de temperatura, um dispositivo de regulação de temperatura 
ambiente (ar condicionado) e um algoritmo de controlo, incluido num cenário configurado pelo utilizador.


## 🔧 Pré-requisitos de Instalação

Antes de executar o programa, certificar a seguinte biblioteca instalada:

- #### PyQt5:

  ```
  pip install PyQt5
  ```
## ⚙️ Instruções de Execução

Começar por correr o código principal com o seguinte comando:
```
python3 AppTempSystem.py
```

Este comando permite iniciar o sistema de controlo de temperatura.
## 📦 Funcionalidades

Após executar o código, antes de iniciar o sistema de regulação de temperatura, é pedido ao utilizador
para configurar o ambiente da divisão onde este será colocado. 

O menu de configuração, consoante o ambiente escolhido, configura a temperatura inicial do dispositivo 
de regulação de temperatura, simulando a temperatura inicial que está nessa divisão.

Após essa configuração, o sistema inicia. A cada segundo é atualizado o valor medido pelo sensor de 
temperatura e apresentado no display (**Current Temperature**), bem como o modo de operação escolhido 
(**Operation Mode**)

### Configuration Menu
#### Exterior Temperature:
- **"Cold"** (Temperatura inicial do dispositivo = 17°C)
- **"Mean"** (Temperatura inicial do dispositivo = 22°C)
- **"Hot"** (Temperatura inicial do dispositivo = 28°C)

#### Time of Day:
- **"Morning"** (Temperatura inicial do dispositivo += 2°C)
- **"Afternoon"** (Temperatura inicial do dispositivo += 0°C)
- **"Night"** (Temperatura inicial do dispositivo -= 2°C)

#### Room Division:
- **"Bedroom"** (Temperatura inicial do dispositivo += 1°C)
- **"Living Room"** (Temperatura inicial do dispositivo -= 1°C)
- **"Office"** (Temperatura inicial do dispositivo += 0°C)
- **"Amphitheater"** (Temperatura inicial do dispositivo += 2°C)

### Temperature Control System
#### DISPLAY:
- **Current Temperature** (indica o valor atual da temperatura medido pelo sensor)
- **Operation Mode** (Indica o modo escolhido pelo utilizador)
#### OPERATION MODES:
- **Choose Temperature** (Utilizador escolhe a temperatura que deseja na divisão)
- **Auto Regulate** (Utilizador escolhe regular a temperatura da divisão para a ideal (= 23°C))
- **Increase 1°C** (Utilizador escolhe aumentar 1°C à temperatura atual da divisão)
- **Decrease 1°C** (Utilizador escolhe diminuir 1°C à temperatura atual da divisão)


## 🗃️ Diagramas
### Diagrama do dispositivo de Regulação de temperatura (ar condicionado)
![Sistema de Controlo de Temperatura](https://github.com/GuilhermeCajeira/Sistema-de-Controlo-de-Temperatura/assets/94262079/575cbad2-24c4-4641-bc57-d882206e2010)

### Diagrama do sistema de controlo
![Control System](https://github.com/GuilhermeCajeira/Sistema-de-Controlo-de-Temperatura/assets/94262079/052d2671-817a-44df-bbd7-a08e75863530)


## 🛠️ Demonstração
#### Exemplo de demonstração do sistema

O utilizador escolheu:
- Temperatura exterior: Frio
- Altura do dia: Noite
- Divisão: Sala
Sendo assim, a temperatura inicial do espaço onde será colocado o dispositivo de regulação de temperatura 
é de 14°C (cenário mais frio de todos os possíveis)


```
_____________________________________
|---- Configuration Environment ----|
|-      Exterior Temperature:      -| 
|              Cold                 |
|-          Time of Day:           -| 
|              Night                |
|-         Room Division:          -| 
|           Living Room             |
|___________________________________|

Inicial System Temperature: 14.0°C
```

De seguida, o utilizador escolhe o modo "**Regulação Automática**". Sendo assim, o controlador de temperatura 
é ativado para atingir a temperatura desejada.

```
===    Mode Auto Regulate (23.0°C)   ===
=     Desired Temperature: 23.00°C     =
=     Current Temperature: 14.04°C     =
=       Temperature increasing...      =
=       Controller Error: 6.362        =

(...)

=     Desired Temperature: 23.00°C     =
=     Current Temperature: 25.87°C     =
=       Temperature decreasing...      =
=       Controller Error: -0.405       =

(...)

=     Desired Temperature: 23.00°C     =
=     Current Temperature: 23.00°C     =
=          Temperature stable.         =
=       Controller Error: -0.001       =
```

Desta forma, após escolhido o modo de operação e, por sua vez, uma nova temperatura desejada (neste caso maior 
do que a atual), podemos observar as seguintes fases:

**1**- O controlador começa a aumentar a temperatura

**2**- Quando atinge uma temperatura superior à desejada, começa a diminuir a temperatura, de forma a estabilizar 
na temperatura desejada

**3**- Estabilizou e mantém a temperatura desejada pelo utilizador
## ✒️ Autor

- [@GuilhermeCajeira](https://github.com/GuilhermeCajeira)

