import pandas as pd
from pathlib import Path


def get_language_results_path(script: str, script_language_result: pd.DataFrame, result_root: Path) -> list[Path]:
    """Get list of results path for given script"""

    results_script_lang = script_language_result.loc[script].to_list()[0]
    results_script_lang_path = [result_root.joinpath(lang).joinpath('results.csv') for lang in results_script_lang]

    return results_script_lang_path

def get_script_results(script: str, script_lang_df: pd.DataFrame, result_root: Path) -> pd.DataFrame:
    """Get results for a given script. output contains results for languages in the script"""

    results_script_path = get_language_results_path(script, script_lang_df, result_root)

    results_list = []
    for result_path in results_script_path:
        lang = result_path.parent.name
        df_res = pd.read_csv(result_path)
        df_res['language'] = lang
        results_list.append(df_res)

    results_script = pd.concat(results_list)
    results_script['script'] = script
    return results_script