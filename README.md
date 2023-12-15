# TrocarParaLer
#### Douglas Gonçalves
#### Ruan Lima

### Arquivos
- app.py
- dados.db
- requirements.txt
- static/
- - style.css
- - leitura.jpg
- templates/
- - layout.html
- - index.html
- - login.html
- - meus_livros.html
- - minhas_ofertas.html
- testes/
- - criacaoBd.py
- - prin.py
- venv/

#### app.py
Possui toda a lógica de backend da aplicação.
Métodos:
+ home() - Tela inicial, mostra lista de livros disponiveis se usuário estiver cadastrado;
+ login() - Loga o usuário se já tiver cadastro salvo no banco de dados;
+ logout() - Faz o logout e redireciona para a tela inicial;
+ add_usuario() - Cadastra o usuário e faz login;
+ meus_livros() - Se o usuário estiver logado, pega os livros salvos dele e renderiza na tela Meus Livros, se não estiver redireciona para a tela de login;
+ minhas_ofertas() - Se o usuário estiver logado, pega as ofertas salvas dele e renderiza na tela Minhas Ofertas, se não estiver redireciona para a tela de login;
