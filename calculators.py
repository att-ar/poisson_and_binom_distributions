from scipy.stats import poisson, binom
import streamlit as st
import numpy as np
import plotly.express as px
from pandas import DataFrame

st.title("Discrete Poisson and Binomial Distributions Probability Calculator")
header = st.container()

with header:
    distrib = st.selectbox("Select distribution",
                           ("Poisson", "Binomial"))
    st.write(f"{distrib} selected")
    cols = st.columns(2)
    with cols[1]:
        method = st.selectbox("Select:",
                              ("P(X=x)", "P(X≥x)", "P(X≤x)"))


def display_pois(func, x, method):
    x_dis = np.arange(func.ppf(0.0001),
                      func.ppf(0.999))

    if method != "P(X=x)":
        y_dis = func.cdf(x_dis)
        color = ["other"] * len(x_dis)

        if method == "P(X≥x)":
            color[:int(x - min(x_dis) + 1)] = ["wanted"] * \
                int(x - min(x_dis) + 1)
        else:
            color[int(x - min(x_dis)):] = ["wanted"] * \
                int(len(x_dis) - x + min(x_dis))

        df_plot = DataFrame(data={"x": x_dis,
                                  "P(x)": y_dis,
                                  "color": color})

        run = px.bar(df_plot, "x", "P(x)",
                     color="color",
                     color_discrete_map={
                         "wanted": "yellow",
                         "other": "navy"},
                     title="Poisson Cumulative Distribution Function: yellow -> wanted x-values")
        run.update_layout(xaxis=dict(tickmode="linear"))
        st.plotly_chart(run)

    # probability mass function:
    y_pmf = func.pmf(x_dis)
    color_pmf = ["other"] * len(x_dis)
    color_pmf[int(x - min(x_dis))] = "wanted"
    pmf_plot = DataFrame(data={
        "x": x_dis,
        "P(x)": y_pmf,
        "color": color_pmf})
    pmf_run = px.bar(pmf_plot, "x", "P(x)",
                     color="color",
                     color_discrete_map={
                         "wanted": "yellow",
                         "other": "navy"},
                     title="Poisson Probability Mass Function: yellow -> wanted x-value")
    pmf_run.update_layout(xaxis=dict(tickmode="linear"))
    st.plotly_chart(pmf_run)


def display_bin(func, x, p, method):


if distrib[0] == "P":
    with cols[0]:
        lambd = st.number_input(label="λ", value=1.0,
                                min_value=0.05, step=0.05)
    func = poisson(lambd)
    with cols[0]:
        x = int(st.number_input(label="x",
                                value=int(func.ppf(0.0001)),
                                min_value=int(func.ppf(0.0001)),
                                max_value=int(func.ppf(0.999) - 1)
                                )
                )
        st.write("x:", x, "lam:", lambd)

    stats = func.stats(moments="mv")
    st.write(f"Mean: {stats[0]} | Variance: {stats[1]}")

    # display graphs
    display_pois(func, x, method)

    # check accuracy of cumulative distrib function and percent point function
    prob = func.cdf(x)
    np.allclose(x, func.ppf(prob))

    if method == "P(X=x)":
        chance = func.pmf(x)
    elif method == "P(X≥x)":
        chance = func.cdf(x)
    elif method == "P(X≤x)":
        chance = 1 - func.cdf(x-1)
    with cols[1]:
        st.header(f"{method} = {round(chance, 5)}")

if distrib[0] == "B":
    x_dis = np.arange(func.ppf(0.0001),
                  func.ppf(0.999))

    if method != "P(X=x)":
        y_dis = func.cdf(x_dis)
      color = ["other"] * len(x_dis)

       if method == "P(X≥x)":
            color[:int(x - min(x_dis) + 1)] = ["wanted"] * \
                int(x - min(x_dis) + 1)
        else:
            color[int(x - min(x_dis)):] = ["wanted"] * \
                int(len(x_dis) - x + min(x_dis))

        df_plot = DataFrame(data={"x": x_dis,
                                  "P(x)": y_dis,
                                  "color": color})
