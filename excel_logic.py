import pandas as pd


class ExcelManager:
    def load_excel(self, file_path):
        return pd.read_excel(file_path)

    def merge_excels(self, files):
        dfs = []
        for file_path in files:
            df = pd.read_excel(file_path)
            dfs.append(df)
        merged = pd.concat(dfs, ignore_index=True)
        return merged, dfs
