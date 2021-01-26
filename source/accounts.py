from itertools import chain


def get_accounts_temas():
    return{
        "Cocina": ["RecetasdeCocina","Cocina_Monstruo","derechupete","mcalabajio","cocinaparados","Dulcesbocados","CocinayVino","CanalCocina","directopaladar","RecetasdeCocina",
                  "GastroSER","GASTROactitud","Gastronomiaycia","DGastronomia","GastronomiaCyL","VinosdeCebreros","Degusta_cyl","tierradesabor","MiquelSen","GastronomadeGa2",
                  "vlcgastronomica","andgastrotur","GastronomiaVeg","gastrosingular","HeraldoGastro","gourmeturbano","bienmesabe_","gourmetjournal","recetasen140","gdegastronomia"],

        "Deportes": ["DeportesCuatro","ABCDeportes","2010MisterChip","mundodeportivo","diarioas","CaracolDeportes","valenciacf","marca","FOXDeportes","ESPNtenis",
                     "MarcaBasket","EFEyDeporte","deportegob","rfef","Tokyo2020es","teledeporte","deportes_rtve","podium_EE","atletismoRFEA","Antena3Deportes",
                     "mundodeportivo","yosoynoticia_","sportsmadeinusa","20mDeportes","ESPNDeportes","atletismoSomos","EPdeportes","EsFutbol_Ingles","deporte_mujer","destelladeporte"],

        "Tecnología y informática": ["360_Hardware","QNAPEspana","elpais_tec","xataka","genbeta","MuyComputerPRO","computerhoy","juanklore","TecnosferaET","TecnoEspectador",
                                     "LaMMordida","Ftv_Fractal","TopesdGama","Revista_ByteTI","elpais_tec","pixeltech","jlacort","adslzone","ZoomNet_tve","ReformaGadgets",
                                     "ENTERCO","tecnocat01","Teknautas","mixx_io","jmatuk","Giz_Tab","iSenaCode","pisapapeles","MovilZona","MalditaTech"],

        "Politica": ["PODEMOS","PSOE","populares","CiudadanosCs","InesArrimadas","sanchezcastejon","vox_es","Santi_ABASCAL","PabloIglesias","Politica_LR",
                     "ierrejon","tuvozalmundo","juanpalop","AquiEuropa","begonavillacis","Tonicanto1","alvaro7carvajal","lugaricano","Albert_Rivera","IzquierdaUnida",
                     "MonederoJC","ccifuentes","MisspoliticaMg","mundo_mas_justo","edosmilaragon","amnistiaespana","OxfamIntermon","Declaracion","reformainter","proceso"],

        "Videojuegos": ["MeriStation","vidaextra","Eurogamer_es","3djuegos","Videojuegos","hobby_consolas","PSPlusES","PokemonGOespana","BRCDEvg","LVPesLoL",
                        "TwitchES","Xbox_Spain","Capcom_Es","KochMedia_es","FortniteEsp_","marcaesports","LVPes","Warcraft_ES","Minecraft_ESP","IGN_es",
                        "ESLspain","Esportmaniacos","AnaitGames","VideojuegosGAME","PlayStationES","HPTXVideojuegos","comunidadxbox","Xbox_Jugones","ttdvideojuegos","FolagoR"],

        "Otros": ["diezminutos_es","Felipez360","Conmicas","skereunpesado","SandraFerrerV","myh_tv","AnimeMangaSpain","LocaportuRopa","volvemos_","FundacionMigrar",
                  "MigrarEsCultura","LadyLauryCandy","perezreverte","TruthSeekerEs","ENM_UNAM","CanaldeHistoria","medicinisse","FacMedicinaUNAM","PSlCOLOGO","chincheto77",
                  "paulagonu","javviercalvo","lolaindigomusic","juanrallo","_Cinefilos_","FICM","edcerbero","nippon_es","culturainquieta","Rafael_delRosal"],
        }


def get_accounts_tests():
    return {
        "Cocina": ["thermorecetas","Gastro7islas","ComidasDelPeru","HortoGourmet","gastro_bloguers","gastronomia_zgz","DeMayorCocinero","chefghgonzalez","RAGinforma","gastronomia593","delascosasdelco","igastronomia"],

        "Deportes": ["ElGolazoDeGol","DAZN_ES","EFEdeportes","revistalideras","COE_es","juegosolimpicos","Mercado_Ingles","AS_amaliafra","TUDNUSA","NBAspain","deportesyahoo","mundosportextra"],

        "Tecnología y informática": ["E1Am1g01nf0rma1","abc_tecnologia","HardwareSfera","muycomputer","ExpansionTecno","muylinux","TecnonautaTV","_VanCajun","unocero","htcmania","daliadepaz","Wikichava"],

        "Politica": ["LPGPolitica","pablocasado_","MasPais_Es","euroefe","esglobal_org","IreneMontero","susanadiaz","marianorajoy","UPYD","CsCValenciana","PoliticaPMA","oxfam_es"],

        "Videojuegos": ["MeridiemGames","Nintenderos","VandalOnline","GamereactorES","Ubisoft_Spain","bethesda_ESP","AlfaBetaJuega","Videojuegos40","CallofDutyES","GeneracionXbox","EspVideojuegos","atomix",],

        "Otros": ["twin_melody","IgnatiusFarray","HistoriaDiceQue","NoSoyLaGente","eduardogavin","Trabalibros","relibertad","LaKefa","ecartelera","viajar","vickicastillo__","ProfesorSnape",]
        }

def get_all_accounts():
    dict={}
    for topic in get_accounts_temas().keys():
        dict[topic]=get_accounts_temas()[topic]+get_accounts_tests()[topic]
    return dict

def get_test_accounts_in_order():

    lista= [item for sublist in list(get_accounts_tests().values()) for item in sublist]
    return lista
def get_length_one_test_theme():
    return len(get_accounts_tests()["Cocina"])

def get_number_accounts():
    return len(list(chain(*get_all_accounts().values())))
