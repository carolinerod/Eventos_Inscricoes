# 🎟️ Sistema de Controle de Eventos e Inscrições

## 📖 Sobre o Projeto "Data & Business Intelligence Summit 2025"
Este projeto foi desenvolvido com o intuito de **facilitar a inscrição de participantes em eventos** como palestras, cursos, workshops e afins.
Este site é um **exemplo funcional** de um sistema de controle de eventos e inscrições.

A ideia é simples e direta:
- O **organizador** já possui acesso ao sistema via login pré-existente,
- Os **participantes** já estão incluídos no evento apenas ao se inscreverem via formulário, portanto **não precisam criar login**.
- Isso garante **simplicidade e rapidez** para quem quer participar e **controle total** para quem organiza.

Assim, o sistema simula perfeitamente a realidade de conferências, palestras e cursos, onde existe uma equipe organizadora separada dos inscritos, cada um com suas permissões e responsabilidades.
A ideia é oferecer uma experiência simples e eficiente:
- O participante acessa a lista de eventos e escolhe aquele que deseja participar.
- Realiza a inscrição preenchendo seus dados.
- Recebe **por e-mail** um ingresso digital que confirma sua participação e garante sua presença no evento.

Na **área do organizador**, é possível:
- Criar, editar e excluir eventos.
- Visualizar quantas pessoas se inscreveram.
- Exportar listas de inscritos.
- Controlar a capacidade máxima de cada evento.
- Vê futuros eventos.
- vê os inscritos e seus ingressos.
- Vê se o inscrito tem a necessidade de ajuda da organização como acessibilidade e afins.
Isso assegura que o controle de inscrições e a organização sejam feitos de forma prática, evitando problemas no momento do evento.

---

## 🎯 Objetivo
- Facilitar a inscrição de participantes em eventos de diferentes tipos.
- Automatizar o envio de ingressos e confirmações por e-mail.
- Dar ao organizador controle sobre a lotação e participação nos eventos.

---

## 🛠 Tecnologias Utilizadas
- **Python 3.13.3**
- **Django 5.2.4**
- **Bootstrap** 
- **Cloudinary** 
- **Supabase** 
- **Render** 
- **SMTP Gmail**

---

## ✅ Funcionalidades Principais
- **Área do Participante**
  - Listagem de eventos disponíveis.
  - Inscrição online com formulário validado.
  - Recebimento de ingresso no e-mail.
  - Link para visualizar/baixar o ingresso.

- **Área do Organizador**
  - Login e logout seguros.
  - Dashboard com métricas: total de eventos, inscrições e próximos eventos.
  - CRUD de eventos (com data, horário, local, descrição, capacidade e imagem).
  - Lista de inscritos por evento.
  - Exportação de lista de inscritos em `.csv`.

- **Funcionalidades Adicionais**
  - Upload e exibição de imagens usando Cloudinary.
  - Validação de capacidade máxima de participantes.
  - Filtros de eventos por data e local.
  - Mensagens de feedback amigáveis.
  - Deploy configurado para ambiente de produção.

---

## 📷 Fluxo do Sistema

### Participante
1. Acessa a lista de eventos.
2. Escolhe um evento e clica em **Inscrever-se**.
3. Preenche nome, e-mail e telefone.
4. Recebe o ingresso por e-mail com link para visualização/impressão.
5. Apresenta o ingresso no evento para garantir a entrada.

### Organizador
1. Faz login na **Área do Organizador**.
2. Cria ou edita eventos.
3. Consulta a lista de inscritos e controla a capacidade.
4. Exporta a lista de inscritos para conferência.

---

