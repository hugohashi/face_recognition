
# Sistemas avançados de visão industrial - Trabalho Prático 1, Grupo 3


## Tabela de conteúdos

1. [Objetivos do trabalho](#objectives)

2. [Bibliotecas necessarias](#libraries)

3. [Funcionamento](#functioning)

4. [Como rodar o script](#run)


<a name="objectives"></a>
## 1. Objetivos do trabalho:

1 - O sistema deverá detetar caras sempre que alguém chegar perto. 

2 - Para além de detetar as caras o sistema deverá ser capaz de reconhecer as várias pessoas da turma (ou do grupo). 
Para isso pode funcionar com uma base de dados pré-gravada. 
Deve também ser possível iniciar o sistema sem ter ainda informação sobre nenhuma pessoa.

3 - Deve ser possível visualizar a base de dados das pessoas em tempo real.

4 - O sistema deverá identificar as pessoas que reconhece, e perguntar sobre as pessoas desconhecidas.

5 - O sistema deve cumprimentar as pessoas que já conhece, dizendo "Hello ". 
Poderá utilizar uma ferramenta de \emph{text to speech}, por exemplo https://pypi.org/project/pyttsx3/

6 - O sistema deverá fazer o seguimento das pessoas na sala e manter a identificação em cima das pessoas que reconheceu anteriormente, 
ainda que atualmente não seja possível reconhecê-las.


<a name="libraries"></a>
## 2. Bibliotecas necessarias

opencv

copy

random

math

threading

pyttsx3

time

os

glob

face_recognition

numpy

speech_recognition

sounddevice


<a name="functioning"></a>
## 3. Funcionamento

O programa liga a camera e se não reconhece a pessoa no frame ele pergunta-lhe o nome;

liga o mic e transcreve a fala para uma string com o nome da pessoa;

Após associar salvar a string, o sistema tira uma foto e salva com aquele nome na base de dados.

Se o sistema já reconhece a pessoa no frame ele cumprimenta-a.


<a name="run"></a>
## 4. Como rodar o script

No terminal clonar o repositorio

 ```
git clone https://github.com/ritapm18/Trab1_G3
 ```

Entrar na pasta em que salvou

 ```
cd path/to/folder
 ```

Rodar o main script

 ```
python3 main.py
 ```
