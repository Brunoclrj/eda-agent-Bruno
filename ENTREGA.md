# 📦 Guia de Entrega da Atividade

## ✅ Checklist Final

Antes de enviar, verifique:

- [ ] Aplicação funciona localmente
- [ ] Testado com dataset de fraudes (Credit Card Fraud)
- [ ] Respondidas ≥4 perguntas (≥1 com gráfico)
- [ ] Pergunta sobre conclusões respondida
- [ ] Relatório PDF gerado com 7 itens
- [ ] Link público funcionando
- [ ] Chaves de API removidas/ocultadas
- [ ] Código organizado e documentado

---

## 📝 Passos para Entrega

### 1. Testar Localmente

```bash
# Executar aplicação
streamlit run src/ui/app.py

# Testar com CSV de fraudes
# 1. Upload do arquivo
# 2. Fazer ≥4 perguntas (≥1 pedindo gráfico)
# 3. Perguntar sobre conclusões
# 4. Capturar screenshots
```

### 2. Gerar Relatório PDF

```python
# Executar gerador de relatório
python src/report/generate_pdf.py

# OU criar manualmente usando as informações coletadas
```

**O relatório DEVE conter:**

1. ✅ Framework escolhida (Claude + Streamlit)
2. ✅ Descrição da arquitetura
3. ✅ ≥4 perguntas com respostas (≥1 com gráfico)
4. ✅ 1 pergunta sobre conclusões + resposta
5. ✅ Códigos-fonte ou indicação de onde estão
6. ✅ Link público para acessar o agente
7. ✅ Evidências de ocultação de chaves

### 3. Deploy (Link Público)

#### Opção A: Streamlit Community Cloud (Recomendado)

```bash
# 1. Criar repositório GitHub
git init
git add .
git commit -m "Agente EDA - Atividade Extra"
git remote add origin https://github.com/seu-usuario/eda-agent.git
git push -u origin main

# 2. Acessar https://streamlit.io/cloud
# 3. New app → Connect GitHub → Selecionar repositório
# 4. Main file: src/ui/app.py
# 5. Advanced settings → Secrets:
#    ANTHROPIC_API_KEY = "sua_chave_aqui"
# 6. Deploy!

# Link gerado será algo como:
# https://seu-usuario-eda-agent-srcuiapp-xxxxx.streamlit.app
```

#### Opção B: Docker + Render/Railway

```bash
# Build e push para Docker Hub
docker build -t seu-usuario/eda-agent .
docker push seu-usuario/eda-agent

# Deploy no Render.com ou Railway.app
# Configurar variável de ambiente: ANTHROPIC_API_KEY
```

### 4. Preparar Arquivos para Envio

```bash
# Criar diretório de entrega
mkdir entrega
cd entrega

# Copiar relatório PDF
cp "../Agentes Autônomos – Relatório da Atividade Extra.pdf" .

# Copiar código-fonte (SEM .env com chaves reais!)
cp -r ../src .
cp ../requirements.txt .
cp ../README.md .
cp ../QUICKSTART.md .
cp ../.env.example .
cp ../Dockerfile .
cp ../docker-compose.yml .

# Criar arquivo com link público
echo "https://seu-app.streamlit.app" > link_publico.txt

# Compactar tudo
zip -r "entrega_agentes_autonomos_$(date +%Y%m%d).zip" .
```

### 5. Verificar Segurança

```bash
# CRÍTICO: Verificar que não há chaves expostas
grep -r "sk-ant-" .  # Não deve retornar nada
grep -r "ANTHROPIC_API_KEY.*=.*sk" .  # Não deve retornar nada

# Verificar .gitignore
cat .gitignore | grep .env  # Deve conter .env
```

### 6. Enviar E-mail

**Para:** challenges@i2a2.academy  
**Cópia:** seu-email@dominio.com  
**Assunto:** Agentes Autônomos – Atividade Extra  

**Anexos:**
1. ✅ `Agentes Autônomos – Relatório da Atividade Extra.pdf`
2. ✅ `entrega_agentes_autonomos_YYYYMMDD.zip` (código-fonte)
3. ✅ `link_publico.txt` (ou no corpo do e-mail)

**Corpo do e-mail (exemplo):**

```
Prezados,

Segue anexo a entrega da Atividade Obrigatória Extra - Agentes Autônomos.

Itens incluídos:
- Relatório PDF com os 7 itens obrigatórios
- Código-fonte completo (arquivo ZIP)
- Link público para teste: https://seu-app.streamlit.app

Framework utilizado: Claude Sonnet 4.5 + Streamlit

O agente está pronto para ser testado com qualquer CSV via link público.

Atenciosamente,
[Seu Nome]
```

---

## 🧪 Como o Avaliador Testará

1. Acessar link público
2. Fazer upload de CSV diferente
3. Fazer perguntas em linguagem natural
4. Verificar se gera respostas + gráficos
5. Verificar memória/conclusões
6. Analisar relatório PDF
7. Verificar código-fonte (sem chaves expostas)

**Certifique-se que tudo funciona!**

---

## ⚠️ Itens Eliminatórios

**NÃO FAZER:**
- ❌ Expor chaves de API no código/PDF
- ❌ Enviar para endereço errado
- ❌ Título de e-mail errado
- ❌ Entregar após 01/10/2025 23h59
- ❌ Cópias idênticas de outros alunos
- ❌ Link público não funcionando
- ❌ Relatório PDF sem os 7 itens

---

## 💡 Dicas Finais

1. **Teste TUDO antes de enviar**
2. **Use CSV pequeno para testes rápidos**
3. **Capture screenshots para o PDF**
4. **Documente problemas conhecidos (se houver)**
5. **Mantenha backup de tudo**
6. **Envie COM ANTECEDÊNCIA** (não deixe para última hora)

---

## 📞 Suporte

Em caso de dúvidas:
- Revisite o documento da atividade
- Consulte README.md e QUICKSTART.md
- Teste localmente antes do deploy

---

## ✅ Checklist de Envio Final

Antes de clicar "Enviar":

- [ ] E-mail para: challenges@i2a2.academy
- [ ] Cópia para: seu-email@dominio.com
- [ ] Assunto: "Agentes Autônomos – Atividade Extra"
- [ ] PDF anexado com nome correto
- [ ] ZIP com código-fonte anexado
- [ ] Link público no corpo do e-mail
- [ ] Sem chaves de API expostas
- [ ] Testado o link público
- [ ] Data/hora dentro do prazo

**BOA SORTE! 🚀**
