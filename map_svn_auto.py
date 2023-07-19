
import os
import subprocess

#Caminho dos Repositorios na rede
RAIZ_TRUNK = ""
RAIZ_BRANCHES = ""

#*******************************************************************************#
PATH_BRANCHES_LOCAIS    = "D:\\ProdutosSG\\branches_nova"
ARQUIVO_MAPEAMENTO      = "C:\\arsenal_5\\mapeiadrivers.cmd"
TOTAL_BRANCHES_MAPEADAS = 4 #Quantidade minima de Branches para checkout

#VARIAVEIS DE AMBIENTE PARA MAPEAMENTO (Se nao quiser alguma eh so preencher com "")
VARIAVEL_BETA      = "A_BRAN_BT"
VARIAVEL_OK        = "A_BRAN_OK"
VARIAVEL_SUPEROK   = "A_SUPER_OK"
VARIAVEL_ULTRAOK   = "A_ULTRA"
VARIAVEL_MEGAOK    = "A_MEGA"


#*******************************************************************************#
def retornar_todas_branches_repositorio():

   print( 'Pegando todas as branches contidas no repositorio...')

   processo = subprocess.run(['svn', 'ls', RAIZ_BRANCHES], stdout=subprocess.PIPE)
   todas_branches = []

   if processo.returncode != 0:
      print( 'Erro: Não foi possivel capturas as Branches' )
      return todas_branches

   todas_branches = []

   for branche in processo.stdout.decode("utf-8").split("/\r\n"):
      if len(branche) > 0:
         todas_branches.append(branche)

   todas_branches.sort(reverse=True)

   return todas_branches

#*******************************************************************************#
def retornar_todas_branches_local():

   local_atual = os.getcwd()

   os.chdir(PATH_BRANCHES_LOCAIS)
   todas_branches_local = list(filter(os.path.isdir, os.listdir()))

   os.chdir(local_atual)

   return todas_branches_local

#*******************************************************************************#
def baixar_branches(todas_branches_repositorio):

   print('Inicializando verificacao das branches locais...')

   todas_branches = todas_branches_repositorio[:TOTAL_BRANCHES_MAPEADAS]

   if len(todas_branches) == 0:
      print('Erro: Não foi encontrado nenhum branche no repositório.')
      return False

   todas_branches_local = retornar_todas_branches_local()

   branches_chechout = []
   for branche in todas_branches:
      if not branche in todas_branches_local:
         branches_chechout.append(branche)

   if len(branches_chechout) == 0:
      return False

   local_atual = os.getcwd()

   os.chdir(PATH_BRANCHES_LOCAIS)

   for branche in branches_chechout:
      print('Iniciando checkout da branche: ' + branche)
      subprocess.run(['svn', 'checkout', RAIZ_BRANCHES + '/' + branche], stdout=subprocess.PIPE)
      print('Finalizado checkout da branche: ' + branche)

   os.chdir(local_atual)

   return True

#*******************************************************************************#
def retornar_branches_locais_validas(todas_branches_repositorio):

   branches_locais_validas = []

   for branche in retornar_todas_branches_local():
      if branche in todas_branches_repositorio:
         branches_locais_validas.append(branche)

   return branches_locais_validas

#*******************************************************************************#
def editar_arquivo_mapeamento(todas_branches_repositorio):

   print('Iniciado edicao do arquivo de mapeamento...')

   if len(ARQUIVO_MAPEAMENTO) == 0:
      print('Nao parametrizado arquivo de mapeamento')
      return

   arquivo        = open(ARQUIVO_MAPEAMENTO, 'r', encoding="utf-8")
   linhas_arquivo = arquivo.readlines()
   arquivo.close()

   retornar_todas_branches_local = retornar_branches_locais_validas(todas_branches_repositorio)
   retornar_todas_branches_local.sort(reverse=True)

   mapeamentos  = []
   nomes        = ['Beta', 'OK', 'SuperOK', 'UltraOK', 'MegaOK']
   variaveis    = [VARIAVEL_BETA, VARIAVEL_OK, VARIAVEL_SUPEROK, VARIAVEL_ULTRAOK, VARIAVEL_MEGAOK]

   for posicao in range(len(variaveis)):

      if len(variaveis[posicao]) == 0:
         continue

      if len(retornar_todas_branches_local) <= posicao:
         continue

      mapeamentos.append( { 'Nome': nomes[posicao],
                            'Variavel':variaveis[posicao],
                            'Branche': retornar_todas_branches_local[posicao]})

   for posicao in range(len(linhas_arquivo)):
      for mapeamento in mapeamentos:
         if 'set ' + mapeamento['Variavel'] in linhas_arquivo[ posicao ] or 'SET ' + mapeamento['Variavel'] in linhas_arquivo[ posicao ]:
            linhas_arquivo[ posicao ] = 'set ' + mapeamento['Variavel'] + '=' + mapeamento['Branche'] + '\n'

   arquivo = open(ARQUIVO_MAPEAMENTO, 'w', encoding="utf-8")
   arquivo.writelines(linhas_arquivo)
   arquivo.close()

#*******************************************************************************#
if __name__ == "__main__":

   print( 'Inicializado script de atualizacao de branches\n')

   if len(PATH_BRANCHES_LOCAIS) == 0 or TOTAL_BRANCHES_MAPEADAS == 0:
      print('Erro: Verificar parametrizacao do arquivo parametros.ini')
      quit()

   todas_branches_repositorio = retornar_todas_branches_repositorio()

   if baixar_branches( todas_branches_repositorio ):
      editar_arquivo_mapeamento( todas_branches_repositorio )

   print( '\nFinalizado script de atualizacao de branches')

