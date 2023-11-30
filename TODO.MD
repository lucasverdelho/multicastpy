- O server vai ser iniciado conecando se ao RP
- O server devera estar preparado para receber pedidos de stream por parte do RP (nao dos nodes)
- Devera enviar em unicast diretamente para o RP

- CAda nodo conhece os vizinhos apenas
- Cada nodo sera capaz ed : procurar pelo RP (propagacao), ir buscar a stream multicasst a sair do RP, caso ja esteja a receber essa stream e um cliente pede deve tambem enviar para esse (outro unicast)

-O cliente vai fazer um pedido de conteudo ao Nodo mais proximo (router)
-O cliente deve estar preparado para receber 2 tipos de resposta : o conteudo (stream) ou uma resposta negativa de que nao foi encontrado o que era pedido

- O RP Devera ser capaz de iniciar uma stream multicast do conteudo unicast que esta a receber do servidor
- Para alem das funcionalidades de um nodo normal
- Devera conhecer o melhor caminho para a stream em termos de metrica (tempo de resposta, perda de pacotes, etc) e quais os nodos que tambem estao a fazer stream desse conteudo


[]: mudar o bash para iniciar cada Nodo do overlay apenas com os nodes vizinhos
[]: Servidor tem que iniciar conexao com o RP enviando uma lista de conteudo e ficar a escuta por pedidos de conteudo