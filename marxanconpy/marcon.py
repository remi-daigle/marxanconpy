import os
import json
import sys
import marxanconpy

def new_project(rootpath='.'):
    """ New Project
    Create a new project dictionary
    :return: dict
    """

    project = {}
    project['version'] = {}
    project['version']['marxanconpy'] = marxanconpy.__version__
    project['version']['MarxanConnect'] = 'NA'
    project['filepaths'] = {}
    project['options'] = {}

    # set default options
    project['options']['fa_status'] = "Status-quo"
    project['options']['aa_status'] = "Status-quo"
    project['options']['demo_pu_cm_progress'] = True
    project['options']['demo_conmat_type'] = "Probability"
    project['options']['demo_conmat_format'] = "Matrix"
    project['options']['demo_conmat_rescale'] = "Identical Grids"
    project['options']['demo_conmat_rescale_edge'] = "Proportional to overlap"
    project['options']['land_hab_buff'] = "1"
    project['options']['land_hab_thresh'] = "0.001"
    project['options']['land_pu_cm_progress'] = True
    project['options']['land_conmat_type'] = "Habitat Type + Resistance"
    project['options']['land_res_matrixType'] = "Least-Cost Path"
    project['options']['calc_metrics_pu'] = True
    project['options']['calc_metrics_cu'] = False
    project['options']['metricsCalculated'] = False

    project['options']['demo_metrics'] = {}
    project['options']['demo_metrics']['in_degree'] = False
    project['options']['demo_metrics']['out_degree'] = False
    project['options']['demo_metrics']['between_cent'] = False
    project['options']['demo_metrics']['eig_vect_cent'] = False
    project['options']['demo_metrics']['google'] = False
    project['options']['demo_metrics']['self_recruit'] = False
    project['options']['demo_metrics']['local_retention'] = False
    project['options']['demo_metrics']['outflow'] = False
    project['options']['demo_metrics']['inflow'] = False
    project['options']['demo_metrics']['stochasticity'] = False
    project['options']['demo_metrics']['fa_recipients'] = False
    project['options']['demo_metrics']['fa_donors'] = False
    project['options']['demo_metrics']['aa_recipients'] = False
    project['options']['demo_metrics']['aa_donors'] = False

    project['options']['demo_metrics']['conn_boundary'] = False

    project['options']['land_metrics'] = {}
    project['options']['land_metrics']['in_degree'] = False
    project['options']['land_metrics']['out_degree'] = False
    project['options']['land_metrics']['between_cent'] = False
    project['options']['land_metrics']['eig_vect_cent'] = False
    project['options']['land_metrics']['google'] = False
    project['options']['land_metrics']['fa_recipients'] = False
    project['options']['land_metrics']['fa_donors'] = False
    project['options']['land_metrics']['aa_recipients'] = False
    project['options']['land_metrics']['aa_donors'] = False

    project['options']['land_metrics']['conn_boundary'] = False

    project['options']['cf_export'] = "Append"
    project['options']['spec_set'] = "Proportion"
    project['options']['targets'] = "0.5"

    project['options']['bd_filecheck'] = True
    project['options']['pudat_filecheck'] = True

    project['options']['NUMREPS'] = "100"
    project['options']['SCENNAME'] = "connect"
    project['options']['marxan_CF'] = "New"
    project['options']['marxan_bound'] = "New"
    project['options']['inputdat_boundary'] = "Symmetric"
    project['options']['CSM'] = "10"
    project['options']['marxan_PU'] = "New"
    project['options']['marxan_bit'] = "64-bit"
    project['options']['marxan'] = "Marxan"

    project['options']['pushp_filecheck'] = True
    project['options']['pucsv_filecheck'] = True
    project['options']['map_filecheck'] = True

    # set default file paths
    # spatial input
    project['filepaths']['pu_filepath'] = ""
    project['filepaths']['pu_file_pu_id'] = ""
    project['filepaths']['fa_filepath'] = ""
    project['filepaths']['aa_filepath'] = ""

    # connectivity input
    project['filepaths']['demo_cu_filepath'] = ""
    project['filepaths']['demo_cu_file_pu_id'] = ""
    project['filepaths']['demo_cu_cm_filepath'] = ""
    project['filepaths']['demo_pu_cm_filepath'] = ""
    project['filepaths']['land_cu_filepath'] = ""
    project['filepaths']['land_cu_file_hab_id'] = ""
    project['filepaths']['land_res_mat_filepath'] = ""
    project['filepaths']['land_res_filepath'] = ""
    project['filepaths']['land_res_file_hab_id'] = ""
    project['filepaths']['land_pu_cm_filepath'] = ""
    project['filepaths']['lp_filepath'] = ""

    # Marxan metrics files
    project['filepaths']['cf_filepath'] = os.path.join(rootpath,  "input", "puvspr_connect.dat")
    project['filepaths']['orig_cf_filepath'] = os.path.join(rootpath,  "input", "puvspr.dat")
    project['filepaths']['spec_filepath'] = os.path.join(rootpath,  "input", "spec_connect.dat")
    project['filepaths']['orig_spec_filepath'] = os.path.join(rootpath,  "input", "spec.dat")
    project['filepaths']['bd_filepath'] = os.path.join(rootpath,  "input", "boundary_connect.dat")
    project['filepaths']['orig_bd_filepath'] = os.path.join(rootpath,  "input", "boundary.dat")
    project['filepaths']['pudat_filepath'] = os.path.join(rootpath,  "input", "pu_connect.dat")
    project['filepaths']['orig_pudat_filepath'] = os.path.join(rootpath,  "input", "pu.dat")

    # Marxan analysis
    project['filepaths']['marxan_template_input'] = "Default"
    project['filepaths']['marxan_input'] = os.path.join(rootpath, "input.dat")

    # Post-Hoc Evaluation
    project['filepaths']['posthoc'] = os.path.join(rootpath,  "output", "posthoc.csv")

    # Export plot data
    project['filepaths']['pushp'] = os.path.join(rootpath,  "output", "pu.shp")
    project['filepaths']['pucsv'] = os.path.join(rootpath,  "output", "pu.csv")
    project['filepaths']['map'] = os.path.join(rootpath,  "output", "map.png")

    return project

def load_project(filename):
    """ Load Project
    Loads the project dictionary from a .MarCon file.
    :param filename:
    :return: dict
    """
    with open(filename, 'r') as fp:
        project = json.loads(fp.read())
    validate_project(project)
    return project

def edit_working_directory(project,wd,type="relative"):
    """ Edit the working directory
    Edits the filepath in the project dictionary. If type = 'relative', the absolute paths that contain the working
    directory are changed to relative paths and vice versa for type = 'absolute'
    :param project: the project dictionary
    :param wd: the working directory
    :param type: either 'relative' or 'absolute'
    :return: dict
    """
    if type == "relative":
        for p in project['filepaths']:
            if p != "working_directory":
                project['filepaths'][p] = project['filepaths'][p].replace(wd + "\\", ".\\")
    elif type == "absolute":
        for p in project['filepaths']:
            if p != "working_directory":
                project['filepaths'][p] = project['filepaths'][p].replace(".\\", wd + "\\")
    return project

def save_project(project,projfile=False):
    """ Save Project

    Saves the project dictionary to a .MarCon file.
    :param project: the project dictionary
    :param projfile: the (optional) filename for the project file to override the projfile entry given in the project
    dictionary.
    :return:
    """
    if projfile==False:
        projfile = project['filepaths']['projfile']
    with open(projfile, 'w') as fp:
        json.dump(project, fp, indent=4, sort_keys=True)

def validate_project(project):
    """ Validate Project

    A function to validate project dictionaries to ensure that they contains all necessary fields (i.e. keys).
    Different versions of marxanconpy may require slightly different fields.
    :param project: the project dictionary
    :return: dict
    """
    if 'marxanconpy' in project['version']:
        if project['version']['marxanconpy'] != marxanconpy.__version__:
            print("Warning: This project file was created with a different version of marxanconpy. Attempting to "
                  "update for compatibility")
            project['version']['marxanconpy'] = marxanconpy.__version__
    else:
        print("Warning: This project file was created with a different version of Marxan Connect. Attempting to "
              "update for compatibility")
        project['version'] = {}
        project['version']['marxanconpy'] = marxanconpy.__version__
        project['version']['MarxanConnect'] = "NA"


    np = new_project()

    for k in np.keys():
        if k not in project:
            print('Warning: This project file does not contain all the required fields (' + k +
                  '). Attempting to update for compatibility')
            project[k] = np[k]
        if type(np[k])==dict:
            for k2 in np[k].keys():
                if k2 not in project[k]:
                    print('Warning: This project file does not contain all the required fields (' + k2 +
                          '). Attempting to update for compatibility')
                    project[k][k2] = np[k][k2]
                if type(np[k][k2]) == dict:
                    for k3 in np[k][k2].keys():
                        if k3 not in project[k][k2]:
                            print('Warning: This project file does not contain all the required fields (' + k3 +
                                  '). Attempting to update for compatibility')
                            project[k][k2][k3] = np[k][k2][k3]
