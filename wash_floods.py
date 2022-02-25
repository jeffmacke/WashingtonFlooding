# Monte Carlo simulation for flood damages in Washington, Illinois
# For loop to run for the number of simulations desired

# Importing Packages
import streamlit as st
import matplotlib.pyplot as plt
import random
import altair as alt
import numpy as np
import pandas as pd

st.title('Flood Damages')

st.sidebar.header('Select Number of Simulations')
selected_sims = st.sidebar.text_input('Simulations')


st.markdown("""
This app performs monte carlo analysis of flood damages in Washington.
* **Python libraries:** seaborn, pandas, random, streamlit
""")


# Creating Roll Dice Function
def sim_year():
    year_chance = random.randint(1, 500)

    # Determining if the dice are the same number
    if year_chance < 51:
        storm = '10-Year'
    elif year_chance > 50 and year_chance < 71:
        storm = '25-Year'
    elif year_chance > 80 and year_chance < 86:
        storm = '100-Year'
    elif year_chance == 86:
        storm = '500-Year'
    else:
        storm = False
    return storm

# Inputs
num_simulations = int(selected_sims)
max_year = 2072

# Tracking
flood_probability = []
end_balance = []

#graph
fig,ax= plt.subplots()

for i in range(num_simulations):
    balance = [0]
    year = [2022]
    num_floods = 0
    # Run until max years is exceeded
    while year[-1] < max_year:
        flood = sim_year()
        # Result if 500-year flood occurs
        if flood == '500-Year':
            balance.append(balance[-1] + 30000000)
            num_floods += 1
        # Result if 100-year flood occurs
        elif flood == '100-Year':
            balance.append(balance[-1] + 18000000)
            num_floods += 1
        # Result if 25-year flood occurs
        elif flood == '25-Year':
            balance.append(balance[-1] + 12000000)
            num_floods += 1
        # Result if 10-year flood occurs
        elif flood == '10-Year':
            balance.append(balance[-1] + 8000000)
            num_floods += 1
        else:
            balance.append(balance[-1])
        year.append(year[-1] + 1)
# Store tracking variables and add line to figure
    flood_probability.append(num_floods/(year[-1]-2022))
    end_balance.append(balance[-1])
    ax.plot(year, balance)
    source = pd.DataFrame({'Year':year,'Damages':balance})
    altchart = alt.Chart(source).mark_line().encode(x='Year',y='Damages')


# Showing the plot after the simulations are finished
st.pyplot(fig)
# Averaging win probability and end balance
overall_flood_probability = sum(flood_probability)/len(flood_probability)
overall_end_balance = sum(end_balance)/len(end_balance)
# Displaying the averages
st.write("Average flood probability after " + str(num_simulations) + " sims: " + str(overall_flood_probability))
st.write("Average damages after " + str(num_simulations) + " sims: $" + str(overall_end_balance))


st.altair_chart(altchart,use_container_width=True)
