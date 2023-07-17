
import os
import subprocess
import configparser

RAIZ_TRUNK = ""
RAIZ_BRANCHES = ""
PATH_PARAMETROS = "c:\\parametros.ini"

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

#MAPEAMENTO
TRUNK   = parametros.get( 'MAPEAMENTO', 'Trunk'  , fallback='')
BETA    = parametros.get( 'MAPEAMENTO', 'Beta'   , fallback='')
OK      = parametros.get( 'MAPEAMENTO', 'OK'     , fallback='')
SUPEROK = parametros.get( 'MAPEAMENTO', 'SuperOK', fallback='')
ULTRAOK = parametros.get( 'MAPEAMENTO', 'UltraOK', fallback='')
MEGAOK  = parametros.get( 'MAPEAMENTO', 'MegaOK' , fallback='')
ANSENAL = parametros.get( 'MAPEAMENTO', 'Arsenal', fallback='')


#*******************************************************************************#
def retornar_todas_branches():

   processo = subprocess.run(['svn', 'ls', RAIZ_BRANCHES], stdout=subprocess.PIPE)
   todas_branches = []

   if processo.returncode != 0:
      print( 'Erro: Não foi possivel capturas as Branches' )
      return todas_branches

   todas_branches = []

   for branche in processo.stdout.decode("utf-8").split("/\r\n"):
      if len(branche) > 0:
         todas_branches.append(branche)

   return todas_branches

#*******************************************************************************#
def retornar_todas_brances_local():

   local_atual = os.getcwd()

   todas_brances_local = []
   for diretorio, subpastas, arquivos in os.walk(PATH_BRANCHES_LOCAIS):
      diretorio = diretorio[diretorio.rfind('\\')+1:]
      todas_brances_local.append(diretorio)

   os.chdir(local_atual)

   return todas_brances_local

#*******************************************************************************#
def baixar_branches():

   todas_branches = retornar_todas_branches()
   todas_branches.sort(reverse=True)
   todas_branches = todas_branches[:TOTAL_BRANCHES_MAPEADAS]

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
def realizar_mapeamentos():

   if len(ANSENAL) != 0 and not os.path.exists(ANSENAL) and len(PATH_ARSENAL) != 0:
      print('Mapeando o Arsenal: ' + PATH_ARSENAL )
      subprocess.run(['subst', ANSENAL, PATH_ARSENAL], stdout=subprocess.PIPE)

   if len(TRUNK) != 0 and not os.path.exists(TRUNK) and len(PATH_TRUNK) != 0:
      print('Mapeando a Trunk: ' + PATH_TRUNK )
      subprocess.run(['subst', TRUNK, PATH_TRUNK], stdout=subprocess.PIPE)

   retornar_todas_brances_local = retornar_branches_locais_validas()
   retornar_todas_brances_local.sort(reverse=True)

   mapeamentos = []
   nomes       = ['Beta', 'OK', 'SuperOK', 'UltraOK', 'MegaOK']
   unidades    = [BETA, OK, SUPEROK, ULTRAOK, MEGAOK]

   for posicao in range(len(unidades)):

      if len(unidades[posicao]) == 0 or os.path.exists(unidades[posicao]):
         continue

      if len(retornar_todas_brances_local) <= posicao:
         continue

      mapeamentos.append( { 'Nome': nomes[posicao],
                            'Unidade':unidades[posicao],
                            'Branche': retornar_todas_brances_local[posicao]})


   for mapeamento in mapeamentos:
      print('Mapeando a ' + mapeamento['Nome'] + ': ' + mapeamento['Unidade'])
      subprocess.run(['subst', mapeamento['Unidade'], PATH_BRANCHES_LOCAIS + '\\' + mapeamento['Branche']], stdout=subprocess.PIPE)


#*******************************************************************************#
def retornar_branches_locais_validas():

   todas_branches = retornar_todas_branches()
   branches_locais_validas = []

   for branche in retornar_todas_brances_local():
      if branche in todas_branches:
         branches_locais_validas.append(branche)

   return branches_locais_validas


#*******************************************************************************#
if __name__ == "__main__":

   if len(PATH_BRANCHES_LOCAIS) == 0 or TOTAL_BRANCHES_MAPEADAS == 0:
      print('Erro: Verificar parametrizacao do arquivo parametros.ini')
      quit()

   baixar_branches()
   realizar_mapeamentos()
