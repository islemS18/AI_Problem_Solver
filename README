PROJET - RESOLUTION DE PROBLEMES A BASE DE GRAPHES D'ETATS

Cours : Concepts d'Intelligence Artificielle

Etudiante : Islem Souissi - L2 Informatique

============================================================

STRUCTURE DU PROJET
-------------------
AIprojet/
├── Les Problemes/
│   ├── Loup_Chevre_Salade/
│   │   ├── LoupChevreSalade.xml     
│   │   └── solution1.1.dot     
│   │   └── solution1.2.dot 
|   |
│   ├── Probleme_des_seaux/
│   │   └── seaux.xml
│   │   ├── solution2.1.dot
│   │   └── solution2.2.dot
│   │   └── solution2.3.dot
│   │   └── solution2.4.dot
│   │   └── solution2.5.dot
│   │   └── solution2.6.dot
│   │   └── solution2.7.dot
│   │   └── solution2.8.dot
│   │   └── solution2.9.dot
│   │   └── solution2.10.dot
│   │   └── solution2.11.dot
│   │   └── solution2.12.dot
│   │
│   └── Probleme3/
│       ├── probleme3.xml
│       ├── solution3.1.dot
│       └── solution3.2.dot
|
├── converter/
│   └── Dot_2_xml_Conversion.py                 
│   └── reverse_converter.py  
├── automation/
│   ├── auto_pipeline.py             (pipeline automatique Talos)
│   ├── generate_problem.py          (generation via LLM)
│   └── prompt.txt                   (prompt generique LLM)
│   └── generated.xml                   
└── README.txt                       (ce fichier)
└── Rapport.pdf


PREREQUIS
---------
- Java (JDK 8+)  
- Python 3.x     
- Graphviz       (pour visualiser les DOT)
- Talos JAR      : talosExamples-0.4 1-SNAPSHOT-jar-with-dependencies.jar
  (non fourni dans le zip car c'est un fichier executable)



PARTIE 1 - EXECUTER TALOS SUR UN PROBLEME
------------------------------------------
  cd AIprojet

  java -cp talosExamples-0.4.1-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 9 -print 1 -file "Les Problemes\Loup_Chevre_Salade\LoupChevreSalade.xml"

  java -cp talosExamples-0.4.1-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 1 -file "Les Problemes\Probleme_des_seaux\seaux.xml"

  java -cp talosExamples-0.4.1-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 1 -file "Les Problemes\Probleme3\probleme3.xml"

PARTIE 2 - CONVERSION DOT <-> XML
-----------------------------------
  cd AIprojet/converter
  python converter.py
  (modifier les chemins dans le script si necessaire)

PARTIE 3 - PIPELINE AUTOMATIQUE 
----------------------------------------------
  cd AIprojet/automation
  python auto_pipeline.py
  Choisir : 1 (LCS) / 2 (Seaux) / 3 (Missionnaires)
  =>Le fichier solution.dot est genere dans le dossier automation/

PARTIE 4 - GENERATION VIA LLM
-------------------------------
  cd AIprojet/automation
  python generate_problem.py

  Le script affiche un prompt a copier dans Claude.ai 
  Collez la reponse du LLM dans le terminal, puis tapez FIN
  Le script genere automatiquement le XML, lance Talos et produit le DOT.

  LLM utilise : Claude Sonnet (Anthropic) via https://claude.ai 

VISUALISER UN FICHIER DOT
--------------------------
ligne de commande :
    dot -Tpng solution.dot -o solution.png  start solution.png

-------

Un travail réalisé par : 
  Islem Souissi
  L2 Informatique
  