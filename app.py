import marimo

__generated_with = "0.25.0"
app = marimo.App(
    app_title="Calidad del Agua en Perú",
    layout_file="layouts/app.grid.json",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Calidad del agua en Perú
    """)
    return


@app.cell(hide_code=True)
def _():
    import pandas as pd
    import numpy as np
    import marimo as mo
    import plotly as plt
    import plotly.graph_objects as go

    return go, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Dataframe
    """)
    return


@app.cell
def _(pd):
    df = pd.read_parquet(
        "https://github.com/Gbarrantes25/WaterQuality/blob/main/datos_morea.parquet"
    )

    df
    return (df,)


@app.cell
def _(pd):
    df_location = pd.read_parquet(
        r"D:\Fuentes de Datos (csv,parquet,xlsx, etc)\PARQUET\Calidad de Agua en Peru\Ubicacion.parquet"
    )

    df_location.index = df_location.index + 1
    df_location.index.name = "estacion_id"
    df_location = df_location.reset_index()
    df_location
    return (df_location,)


@app.cell
def _(df, df_location, pd):
    df_merge = df.merge(
        df_location[["estacion_id", "REGIÓN", "ESTACIÓN"]],
        how="left",
        on="estacion_id",
    )
    df_merge["REGIÓN"] = df_merge["REGIÓN"].astype("category")
    df_merge["ESTACIÓN"] = df_merge["ESTACIÓN"].astype("category")
    df_merge["ph"] = df_merge["ph"].round(2)
    df_merge["cloro"] = df_merge["cloro"].round(2)
    df_merge["temperatura"] = df_merge["temperatura"].round(2)
    df_merge["fecha"] = pd.to_datetime(df_merge["fecha"])
    df_merge["fecha"] = df_merge["fecha"].dt.to_period("M")
    df_merge
    return (df_merge,)


@app.cell
def _(df_merge):
    df_ag = (
        df_merge.groupby(["fecha", "REGIÓN"])
        .agg({"cloro": "median", "ph": "median"})
        .reset_index()
    )

    df_ag["fecha"] = df_ag["fecha"].astype("str")
    df_ag
    return (df_ag,)


@app.cell
def _(df_ag, go):
    fig = go.Figure()
    lineas = go.Scatter(
        x=df_ag["fecha"], y=df_ag["ph"], mode="lines", line_shape="spline"
    )
    fig.add_traces([lineas])
    fig.update_layout(title="Ph de agua")
    fig
    return


if __name__ == "__main__":
    app.run()
