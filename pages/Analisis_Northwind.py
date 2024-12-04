import pandas as pd
import sqlite3
import numpy as np
import os
import sys
from pathlib import Path
import plotly.express as px
import streamlit as st

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import *

fig = px.bar(conexion_ordenada, x='Cantidad', y='ProductName')
st.plotly_chart(fig)