def get_accounts_temas():
    return{
        "cocina": ["RecetasdeCocina","Cocina_Monstruo","derechupete","mcalabajio","cocinaparados","Dulcesbocados"],

        "deportes": ["DeportesCuatro","ABCDeportes","2010MisterChip","mundodeportivo","diarioas","CaracolDeportes"],

        "informatica": ["360_Hardware","QNAPEspana","elpais_tec","xataka","genbeta","MuyComputerPRO"],

        "politica": ["PODEMOS","PSOE","populares","CiudadanosCs","InesArrimadas","sanchezcastejon"],

        "videojuegos": ["MeriStation","vidaextra","Eurogamer_es","3djuegos","Videojuegos","hobby_consolas"]
        }

def get_accounts_tests():
    return {
        "cocina": ["CocinayVino","CanalCocina","directopaladar","RecetasdeCocina","thermorecetas"],

        "deportes": ["valenciacf","marca","FOXDeportes","ESPNtenis","MarcaBasket"],

        "informatica": ["E1Am1g01nf0rma1","abc_tecnologia","HardwareSfera","computerhoy","muycomputer"],

        "politica": ["vox_es","Santi_ABASCAL","PabloIglesias","Politica_LR","LPGPolitica"],

        "videojuegos": ["JaviMoyaCom","Nintenderos","VandalOnline","GamereactorES","Ubisoft_Spain"]
        }

def get_all_accounts():
    dict={}
    for topic in get_accounts_temas().keys():
        dict[topic]=get_accounts_temas()[topic]+get_accounts_tests()[topic]
    return dict

def get_test_accounts_in_order():
    return [item for sublist in list(get_accounts_tests().values()) for item in sublist]

def get_length_one_test_theme():
    return len(get_accounts_tests()["cocina"])