
import streamlit as st
import pandas as pd
from datetime import datetime
import os

ARQUIVO_CSV = "respostas.csv"

st.title("Com Qual Discípulo Você se Parece?")

nome = st.text_input("Digite seu nome:")

perguntas = [
    {
        "pergunta": "Como você reage diante de um problema difícil?",
        "opcoes": {
            "Enfrento logo, mesmo sem pensar muito.": "Pedro",
            "Fico na minha, observando tudo e refletindo.": "João",
            "Analiso, questiono, e só sigo quando tiver certeza.": "Tomé",
            "Tento ajudar os outros, mesmo sem saber a solução.": "André"
        }
    },
    {
        "pergunta": "No seu grupo de amigos, você é...",
        "opcoes": {
            "O líder, que toma a frente e fala o que pensa.": "Pedro",
            "O que escuta, aconselha e valoriza os sentimentos.": "João",
            "O cético, que duvida primeiro e pensa depois.": "Tomé",
            "O que conecta as pessoas e age nos bastidores.": "André"
        }
    },
    {
        "pergunta": "Quando você erra, normalmente...",
        "opcoes": {
            "Se arrepende com intensidade e quer consertar logo.": "Pedro",
            "Fica mais quieto, refletindo no coração.": "João",
            "Fica remoendo o erro, querendo entender o porquê.": "Tomé",
            "Aprende com calma e segue em frente ajudando os outros.": "André"
        }
    },
    {
        "pergunta": "Sua fé é mais parecida com...",
        "opcoes": {
            "Uma chama intensa, mas que oscila.": "Pedro",
            "Uma brisa constante, profunda e amorosa.": "João",
            "Uma montanha-russa — às vezes em alta, às vezes na dúvida.": "Tomé",
            "Uma semente que cresce devagar, mas firme.": "André"
        }
    }
]

pontuacao = {"Pedro": 0, "João": 0, "Tomé": 0, "André": 0}

for i, q in enumerate(perguntas):
    resposta = st.radio(q["pergunta"], list(q["opcoes"].keys()), key=i)
    if resposta:
        pontuacao[q["opcoes"][resposta]] += 1

if st.button("Ver meu resultado") and nome:
    max_ponto = max(pontuacao.values())
    candidatos = [k for k, v in pontuacao.items() if v == max_ponto]

    if len(candidatos) == 1:
        escolhido = candidatos[0]
        mensagem_resultado = f"🎉 {nome}, você pertence ao Time {escolhido}!"
        resposta_final = escolhido
    else:
        discipulos_empate = ", ".join(candidatos)
        mensagem_resultado = f"🎯 {nome}, você tem características de mais de um discípulo: {discipulos_empate}!"
        resposta_final = discipulos_empate

    st.subheader(mensagem_resultado)

    mensagens = {
        "Pedro": {
            "versiculo": "Mateus 16:18 — 'Tu és Pedro, e sobre esta pedra edificarei a minha igreja...'",
            "mensagem": "Pedro era intenso e impulsivo, mas se tornou uma rocha na fé.",
            "video": "https://youtu.be/yTNibI4-CWA"
        },
        "João": {
            "versiculo": "1 João 4:7 — 'Amados, amemo-nos uns aos outros, porque o amor procede de Deus.'",
            "mensagem": "João era o discípulo do amor, sensível e profundo.",
            "video": "https://youtu.be/yTNibI4-CWA"
        },
        "Tomé": {
            "versiculo": "João 20:28 — 'Senhor meu, e Deus meu!'",
            "mensagem": "Tomé duvidou, mas teve uma fé profunda e sincera.",
            "video": "https://youtu.be/yTNibI4-CWA"
        },
        "André": {
            "versiculo": "João 6:9 — 'Aqui está um rapaz com cinco pães de cevada e dois peixinhos...'",
            "mensagem": "André conectava pessoas a Jesus, mesmo fora dos holofotes.",
            "video": "https://youtu.be/yTNibI4-CWA"
        },
        "Empate": {
            "versiculo": "Mateus 10:1–5 — 'Chamando seus doze discípulos...'",
            "mensagem": "Você é uma mistura rara! Escolha com qual discípulo mais se identifica hoje.",
            "video": "https://youtu.be/yTNibI4-CWA"
        }
    }

    resultado = mensagens[candidatos[0]] if len(candidatos) == 1 else mensagens["Empate"]
    st.markdown(f"📖 **Versículo:** *{resultado['versiculo']}*")
    st.markdown(f"💬 **Mensagem:** {resultado['mensagem']}")
    st.markdown(f"🎥 **Assista ao vídeo:** [Clique aqui]({resultado['video']})")

    st.warning(f"⚠️ **Atenção:** Anote aí! Você pertence ao **Time {resposta_final}**. No encontro de hoje, procure seu grupo e participe da missão!")

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = [[agora, nome, resposta_final]]
    colunas = ["Data/Hora", "Nome", "Resultado"]
    nova_linha = pd.DataFrame(linha, columns=colunas)

    if os.path.exists(ARQUIVO_CSV):
        df_antigo = pd.read_csv(ARQUIVO_CSV)
        df_novo = pd.concat([df_antigo, nova_linha], ignore_index=True)
    else:
        df_novo = nova_linha

    df_novo.to_csv(ARQUIVO_CSV, index=False)
    st.success("✅ Resposta salva com sucesso!")

if os.path.exists(ARQUIVO_CSV):
    with open(ARQUIVO_CSV, "rb") as file:
        st.download_button("📥 Baixar respostas em CSV", data=file, file_name="respostas.csv", mime="text/csv")
