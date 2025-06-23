# data_manager.py
# This is where I list my datasets and remove them
import pandas as pd
import uuid

# Global in-memory store:
#   { dataset_id (str) → { "name": original_filename,
#                          "df": pandas.DataFrame } }
DATASETS = {}

def add_dataset(file_storage):
    """
    Parse uploaded CSV/JSON, store the DataFrame, and return:
      - dataset_id (str)
      - list of column names
    Raises ValueError on parse error or unsupported type.
    """
    filename = file_storage.filename
    ext = filename.rsplit('.', 1)[-1].lower()

    try:
        if ext == 'csv':
            df = pd.read_csv(file_storage)
        elif ext == 'json':
            df = pd.read_json(file_storage)
        else:
            raise ValueError(f'Unsupported file type: .{ext}')
    except Exception as e:
        raise ValueError(f'Could not parse file: {e}')

    ds_id = str(uuid.uuid4())
    DATASETS[ds_id] = {
        'name': filename,
        'df': df
    }
    return ds_id, list(df.columns)

def list_datasets():
    """
    Return a dict mapping id → { name, columns } for every loaded dataset.
    """
    return {
        ds_id: {
            'name': meta['name'],
            'columns': list(meta['df'].columns)
        }
        for ds_id, meta in DATASETS.items()
    }

def remove_dataset(ds_id):
    """
    Remove the dataset with the given id (if it exists).
    """
    DATASETS.pop(ds_id, None)

def get_series(ds_id, column):
    """
    Return the data for one series:
      - y: list of values in that column
      - x: list of index labels (as strings)

    Raises KeyError if ds_id or column not found.
    """
    meta = DATASETS[ds_id]  # KeyError if not present
    df = meta['df']
    if column not in df.columns:
        raise KeyError(f'Column "{column}" not in dataset {ds_id}')

    # x will be the DataFrame’s index
    x = df.index.astype(str).tolist()
    y = df[column].tolist()
    return y, x
