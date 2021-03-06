#Definition of inputs and outputs
#==================================
##BC=group
##PG04_WaterQualityParameters_00_OLCI_Subsetting=name
##ParameterBoolean|dontsubset|Don't subset products - In this case no shapefile is needed|false
##Input_vector=optional vector

from qgis.core import *
from PyQt4.QtCore import *
import os
import glob
import tempfile

tempfolder = 'wq_scripts_'
    

def folder_create(tempfolder):
    try:
        tempdir = glob.glob(os.path.join(tempfile.gettempdir(), tempfolder + '*'))[0]
        return tempdir
    except:
        progress.setConsoleInfo('Temporary folder:' + tempfolder + ' does not exist and will be created.')
        tempfile.mkdtemp(prefix=tempfolder)
        tempdir = glob.glob(os.path.join(tempfile.gettempdir(), tempfolder + '*'))[0]
        return tempdir

def folder_check(tempfolder):
    try:
        tempdir = glob.glob(os.path.join(tempfile.gettempdir(), tempfolder + '*'))[0]
        return False
    except IndexError:
        progress.setConsoleInfo('ERROR: Temporary folder:' + tempfolder + ' cloud not be created. Check for administration rights to create folder.')
        return True

def create_parameterfile(tempdir, dontsubset):
    with open(tempdir + "WaterQualityParametersOLCI00.txt", "w") as text_file:
        text_file.write('dontsubset='+ str(dontsubset).lower() + '\n')
        
def create_subset_parameterfile(tempdir, dontsubset, wkt_string):
    with open(tempdir + "WaterQualityParametersOLCI00.txt", "w") as text_file:
        text_file.write('wkt='+ str(wkt_string) + '\n')
        text_file.write('dontsubset='+ str(dontsubset).lower() + '\n')

def get_wkt(Input_vector):
    inlayer = processing.getObject(Input_vector)
    for feat in inlayer.getFeatures():
        geom = feat.geometry()
        wkt_string = geom.exportToWkt().upper()
        print wkt_string
    return wkt_string

def execution(tempfolder, dontsubset):
    tempdir = folder_create(tempfolder) + '/'
    if folder_check(tempfolder):
        return
    else:
        tempdir = glob.glob(os.path.join(tempfile.gettempdir(), tempfolder + '*'))[0] + '/'
        create_parameterfile(tempdir, dontsubset)

def subset_execution(tempfolder, dontsubset, Input_vector):
    tempdir = folder_create(tempfolder) + '/'
    if folder_check(tempfolder):
        return
    else:
        tempdir = glob.glob(os.path.join(tempfile.gettempdir(), tempfolder + '*'))[0] + '/'
        wkt_string = get_wkt(Input_vector)
        create_subset_parameterfile(tempdir, dontsubset, wkt_string)
        
if dontsubset == True:
    execution(tempfolder, dontsubset)
else:
    subset_execution(tempfolder, dontsubset, Input_vector)