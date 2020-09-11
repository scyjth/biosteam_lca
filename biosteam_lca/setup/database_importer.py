# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""

import appdirs
import tempfile
import requests
from zipfile import ZipFile
import eidl
import functools
import collections
from eight import *
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
import pandas as pd
import os
import brightway2 as bw2
from pathlib import Path
import subprocess
import warnings
from biosteam_lca.setup import strategies, importers
#try:
#   import cPickle as pickle
#except:
#   import pickle    
    
c_path=os.path.abspath(os.path.dirname(__file__))   
#%% 

class DatabaseImporter(object):
    """A quick and convenient way to import life cycle inventory databases, including 
    commercial and public databases. This object provides an convenient way to 
    download, map and import the SQLite backend to brightway2.

    Attributes
    ----------
    c_path: string
        The absolute path to the current working directory. 
    dirpath: string
        The abolute path to the database directory.

    """  
#    c_path=os.path.abspath(os.path.dirname(__file__))
    
    def __init__(self, c_path=os.path.abspath(os.path.dirname(__file__))):
        #create database directory
        self.c_path = c_path
        self.dirpath = os.path.join(self.c_path,'database')
        assert isinstance(self.dirpath, str), "`directory` must be a string"
        if not os.path.isdir(self.dirpath):
                os.makedirs(self.dirpath)
                
    def ecoinvent_db(self,download_path=None, store_download=True, **Login_credentials):
        """A method to log in to ecoinvent user account, downlad and import ecoinvent 
        database to current project based on brightway framework. 
        
        Note
        ----
            
            Ecoinvent is a commerial databse. Login credential is required before 
            acessing ecoinvent database through Biosteam_lca. 
        
       
        Parameters
        ----------
        **Login_credentials : dict
        
            * username : str 
                Ecoinvent username
                
            * password : str
                Ecoivnent password    
                
            * version : str 
                Avaiable database version
                
            * system_model : str
                System models. The ecoinvent version 3 database offers three system 
                models to choose from:
                    
                    * Cut-Off: The system model Allocation, cut-off by classification. 
                    For users new to LCI databases, ecoinvent recommends using the 
                    cut-off system model when starting to work with ecoinvent version 3.
                    https://www.ecoinvent.org/database/system-models-in-ecoinvent-3/
                    system-models-in-ecoinvent-3.html
                    
                    * APOS: The system model Allocation at the point of substitution
                    
                    * Consequential: The system model substitution, consequential

        download_path : str, optional

            Default is to download to temporary directory, '.7z file' will be removed 
            after succefful import ecoinvent database. Otherwise user can specify 
            specific download path.

        store_download : bool, optional

            Default is to store the the '.7z file'. Otherwise 'False' if no 
            download_path is provided. 

        Returns
        -------
        
        db_name : str

            The name of the ecoinvent_db.

        Notes
        -----
        
        Ecoinvent is one of the most comprehensive LCI databases based in Europe, 
        with over 14,700 LCI datasets in many areas, such as energy supply, agriculture, 
        transport, biofuels and biomaterials, bulk and specialty chemicals, 
        construction materials, wood, and waste treatment. Current latest version is 
        ecoinvent 3.5, which builds upon all previous versions of the database.
        
        LCI  contain only inputs and outputs to and from biosphere and one output to 
        technosphere (the reference product).
        
        References
        ----------

        [1]Wernet, G., Bauer, C., Steubing, B., Reinhard, J., Moreno-Ruiz, E., 
        and Weidema, B., 2016. The ecoinvent database version 3 (part I): overview 
        and methodology. The International Journal of Life Cycle Assessment, 
        [online] 21(9), pp.1218–1230.
        
        [2]Ecoinvent, Allocation cut-off by classification, accessed [Aug 12 2019], 
        available at https://www.ecoinvent.org/database/system-models-in-ecoinvent-3/
        cut-off-system-model/allocation-cut-off-by-classification.html
        
        [3]Ecoinvent, What is the structure of the data that ecoinvent offers?, 
        accessed [Aug 13 2019], avaiable at https://www.ecoinvent.org/support/faqs/
        first-time-users/what-is-the-structure-of-the-data-that-ecoinvent-offers.html
        
        """
        fp = appdirs.user_data_dir(
                appname='Biosteam_LCA',
                appauthor='ruis'
                )
        if not os.path.isdir(fp):
            os.makedirs(fp)
            print ('Creating directory {} for downloading ecoinvent database'.format(fp))
            
        with tempfile.TemporaryDirectory() as td:
            if download_path is None:
                if store_download:
                    download_path = fp
                else:
                    download_path = td 
            downloader = eidl.EcoinventDownloader(outdir=download_path, **Login_credentials)
            downloader.run()
            # #do not use downloader.extract, it may not work on Mac app 
            # downloader.extract(target_dir=download_path)
            out_path= downloader.out_path
            extract_cmd = ['7za', 'x', out_path, '-o{}'.format(download_path)]
            print ('extract cmd is : {}'.format(extract_cmd))
            try:
                self.extraction_process = subprocess.Popen(extract_cmd)
                self.extraction_process.wait() 
            except FileNotFoundError as e:
                print (e)
                pass
            db_append = downloader.file_name.replace('.7z', '')
            name = "ecoinvent" 
            db_name = name + db_append
            #ei_name = "Ecoinvent{}_{}_{}".format(*self.ecoinvent_version.split("."), self.ecoinvent_system_model) #"Ecoinvent3_3_cutoff"
            datasets_path = os.path.join(download_path, 'datasets') 
            #Use Ecospold2Importer to import datasets and exchanges
            try:
                ecospold_import = importers.SingleOutputEcospold2Importer(datasets_path, name)
            except ImportError as import_err:
                print (import_err)
            
        ecospold_import.apply_strategies()
        self.inspect(ecospold_import, db_name)
                
        print ('ecoinvent database, version {}, has been succefully imported to biosteam_lca :)'.format(db_append))
        return db_name
    
    def forwast_db(self, url="http://lca-net.com/wp-content/uploads/forwast.bw2package.zip"):  
        
        """A method for downloading and installing `forwast database`. 
        
        Parameters
        ----------

        url : string, optional
            The url from which to download the forwast database. Default is to download
            from `http://lca-net.com/wp-content/uploads/forwast.bw2package.zip`.

        Returns
        -------

        sp : obj

            The initialized database.

        Notes
        -----

        FORWAST is a open source database that developed and managed by 
        <2.-0 LCA consultants>, under the " EU’s Sixth Framework Programme – 
        European Union". Forwast database includes "material stocks, waste 
        quantities and environmental indicators based on detailed 
        environmentally extended economic and physical input-output 
        matrices (IO-tables) based on the national accounting systems and 
        other statistics." The database is also available in SimaPro 
        under "EU and DK Input Output library".
        
        Referenences
        ------------

        [1] Schmidt, J. H., Weidema, B. P., & Suh, S. (2010). EU-FORWAST project. 
        Deliverable no. 6.4. Documentation of the final model used for the 
        scenario analyses. In Tech. Rep..  
        
        """
        #exists = os.path.isfile('forwast.package.zip')
        config = Path('forwast.package.zip')
        if config.is_file():
            filename='forwast.package.zip'
            filepath=os.path.join(self.dirpath,filename)
        else: # download database from forwast website
            fp = self.dirpath
            if not os.path.isdir(fp):
                os.makedirs(fp)
            filename = "forwast.bw2package.zip"
            filepath = os.path.join(fp, filename)
            
            #Offical forwast website https://lca-net.com/projects/show/forwast/, may requires updating url from time to time
            r = requests.get(url, stream=True) 
            if r.status_code != 200:
                raise ("URL {} returns status code {}.".format(url), r.status_code)
            # use the following code instead of 'r.raw.read' to save what is being streamed to a file. 
            try:
                with open(filename, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128): #chunk = 128 * 1024
                        fd.write(chunk)
            except FileNotFoundError as err_mms:
                print (err_mms)
            filepath=os.path.realpath(filename)  
        #consider not to save to the current database folder, in case of dirpath doesn't exists error. I nthe future can be moved to database folder              
        sp=ZipFile(filepath).extractall(self.dirpath) 
        bw2.BW2Package.import_file(os.path.join(self.dirpath, "forwast.bw2package"))
    
        print ('forwast database has been successfully installed to biosteam_lca :)')
        return sp
    
                      
    def user_customized_db(self, customized_db_xlsx):
        """ 
        A method for importing user customized lci databases and datasets from an 
        Excel file.

        Parameters
        ----------

        customized_db_xlsx : str

            The filename of a .xlsx file in the local directory. For example:
            `example_user_customized_database.xlsx`

        Returns
        -------

        sp : obj

            The initialized database.

        Notes
        -----

        Database name will be matched with the 'name' field in the excel file.
        """
        filename = customized_db_xlsx
        file_path = os.path.join(self.dirpath,filename) 
        assert os.path.exists(file_path), "File Not Found"  
        #customized datasets needs to be in excel format, follow example in database folder. Use ExcelImporter to import and write datasets and exchanges
        try:
            excel_import = importers.ExcelImporter(os.path.join(self.dirpath,filename))
        except ImportError as import_err:
            print (import_err)
        excel_import.apply_strategies()
        db_name = excel_import.match_database(fields=['name'])
        self.inspect(excel_import, db_name)
        
        df = pd.read_excel(file_path, None);
        inventory_names=list(df.keys())
        warnings.warn ('User customized {}, has been succefully imported :)'.format(inventory_names))
        sp=excel_import
        return sp
                   
    def uslci_db(self):
        """ 
        A method for initializing the `us_lci` database.
        Orignal repository was downloaded from the U.S. Federal LCA Commons|Ag data 
        Commons platform. 

        Returns
        -------

        sp : obj

            The initialized database.
        
        Notes
        -----

        Biosteam_lca leverages ecospold2 importer and excel importer. The Openlca Data 
        Converter is used for converting from json format to ecospold format. 
        Pre-processed databases are saved under biosteam_lca-database directory.
        
        References
        ----------
        
        [1] USDA National Agricultural Library. (2015). LCA Commons. Ag Data Commons. 
        https://doi.org/10.15482/USDA.ADC/1173236. Accessed 2020-03-23.
            
        [2] Michael Srocka, Juliane Franze, Andreas Ciroth, January 2010. 
        Documentation openLCA format converter V2. Data Conversion from EcoSpold02 
        to ILCD. GreenDeltaTC GmbH Berlin 
        """
        db_name = 'us_lci'
        lci_import = importers.SingleOutputEcospold2Importer(os.path.join(self.dirpath,'US_lci'), db_name)
        lci_import.apply_strategies()
        
        lci_import.migrate('unusual-units')
        lci_import.migrate('default-units')
        #linking the biosphere flows by their names, units, and categories
        link_iter = functools.partial(strategies.link_iterable_by_fields, 
                            other= bw2.Database(bw2.config.biosphere),
                            kind='biosphere')
        lci_import.apply_strategy(link_iter)
        try:
            self.inspect(lci_import, db_name)
        except:
            pass
        sp = lci_import
        return sp
    
    @staticmethod
    def inspect(sp, db_name):
        """A static method to check for any unlinked exchange in a given database. 
        If found, it will be the user's decision to if or not continue writing to 
        SQLite3 backend.

        Parameters
        ----------

        sp : obj

            The initialized database.
        
        Returns
        -------

        datasets: int 

            The total number of lci datasets extracted.
        
        exchanges : int

            The total number of exchanges.

        unlinked: int

             The total number of unlinked exchanges.
        """
        
        datasets, exchanges, unlinked = sp.statistics(print_stats=False)
        if not unlinked:
            sp.write_database()
        else:
            print('There are {} unlinked exchanges, would you like to show all unlinked exchanges?'.format(sp.statistics()[2]))
            if input('[y]/[n] ') in {'y', ''}:
                 for x in sp.unlinked:
                     print(x)
            print( 'Continue to write database {}?'.format( db_name))
            if input('[y]/[n] ') in {'y', ''}:
                print ('Deleting exchanges with zero amount...')
                #delete all exchanges with zero amounts
                for ds in sp.data:
                    ds['exchanges'] = [exc for exc in ds['exchanges'] if (exc['amount'] or exc['uncertainty type'] != 0)]
                print ('Drop unlinked exchanges?')
                if input('[y]/[n] ') in {'y', ''}:
                    try:
                        sp.apply_strategies([strategies.generic.drop_unlinked])  #sp.drop_unlinked(i_am_reckless=True)
                        sp.statistics()
                        sp.write_database()
                    except:
                        print ('Dropping unlinked exchanges failed')
            else:
                raise Warning ('Stopped writing to backend SQLite3 database')      
        return datasets, exchanges


Importer = DatabaseImporter
check_path=os.getcwd()

def listDir(dir):
    fileNames=os.listdir(dir)
    for fileName in fileNames:
        print('File Name:' + fileName + '  ' + 'File Path: ' +os.path.abspath(os.path.join(dir,fileName)),sep ='\n')

if __name__ == '__main__':
    listDir(check_path)
    