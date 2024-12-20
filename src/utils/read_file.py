import json
import yaml
import pickle
import pandas as pd
import logging

def read_file(file_path: str, time_series: str = 'no', index: str = 'Date'):
    """
    Function that reads in data by calling necessary read function

    Returns
    -------
    data:
        loaded data from file
    """
    # file extension
    file_type = file_path.split('.')[-1]

    # json
    if file_type == 'json':
        data = _read_json(file_path)
    
    # yaml
    elif file_type == 'yaml':
        data = _read_yaml(file_path)
    
    # pickle
    elif file_type == 'pkl':
        data = _read_pickle(file_path)

    # text
    elif file_type == 'txt':
        data = _read_txt(file_path)

    # sql
    elif file_type == "sql":
        data = _read_txt(file_path)

    # csv
    elif file_type == 'csv':
        
        # time series
        if time_series != 'no':
            data = _read_time_series_csv(file_path, index)
            data.index = pd.to_datetime(data.index)
        
        # non-time series
        else:
            data = pd.read_csv(file_path)

    # error for other unrecognized extensions
    else:
        logging.info(LoadFileExtensionError(file_path))
        raise LoadFileExtensionError(file_path)

    return data

def _read_json(file_path: str) -> dict:
    """
    Function that reads json file as dictionary
    
    Parameters
    --------
    file_path : str
        path to file

    Returns
    -------
    data: dict
        dictionary of loaded data
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data

def _read_yaml(file_path: str):
    """
    Function that reads YAML file as dicitonary
    
    Parameters
    ----------
    file_path: str
        path to file
        
    Returns
    -------
    data: dict
        data in dictionary form
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data

def _read_pickle(file_path: str):
    """
    Function that reads pickle file 

    Parameters
    --------
    file_path : str
        path to file

    Returns
    -------
    data: str/dict/class
        
    """
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    return data

def _read_txt(file_path: str):
    """
    Function that reads YAML file as dicitonary
    
    Parameters
    ----------
    file_path: str
        path to file
        
    Returns
    -------
    data: str
        data in string form
    """
    with open(file_path, 'r') as data_file:
            data = data_file.read()

    return data

def _read_time_series_csv(file_path: str, index: str = 'Date'):
    """
    Function that reads in timeseries dataset
    
    Parameters
    ----------
    file_path: str
        path to file
        
    Returns
    -------
    data: pd.DataFrame
        data
    """
    data = pd.read_csv(file_path)
    data = data.set_index(index)
    data.index = pd.to_datetime(data.index)

    return data

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class LoadFileExtensionError(Exception):
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"""
                         Cannot load in file {file_path} with read_file.
                         Possible extensions include: json, yaml, pkl, csv. 
                         """)
        
class WriteFileExtensionError(Exception):
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"""
                         Cannot write file {file_path} with write_file.
                         Possible extensions include: yaml, pkl, txt. 
                         """)