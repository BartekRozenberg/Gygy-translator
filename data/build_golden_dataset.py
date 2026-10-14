import json
from pathlib import Path
from collections import Counter

GOLDEN_DATASET = [
    # =========================================================================
    # 1. ZDANIA Z PODRĘCZNIKA (Rozdziały 3.1 - 4.5)
    # =========================================================================
    # 3.1 Proste zdania
    {"pl": "Człowiek jest.", "gygy": "kuk lur.", "category": "podrecznik_gramatyka"},
    {"pl": "Kobieta jest.", "gygy": "kak lur.", "category": "podrecznik_gramatyka"},
    {"pl": "Mężczyzna jest.", "gygy": "kuak lur.", "category": "podrecznik_gramatyka"},
    {"pl": "Mężczyzna umiera.", "gygy": "kuak luor.", "category": "podrecznik_gramatyka"},
    {"pl": "Twórczyni jest.", "gygy": "lakak.", "category": "podrecznik_gramatyka"},
    {"pl": "Zabójczyni jest.", "gygy": "luokak.", "category": "podrecznik_gramatyka"},
    {"pl": "Zabójca jest.", "gygy": "luokuak.", "category": "podrecznik_gramatyka"},
    {"pl": "Zabójca tworzy kobietę.", "gygy": "kas luokuak lar.", "category": "podrecznik_gramatyka"},
    {"pl": "Mężczyzna jest niszczony.", "gygy": "kuas luar.", "category": "podrecznik_gramatyka"},
    {"pl": "Twórca życia jest czyniony kobietą.", "gygy": "lolakuas kar.", "category": "podrecznik_gramatyka"},
    {"pl": "Matka jest kobietą.", "gygy": "lolakak kar.", "category": "podrecznik_gramatyka"},
    {"pl": "Śmierć jest antropomorfizowana.", "gygy": "luos kur.", "category": "podrecznik_gramatyka"},
    {"pl": "Matka rodzi córkę.", "gygy": "kokas kuokak lolar.", "category": "podrecznik_gramatyka"},
    {"pl": "Pradziadek umiera.", "gygy": "kuokuokuokuak luor.", "category": "podrecznik_gramatyka"},

    # 3.2 Wyrażanie czasu
    {"pl": "Matka zabiła córkę.", "gygy": "kokas kuokak luoduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Niszczyciel będzie.", "gygy": "luakuak dar.", "category": "podrecznik_gramatyka"},
    {"pl": "Syn będzie kończył życie matkobójczyni.", "gygy": "kuokaluokas kokuak loduodar.", "category": "podrecznik_gramatyka"},
    {"pl": "Kobieta zacznie rodzić.", "gygy": "kak loladodar.", "category": "podrecznik_gramatyka"},
    {"pl": "Dziadek skończył umierać.", "gygy": "kuokuokuak luoduoduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Trup jest niszczony.", "gygy": "luoduakus luar.", "category": "podrecznik_gramatyka"},
    {"pl": "Córka tworzy starca.", "gygy": "duekuas kokak lar.", "category": "podrecznik_gramatyka"},

    # 3.3 - 3.4 Relacja współrzędna i podrzędna
    {"pl": "Żyjący człowiek jest biedny.", "gygy": "lop kuk puor.", "category": "podrecznik_gramatyka"},
    {"pl": "Ojciec bogato obdarował syna.", "gygy": "kokuas lolakuak pop paduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Bogaty i śmiertelny dawca będzie miał bogatą córkę i bogatego syna.", "gygy": "pop kokaci pop kokuas poci luop pakuak pudar.", "category": "podrecznik_gramatyka"},

    # 3.5 Zaimki osobowe i żywioły
    {"pl": "Zabójca jego matki zginął poprzez spalenie.", "gygy": "kiop lolakap luokuas sioluoduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Pewien człowiek się pali.", "gygy": "kuck sior.", "category": "podrecznik_gramatyka"},
    {"pl": "Utopicie nas trzech.", "gygy": "pumkias kyamok syoluodar.", "category": "podrecznik_gramatyka"},
    {"pl": "Topię się.", "gygy": "kiak syoluor.", "category": "podrecznik_gramatyka"},
    {"pl": "Pada deszcz.", "gygy": "syosiar.", "category": "podrecznik_gramatyka"},
    {"pl": "Wy zrobiliście błoto.", "gygy": "syosyas kyamok laduar.", "category": "podrecznik_gramatyka"},

    # 3.6 Konstrukcja "mówić o czymś"
    {"pl": "Uczę.", "gygy": "kiak giogypar.", "category": "podrecznik_gramatyka"},
    {"pl": "My dwoje bez ciebie mówimy o twoim zakopaniu żywcem.", "gygy": "kyap syaluos kiakiok gyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Mędrzec mówił o bogactwie dziadka i biedzie babci.", "gygy": "kuokuokuap poci kuokuokap puos giokuk gyduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Mówca będzie mówił o życiu głupca i życiu mędrca.", "gygy": "gyokup loci giokup los gykuak gydar.", "category": "podrecznik_gramatyka"},
    {"pl": "Stary głupiec zaczął głupio gadać o przyszłym bogactwie.", "gygy": "dap pos duep gyokuk gyop giadoduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Roztropna i mądra zabójczyni ogłupia syna starego mędrca.", "gygy": "duep giokuap kokuas gieci giop luokak gyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Matka gniewa się na młodego syna.", "gygy": "dep kokuas lolakak gyer.", "category": "podrecznik_gramatyka"},
    {"pl": "Ktoś gniewa się na cichego mówcę.", "gygy": "gyap gykus gyer.", "category": "podrecznik_gramatyka"},

    # 3.7 - 3.10 Okolicznik, dopełnienie dalsze i orzeczenie imienne
    {"pl": "Pewien roztropny człowiek jest na ziemi.", "gygy": "giep kuck syaner.", "category": "podrecznik_gramatyka"},
    {"pl": "Na początku było Słowo.", "gygy": "don gyk duar.", "category": "podrecznik_gramatyka"},
    {"pl": "Jestem u góry.", "gygy": "non kiak.", "category": "podrecznik_gramatyka"},
    {"pl": "Siedzę pod błotem podczas deszczu.", "gygy": "syosian kiak syosyanuer.", "category": "podrecznik_gramatyka"},
    {"pl": "Szkoła została zbudowana na wodzie.", "gygy": "syonen giopanus nular.", "category": "podrecznik_gramatyka"},
    {"pl": "W budynku lata dym.", "gygy": "nulan sioduasiak siar.", "category": "podrecznik_gramatyka"},
    {"pl": "Sadza się tworzy podczas spalania.", "gygy": "siodun sioduasys lar.", "category": "podrecznik_gramatyka"},
    {"pl": "Macie swoje bogactwo w popiele.", "gygy": "sioduan kyamop pos kyamok pur.", "category": "podrecznik_gramatyka"},
    {"pl": "On zbudował pewien budynek.", "gygy": "duan nulacs kiok nular.", "category": "podrecznik_gramatyka"},
    {"pl": "Jestem nauczany.", "gygy": "kianion giogypar.", "category": "podrecznik_gramatyka"},
    {"pl": "Uczę cię.", "gygy": "kyanion kiak giogypar.", "category": "podrecznik_gramatyka"},
    {"pl": "Ja uczę was nadczłowieka.", "gygy": "kiomonion nokus kiak giogypar.", "category": "podrecznik_gramatyka"},
    {"pl": "Daję ci moje bogactwo.", "gygy": "kyanion kiap pos kiak par.", "category": "podrecznik_gramatyka"},
    {"pl": "Każdy uczeń ma nauczyciela w szkole.", "gygy": "giopanun giopakus giopanukumik pur.", "category": "podrecznik_gramatyka"},
    {"pl": "Uczeń dał mamie swoje błoto.", "gygy": "lolakanion kyp syosyas giopanukuk paduar.", "category": "podrecznik_gramatyka"},
    {"pl": "My dwoje daliśmy sadzę studentowi i profesorowi na uczelni.", "gygy": "gionukuanio ci giogiopakuanio ci gionun sioduasys kiakiak paduar.", "category": "podrecznik_gramatyka"},
    {"pl": "On zawsze ma dużo bogactw.", "gygy": "dumin pomos kiok pur.", "category": "podrecznik_gramatyka"},
    {"pl": "On teraz ma dużo bogactw.", "gygy": "duln pomos kiok pur.", "category": "podrecznik_gramatyka"},
    {"pl": "On wtedy miał dużo bogactw.", "gygy": "dualn pomos kiok pur.", "category": "podrecznik_gramatyka"},
    {"pl": "Mędrzec jest szczęśliwy.", "gygy": "giokuak cor.", "category": "podrecznik_gramatyka"},
    {"pl": "My dwoje bez ciebie uszczęśliwiliśmy klauna w cyrku.", "gygy": "conun cokuas kiakiok coduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Córka bogacza płacze.", "gygy": "pokuap kokak cuasyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Matka płacze podczas pogrzebu jej syna.", "gygy": "kiop kokuap luoniosyon kuokak cuosyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Facet płacze ze szczęścia podczas pogrzebu swojej teściowej.", "gygy": "kyp piakuokap luoniosyon kuak cosyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Ucieszyłeś się podczas jego ekshumacji.", "gygy": "kiop luonyosyon kyak car.", "category": "podrecznik_gramatyka"},
    {"pl": "Długo będę straszył pewnego młodego teścia.", "gygy": "dep piakuokuacs kiak dumop cuedar.", "category": "podrecznik_gramatyka"},
    {"pl": "Zostałem ojcem.", "gygy": "kiak kokua ludoduar.", "category": "podrecznik_gramatyka"},

    # 3.11 Liczebniki i ilość
    {"pl": "Mało ludzi buduje swoje siedziby na cmentarzu.", "gygy": "luocianun kys lonulas kumuok nular.", "category": "podrecznik_gramatyka"},
    {"pl": "Nie ma klaunów wśród mędrców.", "gygy": "giokucian cokuk muer.", "category": "podrecznik_gramatyka"},
    {"pl": "Części studentów brakuje mądrości.", "gygy": "gionukumop manyon gios muer.", "category": "podrecznik_gramatyka"},
    {"pl": "Zostałeś pozbawiony reszty swojego rozsądku.", "gygy": "kyanyon kyp giep muas muer.", "category": "podrecznik_gramatyka"},
    {"pl": "On pozbawia bogactwa ich troje.", "gygy": "kiokiokionyon pos kiok muer.", "category": "podrecznik_gramatyka"},

    # 3.12 Czas i kalendarz
    {"pl": "Niedziela jest pierwszym dniem tygodnia.", "gygy": "cumfioduk fioduciap cump fiodulur.", "category": "podrecznik_gramatyka"},
    {"pl": "Poniedziałek jest pierwszym dniem tygodnia.", "gygy": "tumfioduk fioduciap cump fiodulur.", "category": "podrecznik_gramatyka"},
    {"pl": "Słońce wzeszło na niebie, czyli rozpoczął się nowy dzień, czwartek, dzień ziemi.", "gygy": "nonun fiofiok noduar ni dedup fioduk doduar ni zumfioduk ni syonup fioduk.", "category": "podrecznik_gramatyka"},

    # 3.13 Pytania i ruch
    {"pl": "Kto umarł?", "gygy": "dikuk luoduar?", "category": "podrecznik_gramatyka"},
    {"pl": "Co robiły płaczki podczas pogrzebu?", "gygy": "luoniosyon cuosyokuak diduar?", "category": "podrecznik_gramatyka"},
    {"pl": "Kiedy wzeszedł księżyc na niebie?", "gygy": "diduci nonun fyofyok noduar?", "category": "podrecznik_gramatyka"},
    {"pl": "Ono wolno szło.", "gygy": "kiok xuop xaduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Pójdę do budynku, żeby nie stać na deszczu.", "gygy": "siasyodu xuaguaxe ci nulanion kiak xadar.", "category": "podrecznik_gramatyka"},
    {"pl": "On biegnie, żeby dojść do celu.", "gygy": "ki xenion xarp xen kiok xoxar.", "category": "podrecznik_gramatyka"},
    {"pl": "Henio ruchawo wypił piwo ze studentami.", "gygy": "gionukumohyen fiotyas Henioguk xup tyaduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Skąd Litwini wracali?", "gygy": "dinyon Lituagu kekumok nyoxaduar?", "category": "podrecznik_gramatyka"},
    {"pl": "Z nocnej wracali wycieczki.", "gygy": "fyodup nyaxanyon nyoxaduar.", "category": "podrecznik_gramatyka"},

    # 3.14 Czasowniki modalne
    {"pl": "Mam nadzieję na uzyskanie możliwości pójścia do budynku.", "gygy": "kiak nulanio xalypualier.", "category": "podrecznik_gramatyka"},
    {"pl": "Możesz się cieszyć.", "gygy": "kyak coliar.", "category": "podrecznik_gramatyka"},
    {"pl": "On pozwala mu rozjaśnić całość jadalni.", "gygy": "kionion kiok ki tianup mes fior liar.", "category": "podrecznik_gramatyka"},
    {"pl": "Musisz zniszczyć swoje bogactwo.", "gygy": "tip pos kyak lualyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Trzeba żyć.", "gygy": "lolyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Chce się żyć.", "gygy": "lolior.", "category": "podrecznik_gramatyka"},
    {"pl": "Idź się zabij.", "gygy": "luoxen kyak xalir.", "category": "podrecznik_gramatyka"},
    {"pl": "Umrzyj.", "gygy": "kyak luolir.", "category": "podrecznik_gramatyka"},
    {"pl": "Niech Pani pije piwo.", "gygy": "fiotyas kyokak tyalir.", "category": "podrecznik_gramatyka"},

    # 3.15 Zdania złożone podrzędnie
    {"pl": "Zjadł mięso.", "gygy": "sotias tiaduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Kot śpi.", "gygy": "tiesok fyodupyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Kot śpi, po tym, gdy zjadł mięso.", "gygy": "ki sotias tiaduarp nuadun tiesok fyodupyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Kot, zjadłszy mięso, śpi.", "gygy": "tiesok ki sotias tiaduarp nuadup fyodupyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Kot, który zjadł mięso, śpi.", "gygy": "ki sotias hik tiaduarp tiesok fyodupyr.", "category": "podrecznik_gramatyka"},

    # 3.16 Porównania
    {"pl": "Tygrys jest większy od lwa.", "gygy": "mietiesok piotiesop miemiar.", "category": "podrecznik_gramatyka"},
    {"pl": "Tygrysica jest tak samo duża jak tygrys.", "gygy": "mietiesokak mietiesokuap mylur.", "category": "podrecznik_gramatyka"},

    # 3.17 Zdania złożone współrzędnie
    {"pl": "Ja jem i ty jesz.", "gygy": "kiak tiar ci kyak tiar.", "category": "podrecznik_gramatyka"},
    {"pl": "On biegnie lub skacze.", "gygy": "kiok xoxar si noxor.", "category": "podrecznik_gramatyka"},
    {"pl": "Ona śpiewa, więc tańczy.", "gygy": "kiok biagiar xi biaxur.", "category": "podrecznik_gramatyka"},
    {"pl": "Kocham cię, ale muszę odejść.", "gygy": "kyas kiak cior pi kiak nyoxalyor.", "category": "podrecznik_gramatyka"},
    {"pl": "Boisz się, więc uciekasz.", "gygy": "kyak cuer xi kyak cuexar.", "category": "podrecznik_gramatyka"},
    {"pl": "Jestem szczęśliwy, bo ty jesteś tutaj.", "gygy": "kiak cor le kyak nialur.", "category": "podrecznik_gramatyka"},
    {"pl": "Zwyciężymy lub zginiemy.", "gygy": "kiamok piodar si kiamok luodar.", "category": "podrecznik_gramatyka"},
    {"pl": "Nie mówisz prawdy, czyli kłamiesz.", "gygy": "kyak gogyguar ni kyak guogyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Wybaczę ci wtedy i tylko wtedy, gdy przeprosisz.", "gygy": "kyas kiak nioduor bi kyak guer.", "category": "podrecznik_gramatyka"},

    # 3.18 Imiesłowowy równoważnik zdania
    {"pl": "Spoglądam na zachód słońca, będąc rozradowanym.", "gygy": "fiofioduos caf kiak ter.", "category": "podrecznik_gramatyka"},
    {"pl": "Słysząc śpiew ptaków, jestem szczęśliwy.", "gygy": "siasop biagias cof kiak tor.", "category": "podrecznik_gramatyka"},
    {"pl": "Zobaczywszy konia, podszedłem do niego.", "gygy": "xosoteduaf kiak kionioxaduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Zanim się rozraduję, chcę się uspokoić.", "gygy": "cadaf kiak cielior.", "category": "podrecznik_gramatyka"},
    {"pl": "Przyszedłszy, przywitał się z nami.", "gygy": "kiamos nioxaduaf kiok ciagyduar.", "category": "podrecznik_gramatyka"},

    # 3.20 Tryb przypuszczający
    {"pl": "Mógłbyś przyjść do mnie.", "gygy": "kyak kianioxafir.", "category": "podrecznik_gramatyka"},
    {"pl": "Nie mógłbyś przyjść do mnie.", "gygy": "kyak kianioxalyguar.", "category": "podrecznik_gramatyka"},
    {"pl": "Przyjdź do mnie.", "gygy": "kyak kianioxalir.", "category": "podrecznik_gramatyka"},
    {"pl": "Proszę, przyjdź do mnie.", "gygy": "kyak kianioxalidir.", "category": "podrecznik_gramatyka"},
    {"pl": "Przyjdź do mnie!", "gygy": "kyak kianioxaligir.", "category": "podrecznik_gramatyka"},
    {"pl": "Chciałbym, żebyś przyszedł do mnie.", "gygy": "kyak kianioxalifir.", "category": "podrecznik_gramatyka"},
    {"pl": "Proszę, żebyś przyszedł do mnie.", "gygy": "kyak kianioxalidifir.", "category": "podrecznik_gramatyka"},
    {"pl": "Gdybyś przyszedł był do mnie, bylibyśmy już w kinie.", "gygy": "ki kyak kianioxafiduaduarp xue ci xategynun kiamok lur.", "category": "podrecznik_gramatyka"},
    {"pl": "Gdyby słońce nie świeciło, poleciałbym tam w nocy.", "gygy": "ki fiofiok fioguafirp xue ci fyodun kiak siaxafir.", "category": "podrecznik_gramatyka"},

    # 3.21 - 3.22 Zwrotność i przestrzenie nazw
    {"pl": "Ja myję kogoś.", "gygy": "kucs kiak tier.", "category": "podrecznik_gramatyka"},
    {"pl": "Ja jestem czysty.", "gygy": "kiak tier.", "category": "podrecznik_gramatyka"},
    {"pl": "Ja jestem myty.", "gygy": "kias tier.", "category": "podrecznik_gramatyka"},
    {"pl": "Ja myję się.", "gygy": "kiak titier.", "category": "podrecznik_gramatyka"},
    {"pl": "Nie chwaląc się, jam sam to zrobił.", "gygy": "ruals biogyliguaf kialik ruduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Lekarz wyleczył pacjenta z zapalenia płuc.", "gygy": "siasuetuzyoz huekus hokus horuduar.", "category": "podrecznik_gramatyka"},

    # 4.1 - 4.5 Imiesłowy, strona czynna/bierna/medialna, Causative
    {"pl": "Widzieliśmy zabijającego żołnierza.", "gygy": "luarup cyekus kiamok teduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Widzieliśmy zabijanego żołnierza.", "gygy": "luapyp cyekus kiamok teduar.", "category": "podrecznik_gramatyka"},
    {"pl": "Matematyk czyta książkę.", "gygy": "gysues mukuk gysuer.", "category": "podrecznik_gramatyka"},
    {"pl": "Książka jest czytana.", "gygy": "gysues gysuer.", "category": "podrecznik_gramatyka"},
    {"pl": "Matematyk czyta.", "gygy": "mukuk gysuer.", "category": "podrecznik_gramatyka"},
    {"pl": "Matematyk śpi.", "gygy": "mukuk fyodupyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Matematyk usypia dziecko.", "gygy": "kokus mukuk fyodupyr.", "category": "podrecznik_gramatyka"},
    {"pl": "Zupa gotuje się.", "gygy": "suotiasyok tiasior.", "category": "podrecznik_gramatyka"},
    {"pl": "On się myje.", "gygy": "kiok titier.", "category": "podrecznik_gramatyka"},
    {"pl": "Drzwi otwierają się łatwo.", "gygy": "buaxak hiop buar.", "category": "podrecznik_gramatyka"},
    {"pl": "Zbudowałem dom.", "gygy": "lonus kiak nuladuar.", "category": "podrecznik_gramatyka"},
    {"pl": "Ktoś inny zbudował dom na moje zlecenie.", "gygy": "lonus kiapiok nuladuar.", "category": "podrecznik_gramatyka"},
    {"pl": "Ja sam zbudowałem dom.", "gygy": "lonus kiatik nuladuar.", "category": "podrecznik_gramatyka"},
    {"pl": "Okazało się, że mimowolnie zbudowałem dom.", "gygy": "lonus kiadyek nuladuar.", "category": "podrecznik_gramatyka"},

    # =========================================================================
    # 2. MODLITWA PAŃSKA - OJCZE NASZ (Rozdział 3.15)
    # =========================================================================
    {"pl": "Ojcze nasz, któryś jest w niebie,", "gygy": "ki riononun hik lurp ci kiamop lolakuagin", "category": "modlitwa_panska"},
    {"pl": "święć się imię Twoje,", "gygy": "kyap gus bielir", "category": "modlitwa_panska"},
    {"pl": "przyjdź królestwo Twoje,", "gygy": "kyap pionuk nioxulir", "category": "modlitwa_panska"},
    {"pl": "bądź wola Twoja jako w niebie, tak i na ziemi.", "gygy": "kyap liok lulir riononurip syasenuril lir.", "category": "modlitwa_panska"},
    {"pl": "Chleba naszego powszedniego daj nam dzisiaj.", "gygy": "fiodul ci kiamonion kiamop ci fiodumip suotias kyak palir.", "category": "modlitwa_panska"},
    {"pl": "I odpuść nam nasze winy, jako i my odpuszczamy naszym winowajcom.", "gygy": "ci kiamonyon kiamop ryorumos ki kiamop ryorukumonyon kiamok nyoduor rip nyoduolir.", "category": "modlitwa_panska"},
    {"pl": "I nie wódź nas na pokuszenie,", "gygy": "ci piadynion kiamos kyak niopioxuliguar.", "category": "modlitwa_panska"},
    {"pl": "ale nas zbaw ode złego.", "gygy": "pi ryonyon kiamos kyak pierulir.", "category": "modlitwa_panska"},

    # =========================================================================
    # 3. PSALM 137 (Nad rzekami Babilonu)
    # =========================================================================
    {"pl": "Nad rzekami Babilonu,", "gygy": "Babylogup xusyonian.", "category": "psalm_137"},
    {"pl": "tam siedzieliśmy i płakaliśmy,", "gygy": "Ln kiamok nuoxua ci tetusyoduar.", "category": "psalm_137"},
    {"pl": "kiedy wspominaliśmy Syjon.", "gygy": "Ki Siongus kiamok giodiaduarp dun.", "category": "psalm_137"},
    {"pl": "Na wierzbach w jego krainie zawiesiliśmy nasze harfy.", "gygy": "Lp xynyep cuawomonen kiamop biagiaras kiamok nenuduar.", "category": "psalm_137"},
    {"pl": "Bo tam ci, którzy nas uprowadzili w niewolę, żądali od nas słów pieśni,", "gygy": "Leci ldu ci kiamonyon biagiagys ki kiamos hik pyoxaduark lyogyduar.", "category": "psalm_137"},
    {"pl": "a nasi ciemiężcy mówili: zaśpiewajcie nam jakąś pieśń Syjonu!", "gygy": "Ci ki kiamonion Siongup biagiagycs kyamok biagiagylirs ki kiamos nyopyoxaduark gyduar.", "category": "psalm_137"},
    {"pl": "Jakże w obcej ziemi będziemy śpiewać pieśń Pańską?", "gygy": "Diri ci kuep syan piokyp biagiagys kiamok biagiagydar?", "category": "psalm_137"},
    {"pl": "Jeśli zapomnę o tobie, Jeruzalem, niech uschnie moja prawica!", "gygy": "Ki Lierusalegus kiak giodyor xuen kiap ferotunion hodyos palir.", "category": "psalm_137"},
    {"pl": "Niech mój język przyschnie do podniebienia,", "gygy": "Kiap notiatunion kiap tuotuk vielir", "category": "psalm_137"},
    {"pl": "jeśli nie będę pamiętał o tobie,", "gygy": "Ki kyas kiak giodioguadar xuen", "category": "psalm_137"},
    {"pl": "jeśli nie postawię Jeruzalem ponad największą moją radość.", "gygy": "Ki kiap cop cumn Lierusalegus kiak diopaguadar xuen.", "category": "psalm_137"},
    {"pl": "Przypomnij, Panie, synom Edomu dzień Jeruzalem,", "gygy": "Lierusalegup fiodu ci Ledogup komonion ls piokygik giodiolir.", "category": "psalm_137"},
    {"pl": "kiedy mówili: zburzcie, zburzcie aż do fundamentów!", "gygy": "Kiki nuebahaganion kyamok lualualirs kiomok gyduar dun.", "category": "psalm_137"},
    {"pl": "Córo Babilonu, niszczycielko,", "gygy": "Babylogup ci puocuap kokagik.", "category": "psalm_137"},
    {"pl": "szczęśliwy, kto ci odpłaci za zło, które nam wyrządziłaś!", "gygy": "Ki kyanion ki kiamonion kyak riepaduarp ci kyap riepas hik riepadarp kuk cobiolur.", "category": "psalm_137"},
    {"pl": "Szczęśliwy, kto schwyci i rozbije o skałę twoje dzieci!", "gygy": "Ki hik hapuarp ci ki juasunion kyap myekomos hik hazieluodarp kuk ciobiolur.", "category": "psalm_137"},

    # =========================================================================
    # 4. PROLOG EWANGELII ŚW. JANA (J 1, 1-14 - Rozdział 6.1)
    # =========================================================================
    {"pl": "Na początku było Słowo,", "gygy": "Don gyk lur.", "category": "prolog_jana"},
    {"pl": "a Słowo było u Boga,", "gygy": "Biekyn gyk lur.", "category": "prolog_jana"},
    {"pl": "i Bogiem było Słowo.", "gygy": "Ci gyk biekylur.", "category": "prolog_jana"},
    {"pl": "Ono było na początku u Boga.", "gygy": "Don ci biekyn lk lur.", "category": "prolog_jana"},
    {"pl": "Wszystko przez Nie się stało,", "gygy": "Lrin mis rur.", "category": "prolog_jana"},
    {"pl": "a bez Niego nic się nie stało, co się stało.", "gygy": "Ci lmuen ki his rurp mues rur.", "category": "prolog_jana"},
    {"pl": "W Nim było życie,", "gygy": "Ln lok lur.", "category": "prolog_jana"},
    {"pl": "a życie było światłością ludzi,", "gygy": "Ci lok kup fiolur.", "category": "prolog_jana"},
    {"pl": "a światłość w ciemności świeci", "gygy": "Ci fyon fiok fior", "category": "prolog_jana"},
    {"pl": "i ciemność jej nie ogarnęła.", "gygy": "Ci fios fyok fyoguar.", "category": "prolog_jana"},
    {"pl": "Pojawił się człowiek posłany przez Boga, imieniem Jan.", "gygy": "Biekyripioniop ci Liohanegup kuk luduar.", "category": "prolog_jana"},
    {"pl": "Przyszedł on na świadectwo, aby zaświadczyć o światłości, by wszyscy uwierzyli przez niego.", "gygy": "Pi ki fios gogyparxe ci ki lrin mik berxen gogypap nioxaduar.", "category": "prolog_jana"},
    {"pl": "Nie był on światłością,", "gygy": "Lk fioluguaduar", "category": "prolog_jana"},
    {"pl": "lecz został posłany, aby zaświadczyć o światłości.", "gygy": "Pi ki fios gogyparxen ls pionioduar.", "category": "prolog_jana"},
    {"pl": "Była światłość prawdziwa, która oświeca każdego człowieka, gdy na świat przychodzi.", "gygy": "Ki senioxap kumis hik fiorp ci gop fiok luduar.", "category": "prolog_jana"},
    {"pl": "Na świecie było Słowo,", "gygy": "Sen gyk luduar", "category": "prolog_jana"},
    {"pl": "a świat stał się przez Nie,", "gygy": "Ci lrin ses luduar", "category": "prolog_jana"},
    {"pl": "lecz świat Go nie poznał.", "gygy": "Pi ls sek gieteguaduar.", "category": "prolog_jana"},
    {"pl": "Przyszło do swojej własności,", "gygy": "Lp punion xaduar", "category": "prolog_jana"},
    {"pl": "a swoi Go nie przyjęli.", "gygy": "Ci ls pupk puaguaduar.", "category": "prolog_jana"},
    {"pl": "Wszystkim tym jednak, którzy Je przyjęli,", "gygy": "Pi ki ls hik puaduarp minion", "category": "prolog_jana"},
    {"pl": "dało moc, aby się stali dziećmi Bożymi,", "gygy": "Ki biekykokus lur res lk paduar.", "category": "prolog_jana"},
    {"pl": "tym, którzy wierzą w imię Jego,", "gygy": "Ki lp gus hik berlnion.", "category": "prolog_jana"},
    {"pl": "którzy ani z krwi, ani z żądzy ciała, ani z woli męża, ale z Boga się narodzili.", "gygy": "Ki guaci tusyonyo Guaci tulionyo Guaci kualionyo Pi biekynion his loladuar.", "category": "prolog_jana"},
    {"pl": "A Słowo stało się ciałem", "gygy": "Ci gys tuluduar.", "category": "prolog_jana"},
    {"pl": "i zamieszkało wśród nas.", "gygy": "Ci kiamon lodaduar.", "category": "prolog_jana"},
    {"pl": "I oglądaliśmy Jego chwałę,", "gygy": "Ci lp bios kiamok teduar.", "category": "prolog_jana"},
    {"pl": "chwałę, jaką Jednorodzony otrzymuje od Ojca, pełen łaski i prawdy.", "gygy": "Ki lolakuanyon his gop ci biepep mep cumlolapypk puar bios.", "category": "prolog_jana"},

    # =========================================================================
    # 5. HYMN TE DEUM (Ciebie, Boga, wysławiamy - Rozdział 6.2)
    # =========================================================================
    {"pl": "Ciebie, Boga, wysławiamy,", "gygy": "Biekykyas kiamok biebiogyr.", "category": "te_deum"},
    {"pl": "Ciebie, Pana, wyznajemy.", "gygy": "Piokykyas kiamok bebygyr.", "category": "te_deum"},
    {"pl": "Ciebie, Przedwiecznego Ojca, cała ziemia czci.", "gygy": "Dumip kuokuakyas mip sesyak bypar.", "category": "te_deum"},
    {"pl": "Tobie wszyscy aniołowie, Tobie niebiosa i wszystkie moce, Tobie cherubini i serafini nieustannym głosem wołają:", "gygy": "Kyanion mip nosiakymok Kyanion nosiap ci misep rekymok Kyanion banosiakymo ci sionosiakymok Duomuep giap giagyr:", "category": "te_deum"},
    {"pl": "Święty, Święty, Święty, Pan Bóg Zastępów.", "gygy": "Biebiebie pioky ci momop biekygin.", "category": "te_deum"},
    {"pl": "Pełne są niebiosa i ziemia majestatu chwały Twojej.", "gygy": "Nosia ci sesyak kyap biop piobymer.", "category": "te_deum"},
    {"pl": "Ciebie chwalebny chór Apostołów, Ciebie proroków chwalebna liczba, Ciebie męczenników świetlane wojsko wysławia.", "gygy": "Kyas biop pioniopykuamop giaciak Kyas biebiop datekuamop mociak Kyas fiofiotp gogykuamop cyekuciak biebiogyr.", "category": "te_deum"},
    {"pl": "Ciebie po całym okręgu ziemi święty Kościół wyznaje:", "gygy": "Sesyan kyas biep beciak bebygyr.", "category": "te_deum"},
    {"pl": "Ojca niezmierzonego majestatu,", "gygy": "Miemiep piobyp kuokuas.", "category": "te_deum"},
    {"pl": "czcigodnego Twojego prawdziwego i jedynego Syna,", "gygy": "Bypapyp ci gop ci cumkyap kokuas", "category": "te_deum"},
    {"pl": "oraz Świętego Ducha Pocieszyciela.", "gygy": "Ci lioniogiaky bie sielokys.", "category": "te_deum"},
    {"pl": "Tyś Królem chwały, Chryste.", "gygy": "Kya hosypygugik biop nopiokualur.", "category": "te_deum"},
    {"pl": "Tyś Ojca przedwiecznym Synem.", "gygy": "Kyak kuokuap ci dumip kokualur.", "category": "te_deum"},
    {"pl": "Ty, mając podjąć się wyzwolenia człowieka, nie wzgardziłeś łonem Dziewicy.", "gygy": "Kyak ki kup pienion kyak liodaduarf Tiekap lolasuetup cueduaguar.", "category": "te_deum"},
    {"pl": "Ty, pokonawszy żądło śmierci, otworzyłeś wierzącym królestwo niebieskie.", "gygy": "Bekumonion nosiap pionumos Kyak ki luop buofuas piodarf baduar.", "category": "te_deum"},
    {"pl": "Ty siedzisz po prawicy Boga w chwale Ojca.", "gygy": "Biekyp fe ci kuokuap bion kyak nuoxuar.", "category": "te_deum"},
    {"pl": "Wierzymy, że przyjdziesz jako Sędzia.", "gygy": "Kyas xadap riepiokua luber.", "category": "te_deum"},
    {"pl": "Ciebie więc błagamy, wspomóż sługi Twoje, które odkupiłeś drogocenną krwią.", "gygy": "Kyas kiamok ki kyap ci ki pobyp tusyorin his kyak dbypaduarp pyokumonion kyak rioroxalirf liegyr.", "category": "te_deum"},
    {"pl": "Spraw, aby zostali policzeni ze świętymi Twoimi w chwale wiecznej.", "gygy": "Dumip bion ls kyak kyap biekuhye murulir.", "category": "te_deum"},
    {"pl": "Zbaw lud swój, Panie,", "gygy": "Kyas kukes piokygik hopierulir.", "category": "te_deum"},
    {"pl": "i błogosław dziedzictwu swojemu,", "gygy": "Ci kyap bokopuas kyak riogylir", "category": "te_deum"},
    {"pl": "i rządź nimi,", "gygy": "Ci ls kyak piolir", "category": "te_deum"},
    {"pl": "i wywyższaj ich aż na wieki.", "gygy": "Ci duminion ls kyas nonioxalir.", "category": "te_deum"},
    {"pl": "Po wszystkie dni błogosławimy Ciebie", "gygy": "Cumip fiodumon kyas kiamok riogyr.", "category": "te_deum"},
    {"pl": "i wysławiamy imię Twoje na wieki i na wieki wieków.", "gygy": "Ci dumidunion kyap gus kiamok biebiogyr Ci dumidup dumidun.", "category": "te_deum"},
    {"pl": "Racz, Panie, dnia tego zachować nas bez grzechu.", "gygy": "Fiodudal ci ryorumuen kiamos piokygik buliliolir", "category": "te_deum"},
    {"pl": "Zmiłuj się nad nami, Panie,", "gygy": "Kiamos piokygik puociolir.", "category": "te_deum"},
    {"pl": "zmiłuj się nad nami.", "gygy": "Kiamos puociolir.", "category": "te_deum"},
    {"pl": "Niech miłosierdzie Twoje, Panie, okaże się nad nami,", "gygy": "Kiamonon piokygikyap puociok lulir", "category": "te_deum"},
    {"pl": "tak jak w Tobie nadzieję pokładaliśmy.", "gygy": "Leni kyan kiamok lieduar.", "category": "te_deum"},
    {"pl": "W Tobie, Panie, zaufałem,", "gygy": "Piokygikyan kiak lieduar.", "category": "te_deum"},
    {"pl": "nie będę zawstydzony na wieki.", "gygy": "Dumin kiak ryabyoguar.", "category": "te_deum"},
    {"pl": "Amen.", "gygy": "Lamen.", "category": "te_deum"},

    # =========================================================================
    # 6. KSIĘGA IZAJASZA (Iz 11, 1-5)
    # =========================================================================
    {"pl": "I wyrośnie różdżka z pnia Jessego,", "gygy": "Ci liesegup nuesuonyon refuak nyoxadar.", "category": "izajasz_11"},
    {"pl": "a z jego korzeni wypuści pęd kwiat.", "gygy": "Ci lp nuesuonyon biasuok noxadar.", "category": "izajasz_11"},
    {"pl": "I spocznie na nim Duch Pański:", "gygy": "Ci lnon piokyp sielokyk ciaxuadar:", "category": "izajasz_11"},
    {"pl": "Duch mądrości i rozumu,", "gygy": "Giop ci gygiop sielokyk", "category": "izajasz_11"},
    {"pl": "Duch rady i męstwa,", "gygy": "Giegyp ci rorep sielokyk", "category": "izajasz_11"},
    {"pl": "Duch wiedzy i pobożności.", "gygy": "Giogyp ci riorep sielokyk.", "category": "izajasz_11"},
    {"pl": "I napełni go Duch bojaźni Pańskiej.", "gygy": "Ci ls piokyp recuep sielokyk dmedar.", "category": "izajasz_11"},
    {"pl": "Nie będzie sądził według widoku oczu", "gygy": "Tetup terin riepioguadar", "category": "izajasz_11"},
    {"pl": "ani rozstrzygał według słuchu uszu.", "gygy": "Ci totup torin riegyguadar.", "category": "izajasz_11"},
    {"pl": "Lecz będzie sądził w sprawiedliwości biednych", "gygy": "Pi rien buokumos riepiodar.", "category": "izajasz_11"},
    {"pl": "i będzie rozstrzygał słusznie za cichymi ziemi.", "gygy": "Ci sesyap hiobykumoxian myp riegydar.", "category": "izajasz_11"},
    {"pl": "I uderzy ziemię rózgą swoich ust,", "gygy": "Ci lp gybuatup refuaran sesyas rehadar.", "category": "izajasz_11"},
    {"pl": "a tchnieniem swoich warg uśmierci bezbożnego.", "gygy": "Ci lp gybatup sieloran riobieguakus reluodar.", "category": "izajasz_11"},
    {"pl": "I będzie sprawiedliwość pasem jego bioder,", "gygy": "Ci riek lp lolatup fafuatio ludar.", "category": "izajasz_11"},
    {"pl": "a wierność przepaską jego lędźwi.", "gygy": "Ci bek lp tyedyatup fuafatio ludar.", "category": "izajasz_11"},
]


def save_golden_dataset():
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    golden_path = output_dir / "test_golden.jsonl"
    instruction_text = (
        "Przetłumacz poniższe zdanie z języka polskiego na język gygy, "
        "stosując szyk AOSPV oraz zasady gramatyczne gygy."
    )

    with open(golden_path, "w", encoding="utf-8") as f:
        for entry in GOLDEN_DATASET:
            record = {
                "pl": entry["pl"],
                "gygy": entry["gygy"],
                "category": entry["category"],
                "instruction": instruction_text,
                "input": entry["pl"],
                "output": entry["gygy"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    counts = Counter(item["category"] for item in GOLDEN_DATASET)
    print(f"[✓] Zapisano złoty zbiór walidacyjny ({len(GOLDEN_DATASET)} pozycji) do: {golden_path}\n")
    print("Rozkład kategorii w zbiorze walidacyjnym:")
    for cat, count in counts.items():
        print(f"  - {cat:22s}: {count} zdań")


if __name__ == "__main__":
    save_golden_dataset()