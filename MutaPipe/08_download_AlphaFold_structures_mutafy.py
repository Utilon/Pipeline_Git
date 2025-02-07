# Script to download AlphaFold predicted structures for MutaPipe input genes
# ==========================================================================================
# Script will use input gene names and get the corresponding UniProt ID from the UniProt API
# The UniProt ID is then used to construct the url to download the AlphaFold predicted structures from the AlphaFold database
# ==========================================================================================
# Set up
# ******
import requests
import pandas as pd
import argparse
import os
from datetime import datetime
import sys

# get this script's name:
script_name = os.path.basename(__file__)
# ----------------------------------------------------------------------------------------------------------------------------------
# Read in gene file for DEFAULT settings
#  read in gene_list from textfile
try:
    with open('genes.txt', 'r') as f:
        genes = f.read().split(' ')
    # remove empty entries
    if '' in genes:
        genes.remove('')
except FileNotFoundError:
    genes = ['DCTN1', 'ERBB4', 'SOD1']
    
genes = ['ACSL5', 'AGT', 'ALAD', 'ALS2', 'ALS3', 'ALS7', 'ANG', 'ANXA11', 'APEX1', 'APOE', 'AR', 'ARHGEF28', 'ARPP21', 'ATXN1', 'ATXN2', 'B4GALT6', 'BCL11B', 'BCL6', 'C21ORF2', 'C9ORF72', 'CAMTA1', 'CAV1', 'CAV2', 'CCNF', 'CCS', 'CDH13', 'CDH22', 'CFAP410', 'CHCHD10', 'CHGB', 'CHMP2B', 'CNTF', 'CNTN4', 'CNTN6', 'CRIM1', 'CRYM', 'CSNK1G3', 'CST3', 'CX3CR1', 'CYP27A1', 'CYP2D6', 'DAO', 'DCTN1', 'DIAPH3', 'DISC1', 'DNAJC7', 'DNMT3A', 'DNMT3B', 'DOC2B', 'DPP6', 'DYNC1H1', 'EFEMP1', 'ELP3', 'ENAH', 'EPHA3', 'EPHA4', 'ERBB4', 'ERLIN1', 'EWSR1', 'EPHA3', 'FEZF2', 'FGGY', 'FIG4', 'FUS', 'GARS', 'GGNBP2', 'GLE1', 'GLT8D1', 'GPX3', 'GRB14', 'GRN', 'HEXA', 'HFE', 'HNRNPA1', 'HNRNPA2B1', 'IDE', 'ITPR2', 'KBTBD3', 'KDR', 'KIAA1600', 'KIF5A', 'KIFAP3', 'LIF', 'LIPC', 'LMNB1', 'LOX', 'LUM', 'MAOB', 'MAPT', 'MATR3', 'MOBP', 'MTND2P1', 'NAIP', 'NEFH', 'NEFL', 'NEK1', 'NETO1', 'NIPA1', 'NT5C1A', 'NT5C3L', 'ODR4', 'OGG1', 'OMA1', 'OPTN', 'PARK7', 'PCP4', 'PFN1', 'PLEKHG5', 'PNPLA6', 'PON1', 'PON2', 'PON3', 'PRPH', 'PSEN1', 'PVR', 'RAMP3', 'RBMS1', 'RFTN1', 'RNASE2', 'RNF19A', 'SARM1', 'SCFD1', 'SCN7A', 'SELL', 'SEMA6A', 'SETX', 'SIGMAR1', 'SLC1A2', 'SLC39A11', 'SLC52A3', 'SMN1', 'SMN2', 'SNCG', 'SOD1', 'SOD2', 'SOX5', 'SPAST', 'SPG11', 'SPG7', 'SQSTM1', 'SS18L1', 'STMN2', 'SUSD1', 'SYNE1', 'SYT9', 'TAF15', 'TARDBP', 'TBK1', 'TFIP11', 'TIA1', 'TMEM225B', 'TNIP1', 'TRPM7', 'TUBA4A', 'TUBGCP4', 'UBQLN1', 'UBQLN2', 'UNC13A', 'VAPB', 'VCP', 'VDR', 'VEGFA', 'VPS54', 'VRK1', 'ZFP64', 'ZNF512B', 'ZNF746', 'ZNHIT3', 'ADAMTS2', 'ANKRD18B', 'APTX', 'AQP3', 'AQP7', 'ARHGEF39', 'ARID3C', 'ATOSB', 'ATP5PO', 'B4GALT1', 'BAG1', 'BSCL2', 'C21orf62', 'C22orf15', 'C5orf60', 'C9orf131', 'C9orf72', 'CA9', 'CAMK1D', 'CANX', 'CBR1', 'CBR3', 'CBY3', 'CCDC107', 'CCDC3', 'CCIN', 'CCL19', 'CCL21', 'CCL27', 'CD72', 'CFAP298', 'CHAF1B', 'CHMP5', 'CIMIP2B', 'CLDN14', 'CLIC6', 'CLTA', 'CNTFR', 'CREB3', 'CRYZL1', 'CSNK2A1', 'CYLD', 'CYLD-AS2', 'DCAF12', 'DCTN3', 'DNAI1', 'DNAJA1', 'DNAJB5', 'DNAJC28', 'DONSON', 'DOP1B', 'DYRK1A', 'EGILA', 'ENHO', 'EVA1C', 'EXOSC3', 'FAM166B', 'FAM205A', 'FAM214B', 'FAM219A', 'FAM221B', 'FANCG', 'FBXO10', 'FRMPD1', 'GALT', 'GART', 'GBA1', 'GBA2', 'GLIPR2', 'GNE', 'GRHPR', 'GRM6', 'HINT2', 'HLCS', 'HNRNPH1', 'HNRNPUL2-BSCL2', 'HRCT1', 'HUNK', 'IFNAR1', 'IFNAR2', 'IFNGR2', 'IL10RB', 'IL11RA', 'ITSN1', 'KCNE1', 'KCNE2', 'KCNJ6', 'KIF24', 'LOC106627981', 'LOC108903148', 'LOC108903149', 'LOC109504728', 'LOC117038776', 'LOC121366042', 'LOC124629354', 'LOC126807526', 'LOC126860782', 'LOC126860783', 'LTC4S', 'MAML1', 'MASP2', 'MCM10', 'MELK', 'MGAT4B', 'MIS18A', 'MORC3', 'MPP4', 'MRAP', 'MRPS6', 'MSMP', 'MYORG', 'NDUFB6', 'NFX1', 'NOL6', 'NPR2', 'NUDT2', 'OLIG1', 'OLIG2', 'OR13J1', 'OR2S2', 'PAX5', 'PAXBP1', 'PHF24', 'PIGO', 'PIGP', 'POLR1C', 'POLR1E', 'POU1F1', 'PRSS3', 'RBCK1', 'RCAN1', 'RECK', 'RGP1', 'RIGI', 'RIPPLY3', 'RMRP', 'RNASE4', 'RNF38', 'RPP25L', 'RUFY1', 'RUNX1', 'RUSC2', 'SCAF4', 'SCRT2', 'SETD4', 'SIM2', 'SIT1', 'SLC5A3', 'SMIM11', 'SMU1', 'SNHG4', 'SON', 'SPAG8', 'SPATA31F1', 'SPINK4', 'SPMIP6', 'SRXN1', 'STOML2', 'SYNJ1', 'TAF1L', 'TBC1D20', 'TCF15', 'TCP10L', 'TESK1', 'TIAM1', 'TLN1', 'TMEM215', 'TMEM237', 'TMEM50B', 'TMEM8B', 'TOMM5', 'TOPORS', 'TPM2', 'TRMT10B', 'TROAP-AS1', 'TTC3', 'UBAP1', 'UBAP2', 'UBE2R2', 'UNC13B', 'URB1', 'VPS26C', 'ZBTB5', 'ZCCHC7', 'ZFP91-CNTF', 'ZNF354C', 'ZNF879']
# set default values for arguments we want to implement
# we have to do this here if we want to print the default values in the help message
# specify other search terms and search operator:
target_directory = os.getcwd()   # set directory to create Results folder with new folders with pdb files for each gene
                                                # Default: set to current working directory (where this script is saved)
create_search_log = False      # will create a file called search_log.txt with console output if set to True,
                                            # prints to console if set to False.

# ----------------------------------------------------------------------------------------------------------------------------------

# use argparse to make it so we can pass arguments to script via terminal
# define a function to convert different inputs to booleans
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Now we create an argument parser called ap to which we can add the arguments we want to have in the terminal
ap = argparse.ArgumentParser(description="""****   This script takes a list of genes in txt. format as input and performs the following:\n
1. Gets the corresponding UniProt IDs for each gene name (in Homo Sapiens) via the UniProt API\n
2. Downloads all AlphaFold2 predicted structures for the identified UniProt IDs\n
3. Outputs a csv file called 08_AlphaFold_structures indicating download status for each structure   ***""")

ap.add_argument('-g','--genes', nargs='+', required=False, help=f'Specify genes for which to download AlphaFold predicted structures, default = {genes}; to pass a file containing all genes use -g $(cat filename)')
ap.add_argument("-l", "--log", type=str2bool, required = False, help=f'Write output to .log file in current directory if set to True, default = {str(create_search_log)}')
ap.add_argument("-t", "--target", required = False, help=f'Specify target directory, default = {target_directory}')

args = vars(ap.parse_args())

# Now, in case an argument is used via the terminal, this input has to overwrite the default option we set above
# So we update our variables whenever there is a user input via the terminal:
genes = genes if args["genes"] == None else args["genes"]
create_search_log  = create_search_log  if args["log"]   == None else args["log"]
target_directory  = target_directory if args["target"]   == None else args["target"]

# ----------------------------------------------------------------------------------------------------------------------------------
# We want to write all our Output into the Results directory
results_dir = f'{target_directory}/Results' #define path to results directory

# No need for this on Mutafy, so commented out
# # create Results folder if it doesn't already exist
# if not os.path.exists(results_dir):
#         os.makedirs(results_dir)

# ----------------------------------------------------------------------------------------------------------------------------------
#  create log file for console output:
if create_search_log == True:
    with open(f'{results_dir}/search_log_08.txt', 'w') as search_log:
        search_log.write(f'Search log for {script_name} with genes {genes}\n\n')
    sys.stdout = open(f'{results_dir}/search_log_08.txt', 'a')

# print nice title
print('===============================================================================')
print('*****    Downloading AlphaFold2 Predicted Structures for all Input Genes    *****')
print('===============================================================================\n')

# print script name to console/log file
print(f'script name: {script_name}')

# store current date and time in an object and print to console / write to log file
start_time = datetime.now()
print(f'start: {start_time}\n')

print('Input genes: ', genes, '\n')
# ----------------------------------------------------------------------------------------------------------------------------------

# ==========================================================================================
# define functions with GET requests
# **********************************

# Define a function which will retrieve data from UniProt for all input gene names
# see the following links for more info:
# this is basically an example of a search result which we might want to download:
# (click on download to choose format + settings and click generate url for API)
# https://www.uniprot.org/uniprotkb?query=organism_name%3A%22homo%20sapiens%22%20AND%20%28gene_exact%3Abraf%20OR%20gene_exact%3Abrca1%20OR%20gene_exact%3Abrca2%20OR%20gene_exact%3Abtk%20OR%20gene_exact%3Acasp10%20OR%20gene_exact%3Acasp8%29%20AND%20reviewed%3Atrue

def get_UniProt_data(genes):
    # we define the beginning of the url but don't add the genes yet
    # url = 'https://www.uniprot.org/uniprot/?query=organism:%22homo%20sapiens%22%20and%20('
    # url above doesn't work anymore (28.6.2022); use new format instead:
    # url = 'https://rest.uniprot.org/uniprotkb/search?compressed=true&fields=accession%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=tsv&query=organism_name%3A%22homo%20sapiens%22'
    # url = 'https://rest.uniprot.org/uniprotkb/search?compressed=true&fields=accession%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=xlsx&query=organism_name%3A%22homo%20sapiens%22'
    url = 'https://rest.uniprot.org/uniprotkb/search?fields=accession%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=tsv&query=organism_name%3A%22homo%20sapiens%22'
    # now we loop over all the genes to add them in our query url
    for gene in genes:
        # for the first gene we use the AND operator, for the rest the OR operator
        # so we add an if else statement like so, to catch the first gene
        if genes.index(gene)==0:
            # gene_url_string = f'gene_exact:{gene.lower()}'
            # url above doesn't work anymore (28.6.2022); use new format instead:
            gene_url_string = f'%20AND%20%28gene_exact%3A{gene.lower()}'
        else:
            # gene_url_string = f'%20or%20gene_exact:{gene.lower()}'
            # url above doesn't work anymore (28.6.2022); use new format instead:
            gene_url_string = f'%20OR%20gene_exact%3A{gene.lower()}' 
        # now we add the part of the url for this gene to the overall url
        url = url + gene_url_string
    # finally we add the other components of our search to the url:
    # search_params = ')%20and%20reviewed:yes&format=tab&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&sort=score'
    # url above doesn't work anymore (28.6.2022); use new format instead:
    search_params = '%29%20AND%20reviewed%3Atrue&size=500'
    # we combine everything to get our final url (to download data from the uniprot API)
    final_url = url + search_params
    # to download results from uniprot my url should look like this
    # 'https://www.uniprot.org/uniprot/?query=organism:%22homo%20sapiens%22%20and%20(gene_exact:nek1%20or%20gene_exact:kl%20or%20gene_exact:fus)%20and%20reviewed:yes&format=tab&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&sort=score'
    # apparently this doesn't work anymore (28.6.2022)
    # try this format instead:
    # 'https://rest.uniprot.org/uniprotkb/search?compressed=true&fields=accession%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=tsv&query=organism_name%3A%22homo%20sapiens%22%20AND%20%28gene_exact%3Abraf%20OR%20gene_exact%3Abrca1%20OR%20gene_exact%3Abrca2%20OR%20gene_exact%3Abtk%20OR%20gene_exact%3Acasp10%20OR%20gene_exact%3Acasp8%29%20AND%20reviewed%3Atrue&size=500'
    # Now we get data from the API and save it as a txt file
    response = requests.get(final_url)
    if response.status_code == 200:
        with open ('uniprot_results.txt', 'w') as file:
            file.write(response.text)
        # now we read this data in as a df
        uniprot_data = pd.read_csv('uniprot_results.txt', sep='\t')
        # and we delete the file uniprot_results.txt again
        os.remove('uniprot_results.txt')
        return uniprot_data
    else:
        # If there is no data, print status code and response
        print(response.status_code, response.text)
        print(f'No data retrieved from UniProt ID for query url {final_url}\n')
        return None # for failure


# Define a function which takes a uniprot ID as input and will download the corresponding mmCif structure from the AlphaFold Database
def get_AlphaFold_structure(uniprot_id):
    mmCIF_url = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v2.cif'
    response = requests.get(mmCIF_url)
    if response.status_code == 200:
        data = response.text
        # save the data as mmCIF file
        with open (f'{uniprot_id}_AFprediction.cif', 'w') as f:
            f.write(data)
        print(f'Download of AlphaFold structure for {uniprot_id} successful!')
        return 1 # for success
    else:
        # If there is no data, print status code and response
        print(response.status_code, response.text)
        print(f'No data retrieved for UniProt ID {uniprot_id}\n')
        return 0 # for failure

# ==========================================================================================
# we change to the results directory
os.chdir(results_dir)

# we don't need this for Mutafy as we do not download the AF predicted stuctures onto the server
# code is thus commented out
# # make a folder to store all AlphaFold structures if it doesn't already exist:
# alphafold_dir = f'{results_dir}/AlphaFold_structures' #define path
# # create AlphaFold folder if it doesn't already exist
# if not os.path.exists(alphafold_dir):
#         os.makedirs(alphafold_dir)

print('>>> getting UniProt identifiers...')
uniprot_data = get_UniProt_data(genes)
print(f'Complete!\n    Identified {len(uniprot_data)} UniProt enries for a total of {len(genes)} input genes\n')
# We define a df to output at the end of the script, containing relevant information from uniprot and a link to the AlphaFold Database entry
output_df = pd.concat([uniprot_data, pd.DataFrame(columns=['Link AlphaFold Database', 'Status'])])

# For mutafy webserver output we want to add 2 extra cols
# we want to add an extra column with the name of the input gene (not multiple gene names like in the uniprot_df Gene Names column!)
output_df['Gene'] = ''
# we also add an extra column 'Link to AF mmCIF'
output_df['Link to AF mmCIF'] = ''

# For Mutafy loop over this table and fill it in, but don't download the AF predicted structures, so
# part of the code is commented out because it's not needed!
# We loop over this table and get the Alphafold structure for each UniProt ID (stored in the column 'Entry') using the function defined above
# we will simultaneously fill in the table with additional data (the link to the entry in the AlphaFold database, and the download status)
# print('>>> getting AlphaFold2 predicted structures...')
# in order to link the gene names from the output_df to the genes in the gene list (input genes)
# we have to make sure to make the list case-insensitive, i.e. we convert all gene names to capital letters with upper()
genes_upper = [gene.upper() for gene in genes]
# # first we change to the alphafold folder so the structures get saved in the correct place
# os.chdir(alphafold_dir)
for index, row in output_df.iterrows():
    # we identify the original input gene name for this row and write it to the new
    # column "gene" because there may be one or more gene names for each
    # row in column output_df['Gene names']
    gene_name = [gene_name for gene_name in output_df.loc[index, 'Gene Names'].split(' ') if gene_name.upper() in genes_upper]
    # if there are multiple matches with our input gene names, we list all of them, otherwise we list only the first one
    # so if the length of the gene_name list is 1, we take only the first element of the list, otherwise we take the entire list
    if len(gene_name) == 1:
        gene_name = gene_name[0]
    
    # now we attach the identified gene name(s) to the output_df    
    output_df.loc[index, 'Gene'] = str(gene_name)
    uniprot_id = row.Entry
    # we also add the link to this Entry in the AlphaFold Database to the table
    output_df.loc[index, 'Link AlphaFold Database'] = f'https://www.alphafold.ebi.ac.uk/entry/{uniprot_id}'
    ## for Mutafy
    # as we don't want to download the structures and store them on the mutafy server,
    # we can skip the download bit below (commented out)
    # we just need to add info to the output df instead
    # we only need the links:
    # we add the link to the mmCif structure to the column 'Link to AF mmCIF'
    output_df.loc[index, 'Link to AF mmCIF'] = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v2.cif'
    
#     # download AlphaFold structure
#     # the function returns 1 if download was succesful and 0 if it failed (the structure is downloaded in the background)
#     # so we use this information to fill in the download status column in the output table
#     if get_AlphaFold_structure(uniprot_id) == 1:
#         output_df.loc[index, 'Status'] = 'downloaded'
#         # we add the link to the mmCif structure to the column 'Link to AF mmCIF'
#         output_df.loc[index, 'Link to AF mmCIF'] = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v2.cif'
#         # we also rename the downloaded structure file (currently in format: uniprotID_AFprediction.cif)
#         os.rename(f'{uniprot_id}_AFprediction.cif', f'{gene_name}_{uniprot_id}_AFprediction.cif')        
#     else:
#         output_df.loc[index, 'Status'] = 'failed'

# print('Complete!\n    All AlphaFold structures have been dowloaded.')
# ==========================================================================================

# modify the output for Mutafy webserver:
# gene name, uniprot id, protein name, length, link to alphafold database
# and links to download structures from alphafold database
rel_cols = ['Gene', 'Entry', 'Protein names', 'Length', 'Link AlphaFold Database',  'Link to AF mmCIF']

# write output to a csv file in the results directory
os.chdir(results_dir)
output_df[rel_cols].to_csv('08_AlphaFold_structures.csv', index = False)

# change back to target directory
os.chdir(target_directory)

print('\n============================== Summary ================================================\n')
print(f'    o      A total of {len(uniprot_data)} UniProt IDs have been found for the inputted {len(genes)} genes.')
print(f'    o      Crosslinks to the corresponding entry page in the AlphaFold database and to download data have been added.')
# print(f'    o      AlphaFold predicted structures have been downloaded for {len(output_df[output_df.Status == "downloaded"])} out of {len(uniprot_data)} identified UniProt IDs.\n')

print('The following files have been created:')
print('   o      08_AlphaFold_structures.csv      (contains information on identified AlphaFold structures)\n\n')

# print script name to console/log file
print(f'end of script {script_name}')

# store current date and time in an object and print to console / write to log file
end_time = datetime.now()
print(f'start: {start_time}')
print(f'end: {end_time}\n\n')
print('........................................................................................................................................................\n\n\n')

# close search log
if create_search_log == True:
    sys.stdout.close()
