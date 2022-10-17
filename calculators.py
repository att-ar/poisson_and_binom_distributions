from scipy.stats import poisson, binom
import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.title("Discrete Poisson and Binomial Distributions Probability Calculator")
header = st.container()

with header:
    distrib = st.selectbox("Select distribution",
                           ("Poisson", "Binomial"))
    st.write(f"{distrib} selected")
    cols = st.columns(2)
    with cols[1]:
        method = st.selectbox("Select:",
                              ("P(X=x)", "P(X≥x)", "P(X≤x)", "P(x1≤X≤x2)"))

def check_acc(func, x):
    "Checks the accuracy of the distribution functions"
    prob = func.cdf(x)
    assert np.allclose(x, func.ppf(prob)), "cdf and ppf are not accurate"

def create_color(method, x_dis, *args):
    '''Helper function that changes the color of the graphs according to the X inputs'''
    color = ["other"] * len(x_dis)

    if method != "P(x1≤X≤x2)":
        x = args[0]
        color[int(x - min(x_dis))] = "wanted"
        if method != "P(X=x)":

            if method == "P(X≤x)":
                color[:int(x - min(x_dis) + 1)] = ["wanted"] * \
                    int(x - min(x_dis) + 1)
            else:
                color[int(x - min(x_dis)):] = ["wanted"] * \
                    int(len(x_dis) - x + min(x_dis))

    else:
        x1, x2 = args
        color[int(x1 - min(x_dis)):
              int(x2 - min(x_dis) + 1)] = ["wanted"] * int(x2 - x1 + 1)
    
    return color


def display_pois(func, method, *args):
    '''
    scipy.stats function, string[,int[,int]]] -> plotly chart, float

    This function graphs a Poisson probability distribution based on user input
    Returns the probability of obtaining the random variable input by the user.
    '''
    x_dis = np.arange(func.ppf(0.00001),
                      func.ppf(0.99999))
    y_dis = func.cdf(x_dis)
    if len(args) == 1:
        x = args[0]
        color = create_color(method, x_dis, x)
    else:
        x1,x2 = args
        color = create_color(method, x_dis, x1, x2)

    df_plot = pd.DataFrame(data={"x": x_dis,
                              "P(x)": y_dis,
                              "color": color})
    run = px.bar(df_plot, "x", "P(x)",
                    color="color",
                    color_discrete_map={
                        "wanted": "yellow",
                        "other": "navy"},
                    title="Poisson Cumulative Distribution Function: yellow -> wanted x-values")
    run.update_layout(xaxis=dict(tickmode="linear"))

    # probability mass function:
    y_pmf = func.pmf(x_dis)
    pmf_plot = pd.DataFrame(data={
        "x": x_dis,
        "P(x)": y_pmf,
        "color": color})
    pmf_run = px.bar(pmf_plot, "x", "P(x)",
                     color="color",
                     color_discrete_map={
                         "wanted": "yellow",
                         "other": "navy"},
                     title="Poisson Probability Mass Function: yellow -> wanted x-value")
    pmf_run.update_layout(xaxis=dict(tickmode="linear"))
    
    st.plotly_chart(run)
    st.plotly_chart(pmf_run)



def display_bin(func, method, *args):
    '''
    scipy.stats function, string[,int[,int]]] -> plotly chart, float

    This function graphs a Binomial probability distribution based on user input
    Returns the probability of obtaining the random variable input by the user.
    '''
    x_dis = np.arange(func.ppf(0.00001),
                      func.ppf(0.99999))
    y_dis = func.cdf(x_dis)

    if len(args) == 1:
        x = args[0]
        color = create_color(method, x_dis, x)
    else:
        x1,x2 = args
        color = create_color(method, x_dis, x1, x2)

    df_plot = pd.DataFrame(data={"x": x_dis,
                              "P(x)": y_dis,
                              "color": color})

    run = px.bar(df_plot, "x", "P(x)",
                    color="color",
                    color_discrete_map={
                        "wanted": "yellow",
                        "other": "navy"},
                    title="Poisson Cumulative Distribution Function: yellow -> wanted x-values")
    run.update_layout(xaxis=dict(tickmode="linear"))

    # probability mass function:
    y_pmf = func.pmf(x_dis)
    pmf_plot = pd.DataFrame(data={
        "x": x_dis,
        "P(x)": y_pmf,
        "color": color})
    pmf_run = px.bar(pmf_plot, "x", "P(x)",
                     color="color",
                     color_discrete_map={
                         "wanted": "orange",
                         "other": "blue"},
                     title="Binomial Probability Mass Function: orange -> wanted x-value")
    pmf_run.update_layout(xaxis=dict(tickmode="linear"))

    st.plotly_chart(run)
    st.plotly_chart(pmf_run)
#------------------------------------------------------------------------------------
#placeholders:
x, x1, x2 = 0, 0, 0
if distrib[0] == "P":
    with cols[0]:
        lambd = st.number_input(label="λ", value=1.0,
                                min_value=0.05, step=0.05)
    func = poisson(lambd)
    with cols[0]:
        if method != "P(x1≤X≤x2)":
            x = int(st.number_input(label="X",
                                    value=int(func.ppf(0.0001)),
                                    min_value=int(func.ppf(0.00001)),
                                    max_value=int(func.ppf(0.99999) - 1)
                                    )
                    )
            st.write("X:", x, "lam:", lambd)
        else:
            x1 = int(st.number_input(label="X1",
                                     value=int(func.ppf(0.0001)),
                                     min_value=int(func.ppf(0.00001)),
                                     max_value=int(func.ppf(0.99999) - 2)))
            x2 = int(st.number_input(label="X2",
                                     value=int(func.ppf(0.9999) - 1),
                                     min_value=x1,
                                     max_value=int(func.ppf(0.99999) - 1)))
            st.write("X1:", x1, "X2:", x2, "lam", lambd)

    stats = func.stats(moments="mv")
    st.write(f"Mean: {stats[0]} | Variance: {stats[1]}")

    # display graphs
    if method != "P(x1≤X≤x2)":
        display_pois(func, method, x)
        # check accuracy of cumulative distrib function and percent point function
        check_acc(func, x)
    else:
        display_pois(func, method, x1, x2)
        # check accuracy of cumulative distrib function and percent point function
        check_acc(func, x1)

    methods_result = {"P(X=x)": func.pmf(x),
                    "P(X≥x)": 1 - func.cdf(x-1),
                    "P(X≤x)": func.cdf(x),
                    "P(x1≤X≤x2)": func.cdf(x2) - func.cdf(x1 - 1)
                    }
    chance = methods_result[method]

    with cols[1]:
        st.header(f"{method} = {round(chance, 9)}")

if distrib[0] == "B":
    with cols[0]:
        n = int(st.number_input(label="n", value=10, min_value=1, step=1))
        p = float(st.number_input(label="p (prob of success)", value=0.01,
                  min_value=0.0, max_value=1.0, step=0.001))
    func = binom(n, p)
    with cols[0]:
        if method != "P(x1≤X≤x2)":
            x = int(st.number_input(label="X",
                                    value=int(func.ppf(0.0001)),
                                    min_value=int(func.ppf(0.0001)),
                                    max_value=int(func.ppf(0.99999) - 1)
                                    )
                    )
            st.write("X:", x, "n:", n, "p:", p)
        else:
            x1 = int(st.number_input(label="X1",
                                     value=int(func.ppf(0.0001)),
                                     min_value=int(func.ppf(0.0001)),
                                     max_value=int(func.ppf(0.99999) - 2)))
            x2 = int(st.number_input(label="X2",
                                     value=int(func.ppf(0.999) - 1),
                                     min_value=x1,
                                     max_value=int(func.ppf(0.99999) - 1)))
            st.write("X1:", x1, "X2:", x2, "n:", n, "p", p)
    stats = func.stats(moments="mv")
    st.write(f"Mean: {stats[0]} | Variance: {stats[1]}")

    if method != "P(x1≤X≤x2)":
        display_bin(func, method, x)
        # check accuracy of cumulative distrib function and percent point function
        check_acc(func, x)
    else:
        display_bin(func, method, x1, x2)
        # check accuracy of cumulative distrib function and percent point function
        check_acc(func, x1)

    methods_result = {"P(X=x)": func.pmf(x),
                    "P(X≥x)": 1 - func.cdf(x),
                    "P(X≤x)": func.cdf(x),
                    "P(x1≤X≤x2)": func.cdf(x2) - func.cdf(x1 - 1)
                    }
    chance = methods_result[method]
    
    with cols[1]:
        st.header(f"{method} = {round(chance, 9)}")
