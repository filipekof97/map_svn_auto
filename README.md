# map_svn_auto
Para facilitar a virada de vers�o, o script `map_svn_auto` tem como objetivo automatizar o checkout das braches e realizar a altera��o no arquivo de mapeamento virtual das unidades, conforme parametrizado no cabe�alho do script.


## Para utilizar o script map_svn_auto.py � necess�rio seguir alguns passos:

1) Instalar o [Python](https://www.python.org/downloads/) acima da vers�o 3.10, lembrando de habilitar a inclus�o do caminho na variavel de ambiente PATH do Windows.

<img src="img\python_install.png" width="300" height="200"/>

2) E tamb�m dever� ser instalado\atualizado o [TortoisSVN](https://tortoisesvn.net/downloads.html), verificando se ativou o modo de linha de comando, que geralmente est� desabilitado.

<img src="img\tortois_svn.png" width="300" height="200"/>

3) (Apenas para SG Sistemas) Renomear o arquivo svn.cmd para _svn.cmd, caso exista em C:\arsenal_5\tools, para que n�o existam conflitos nos comandos.

4) Preencher o valor das constantes no cabe�alho do arquivo map_svn_auto.py

5) Assim agora dever� apenas chamar o script em linha de comando:

```bash
python map_svn_auto.py
```
6) (Apenas para SG Sistemas) Copiar o arquivo map_svn_auto.py para dentro da pasta do arsenal e tamb�m modificar o arquivo configurexxxxx.cmd conforma exemplo a baixo.

```bash
python c:\arsenal_5\map_svn_auto.py
call c:\arsenal_5\mapeiadrivers.cmd
```
