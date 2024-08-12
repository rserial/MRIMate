import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import logging

def plot_proton_density(data, plot_type='slices', slice_idx=None, dynamic_idx=None, title='Proton Density', color_continuous_scale='gray', interval=8, rotate_xy_axes=False):
    """
    Generate and return a plot for proton density data.

    Args:
        data (ndarray): The MRI data to plot.
        plot_type (str): Type of plot to generate ('slices' or 'dynamics').
        slice_idx (int, optional): Index of the slice to plot when plot_type='dynamics'.
        dynamic_idx (int, optional): Index of the dynamic to plot when plot_type='slices'.
        title (str): Title of the plot.
        color_continuous_scale (str): Color scale for the plot.
        interval (int): Interval between dynamics to plot when plot_type='dynamics'.
    """
    # Normalize data
    data = (data - np.min(data)) / (np.max(data) - np.min(data))

    # Rotate data if rotate is True
    if rotate_xy_axes:
        # data = np.transpose(data, (1, 0, 2, 3))
        # Rotate 90 degrees clockwise in the xy plane
        data = np.rot90(data, k=1, axes=(0, 1))
    # Determine the global zmin and zmax for consistent color scaling
    zmin = np.min(data)
    zmax = np.max(data)

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Determine the shape of the data
    ndim = data.ndim
    if plot_type == 'slices':
        if ndim < 3:
            raise ValueError("Data must have at least 3 dimensions to plot slices.")

        # If a specific dynamic is chosen, use it; otherwise, use the first dynamic by default
        dynamic_idx = dynamic_idx if dynamic_idx is not None else 0
        num_slices = data.shape[2]
        fig = make_subplots(rows=1, cols=num_slices, subplot_titles=[f'Slice {i+1}' for i in range(num_slices)])

        for i in range(num_slices):
            fig.add_trace(
                go.Heatmap(z=data[:, :, i, dynamic_idx], colorscale=color_continuous_scale, zmin=zmin, zmax=zmax, colorbar=dict(showticklabels=False)),
                row=1, col=i+1
            )
            fig.update_layout(
            title=title,
            font=dict(size=16),
            xaxis=dict(
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,
                showticklabels=True,
                tickcolor='black',
                ticks='outside',
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
            yaxis=dict(
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,
                showticklabels=True,
                tickcolor='black',
                ticks='outside',
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
        )

    elif plot_type == 'dynamics':
        if ndim < 4:
            raise ValueError("Data must have at least 4 dimensions to plot dynamics.")

        # If a specific slice is chosen, use it; otherwise, use the first slice by default
        slice_idx = slice_idx if slice_idx is not None else 0
        num_dynamics = data.shape[3]

        if num_dynamics > 16:
            interval = interval if interval > 0 else 4  # Set default interval to 4 if interval is not specified or invalid
            dynamics_indices = list(range(0, num_dynamics, interval))
        else:
            dynamics_indices = list(range(num_dynamics))

        # Always include the first and last dynamics
        if dynamics_indices[0] != 0:
            dynamics_indices.insert(0, 0)
        if dynamics_indices[-1] != num_dynamics - 1:
            dynamics_indices.append(num_dynamics - 1)

        # Log message about plotting interval
        print(f"Plotting every {interval} dynamics. You can change this by: plot_proton_density(..., interval=your_desired_interval)")

        cols = 4
        rows = (len(dynamics_indices) + cols - 1) // cols  # Calculate the number of rows needed
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f'Dyn. {i+1}' for i in dynamics_indices])

        for idx, i in enumerate(dynamics_indices):
            row = idx // cols + 1
            col = idx % cols + 1
            fig.add_trace(
                go.Heatmap(z=data[:, :, slice_idx, i], colorscale=color_continuous_scale, zmin=zmin, zmax=zmax, colorbar=dict(showticklabels=False)),
                row=row, col=col
            )

        fig.update_layout(
            width=200 * cols,
            height=300 * rows,
        )

        fig.update_layout(
            title=title,
            font=dict(size=16),
            xaxis=dict(
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,
                showticklabels=True,
                tickcolor='black',
                ticks='outside',
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
            yaxis=dict(
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,
                showticklabels=True,
                tickcolor='black',
                ticks='outside',
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
        )

    elif plot_type == '3d':
        if ndim < 3:
            raise ValueError("Data must have at least 3 dimensions to plot in 3D.")

        fig = go.Figure(data=go.Volume(
            x=np.arange(data.shape[0]),
            y=np.arange(data.shape[1]),
            z=np.arange(data.shape[2]),
            value=data.flatten(),
            isomin=zmin,
            isomax=zmax,
            opacity=0.1,  # Adjust for transparency
            surface_count=10,  # Adjust the number of isosurfaces
            colorscale=color_continuous_scale
        ))

    else:
        raise ValueError("Unsupported plot type. Supported types are 'slices', 'dynamics', and '3d'.")

    fig.update_layout(
        title=title,
        font=dict(size=16),
    )
    
    return fig
