# Kenzie Commerce G19 API

Uma API de comércio eletrônico desenvolvida em Python Django com PostgreSQL. Um excelente exercício de algo muito comum na web e muito útil para gerar uma experiência em uma demanda do mercado de trabalho.

Todo o trabalho foi realizado em etapas bem definidas em que todos os integrantes puderam vivenciar o desenvolvimento, os testes, a integração com o git e o deploy via railway.

# Planejamento do projeto

Todas as etapas do projeto foram organizadas e divididas aos integrantes através da ferramenta Trello, que proporcionou um ambiente para instruções, definições e principalmente o acompanhamento do andamento do projeto.

As primeiras etapas do projeto foram a criação do repositório git e a definição das models, com base no pré-requisito estipulado pela Kenzie Academy em sua proposta de API para comércio eletrônico.

# Rotas da API

/api/users/ - List e Create: A criação não requer autenticação ou permissão, mas a listagem está restrita a contas de administração.<br /><br />
/api/users/<id> - Retrieve, Update e Destroy: Essa rota necessita autenticação e apenas contas de administração e object owner possuem permissão de acesso.<br /><br />
/api/cart/<id> - Retrieve e Update: Essa rota necessita autenticação e apenas contas de administração e object owner possuem permissão de acesso.<br /><br />
/api/products/ - List e Create: A criação requer autenticação e apenas para contas com atributo de vendedor ou contas de administração, porém a listagem não requer autenticação ou permissão, seja geral ou para pesquisa por nome ou categoria de produto.<br /><br />
/api/products/<id> - Retrieve, Update e Destroy: Essa rota necessita autenticação e apenas contas de administração e object owner possuem permissão de acesso.<br /><br />
/api/orders/ - List e Create: A criação requer autenticação mas não necessita de request body, devido à análise do estado da model cart do usuário autenticado, para então criar ordens de compra para cada vendedor presente nos produtos do carrinho.<br /><br />
/api/orders/<id> - Retrieve, Update e Destroy: Essa rota necessita autenticação e apenas contas de administração e de vendedor object owner possuem permissão de acesso.<br /><br />
/api/login/ - Token Obtain Pair: Rota utilizada para autenticação de usuários cadastrados com response de token e refresh.<br /><br />
/api/docs/ - Spectacular Swagger: Documentação completa do projeto através de documentação web com o uso do Swagger.<br /><br />

# Integrantes do projeto

Juan Sgarbi
Lucas Schmidt
Marcelo Henrique
Francisco Trancoso
