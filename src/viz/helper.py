from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def display_box_plot(results_df: pd.DataFrame, metric_type = 'CER', script = ""):
    """Display Box Plot of error rate for given metric type

    :param results_df: _description_
    :type results_df: _type_
    :param metric_type: _description_, defaults to 'CER'
    :type metric_type: str, optional
    """
    fig = go.Figure()
    lang_list = list(results_df['language'].unique())

    fig = make_subplots(rows=results_df['language'].nunique(), 
                        cols=1, 
                        shared_yaxes=True,
                        subplot_titles=lang_list)

    if metric_type == 'CER':
        err_cols = ['cer_l0', 'cer_l1', 'cer_l2','cer_l3']
    if metric_type == 'WER':
        err_cols = ['wer_l0', 'wer_l1', 'wer_l2','wer_l3']

    for idx, language in enumerate(lang_list):
        results_lang = results_df.loc[results_df['language'] == language]
        for err_col in err_cols:
            fig.add_trace(go.Box(y=round(results_lang[err_col] * 100, 2),
                                    name=err_col,
                                    text=results_lang['file_id']), 
                                    row=idx + 1, col=1)


    fig.update_layout(height=1200, width=1400)
    fig.update_layout(showlegend=False, title_text=f"{metric_type} % across various degradation level in {script} languages")
    fig.update_yaxes(title_text=f"{metric_type} in %")

    return fig
