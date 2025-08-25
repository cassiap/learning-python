#ajustar_img.py — Compactar imagem para um tamanho alvo (KB)



Este script nasceu de uma situação prática: minha tia precisava diminuir o tamanho de uma imagem para anexar em um site que exigia limite máximo de KB.  

A partir disso, desenvolvi um utilitário em Python que ajusta automaticamente a qualidade (e, se necessário, a resolução) até atingir o tamanho desejado.



---



## 🚀 Funcionalidade

\- Reduz imagens para um tamanho-alvo em KB (ex.: 70 KB).  

\- Suporte a JPEG e WEBP (mantém transparência em WEBP).  

\- Ajuste automático de qualidade com busca binária.  

\- Se não for suficiente, redimensiona a imagem de forma proporcional.  

\- Funciona com qualquer nome de arquivo (não precisa renomear).  



---



## 📦 Requisitos

Instale as dependências com:



```bash

pip install -r requirements.txt



