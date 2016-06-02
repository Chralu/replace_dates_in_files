Replace Dates In Files
======

replace_dates_in_files met a jour les dates dans les noms de fichiers et dans leur contenu.


Installation
-----------

    $ sudo apt-get install python3-setuptools
    $ wget replace_dates_in_files.tar.gz
    $ tar xvzf replace_dates_in_files.tar.gz
    $ cd replace_dates_in_files/src/
    $ sudo easy_install3 .
  

Execution
---------   

    $ replace_dates_in_files.py <path to watch>  

    # surveille la creation de fichiers dans le dossier <path to watch>
    # Remplace les dates dans les fichiers créés dans le dossier <path to watch>. 
    # Seuls les fichiers *.xml et *.csv seront traités.
    #
    # Les dates à remplacer doivent être définies comme ceci '{DATE<daysOffset><dateFormat>}'
    #    <daysOffset> :   entier, nombre de jours à ajouter à la date courante (peut être négatif)
    #    <dateFormat> :   string, expression de format de date en style python



    # Exemples d'expressions :
    #    {DATE+2%Y%m%d}  :   date in two days, with the format 20160123
    #    {DATE%Y%m}      :   today, with the format 201601
    #    {DATE-4%Y%m}    :   four days ago, with the format 201601

