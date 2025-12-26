import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gradient Explorer", layout="wide")

st.title("🏔️ Gradient & Direction of Steepest Ascent")
st.markdown("""
This interactive application visualizes the concept of the **Gradient Vector** on functions of two variables.
The gradient (red arrow) always points in the **direction of steepest ascent**.
""")

# --- SIDEBAR (CONTROLS) ---
st.sidebar.header("Settings")

# Function selection (Meeting the "two complexities" requirement)
function_choice = st.sidebar.selectbox(
    "Choose a Surface Function:",
    ("Bowl (Simple): z = x² + y²", "Mountains (Complex): z = sin(x) * cos(y)")
)

# Sliders for point position (x, y)
st.sidebar.subheader("Point Position")
x_val = st.sidebar.slider("Value of x", -2.0, 2.0, 0.5, 0.1)
y_val = st.sidebar.slider("Value of y", -2.0, 2.0, 0.5, 0.1)

# --- FUNCTIONS & DERIVATIVES DEFINITION ---
def calculate_surface(choice, x, y):
    if "Bowl" in choice:
        # Simple Function: f(x,y) = x^2 + y^2
        z = x**2 + y**2
        # Partial Derivatives (Gradient components)
        dz_dx = 2*x
        dz_dy = 2*y
    else:
        # Complex Function: f(x,y) = sin(x)*cos(y)
        z = np.sin(x) * np.cos(y)
        # Partial Derivatives using chain rule
        dz_dx = np.cos(x) * np.cos(y)
        dz_dy = -np.sin(x) * np.sin(y)
    
    return z, dz_dx, dz_dy

# Calculate values for the chosen point
z_val, grad_x, grad_y = calculate_surface(function_choice, x_val, y_val)

# --- DYNAMIC MATH EXPLANATIONS (Sidebar) ---
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Real-time Calculations")
st.sidebar.latex(r"\nabla f = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right)")
st.sidebar.write(f"Gradient at point ({x_val}, {y_val}):")
st.sidebar.code(f"∇f = [{grad_x:.2f}, {grad_y:.2f}]")
st.sidebar.write(f"Steepness (Magnitude): {np.sqrt(grad_x**2 + grad_y**2):.2f}")

# --- 3D VISUALIZATION (PLOTLY) ---
# Create grid for the floor
X = np.linspace(-2.5, 2.5, 50)
Y = np.linspace(-2.5, 2.5, 50)
X, Y = np.meshgrid(X, Y)

# Calculate Z for the whole grid
if "Bowl" in function_choice:
    Z = X**2 + Y**2
else:
    Z = np.sin(X) * np.cos(Y)

fig = go.Figure()

# 1. Add the 3D Surface
fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name="Surface"))

# 2. Add the specific Point P
fig.add_trace(go.Scatter3d(
    x=[x_val], y=[y_val], z=[z_val],
    mode='markers', marker=dict(size=8, color='red'), name="Point P"
))

# 3. Add the Gradient Vector (3D Cone/Arrow)
fig.add_trace(go.Cone(
    x=[x_val], y=[y_val], z=[z_val], # Start point
    u=[grad_x], v=[grad_y], w=[0],   # Direction (Gradient lies on the xy-plane mathematically, projected here)
    sizemode="absolute", sizeref=0.5, anchor="tail", showscale=False, colorscale=[[0, 'red'], [1, 'red']],
    name="Gradient Vector"
))

# Layout formatting
fig.update_layout(
    title="Interactive 3D Visualization",
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis (Height)',
        aspectmode='cube'
    ),
    width=800, height=600,
    margin=dict(l=0, r=0, b=0, t=40)
)

st.plotly_chart(fig)

# --- THEORETICAL EXPLANATION SECTION ---
st.header("Concept Explanation")
st.write("""
### 1. The Gradient Vector (Red Arrow)
The gradient vector $\\nabla f$ at any point $(x,y)$ indicates the direction in which the function increases most rapidly. If you were standing on the surface at the red dot, the arrow points directly uphill.

### 2. Partial Derivatives
The gradient is composed of the partial derivatives of the function:
$$ \\nabla f(x,y) = \\frac{\\partial f}{\\partial x} \\mathbf{i} + \\frac{\\partial f}{\\partial y} \\mathbf{j} $$
* **$\\frac{\\partial f}{\\partial x}$** represents the slope in the x-direction.
* **$\\frac{\\partial f}{\\partial y}$** represents the slope in the y-direction.

### 3. Real-World Application: AI & Optimization
This concept is fundamental in **Machine Learning**. Algorithms use "Gradient Descent" (moving opposite to the gradient) to find the minimum error in a model. Just as the gradient points to the steepest ascent, the negative gradient points to the steepest descent, allowing AI to "learn" by minimizing mistakes.
""")
