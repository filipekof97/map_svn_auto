
import os
import subprocess
import configparser

RAIZ_TRUNK = ""
RAIZ_BRANCHES = ""
PATH_PARAMETROS = "C:\\arsenal_5\\parametros.ini"

if not os.path.exists(PATH_PARAMETROS):
   print('ERRO: Não encontrado arquivo de parametrização')
   quit()

parametros = configparser.ConfigParser()
parametros.read(PATH_PARAMETROS)

#GERAL
PATH_ARSENAL            = parametros.get( 'GERAL'   , 'CaminhoArsenal'       , fallback='')
PATH_TRUNK              = parametros.get( 'GERAL'   , 'CaminhoTrunk'         , fallback='')
PATH_BRANCHES_LOCAIS    = parametros.get( 'GERAL'   , 'CaminhoBranches'      , fallback='')
TOTAL_BRANCHES_MAPEADAS = parametros.getint( 'GERAL', 'TotalBranchesMapeadas', fallback=0 )

#VARIAVEIS_MAPEAMENTO
ARQUIVO_MAPEAMENTO = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'Caminho', fallback='')
VARIAVEL_BETA      = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'Beta'   , fallback='')
VARIAVEL_OK        = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'OK'     , fallback='')
VARIAVEL_SUPEROK   = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'SuperOK', fallback='')
VARIAVEL_ULTRAOK   = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'UltraOK', fallback='')
VARIAVEL_MEGAOK    = parametros.get( 'VARIAVEIS_MAPEAMENTO', 'MegaOK' , fallback='')

#*******************************************************************************#
def retornar_todas_branches():

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
def retornar_todas_brances_local():

   local_atual = os.getcwd()

   os.chdir(PATH_BRANCHES_LOCAIS)
   todas_brances_local = list(filter(os.path.isdir, os.listdir()))

   os.chdir(local_atual)

   return todas_brances_local

#*******************************************************************************#
def baixar_branches(todas_branches_repositorio):

   print('Inicializando verificacao das branches locais...')

   todas_branches = todas_branches_repositorio[:TOTAL_BRANCHES_MAPEADAS]

   if len(todas_branches) == 0:
      print('Erro: Não foi encontrado nenhum branche no repositório.')
      return False

   todas_brances_local = retornar_todas_brances_local()

   brances_chechout = []
   for branche in todas_branches:
      if not branche in todas_brances_local:
         brances_chechout.append(branche)

   if len(brances_chechout) == 0:
      return False

   local_atual = os.getcwd()

   os.chdir(PATH_BRANCHES_LOCAIS)

   for branche in brances_chechout:
      print('Iniciando checkout da branche: ' + branche)
      subprocess.run(['svn', 'checkout', RAIZ_BRANCHES + '/' + branche], stdout=subprocess.PIPE)
      print('Finalizado checkout da branche: ' + branche)

   os.chdir(local_atual)

   return True

#*******************************************************************************#
def retornar_branches_locais_validas(todas_branches_repositorio):

   branches_locais_validas = []

   for branche in retornar_todas_brances_local():
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

   retornar_todas_brances_local = retornar_branches_locais_validas(todas_branches_repositorio)
   retornar_todas_brances_local.sort(reverse=True)

   mapeamentos = []
   nomes       = ['Beta', 'OK', 'SuperOK', 'UltraOK', 'MegaOK']
   variaveis    = [VARIAVEL_BETA, VARIAVEL_OK, VARIAVEL_SUPEROK, VARIAVEL_ULTRAOK, VARIAVEL_MEGAOK]

   for posicao in range(len(variaveis)):

      if len(variaveis[posicao]) == 0 or os.path.exists(variaveis[posicao]):
         continue

      if len(retornar_todas_brances_local) <= posicao:
         continue

      mapeamentos.append( { 'Nome': nomes[posicao],
                            'Variavel':variaveis[posicao],
                            'Branche': retornar_todas_brances_local[posicao]})

   for posicao in range(len(linhas_arquivo)):
      for mapeamento in mapeamentos:
         if 'set ' + mapeamento['Variavel'] in linhas_arquivo[ posicao ]:
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

   todas_branches_repositorio = retornar_todas_branches()

   if baixar_branches( todas_branches_repositorio ):
      editar_arquivo_mapeamento( todas_branches_repositorio )

   print( '\nFinalizado script de atualizacao de branches')

