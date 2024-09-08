import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_2d_data(data, plot_type='slices', 
                 slice_idx=None, 
                 dynamic_idx=None, 
                 title='Proton Density', 
                 color_continuous_scale='gray',
                 colorbar_title_text = "Intensity", 
                 interval=8, 
                 rotate_xy_axes=False
                 ):
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
        rotate_xy_axes (bool): Rotate the data along the XY axes.
    """
    # Rotate data if rotate_xy_axes is True
    if rotate_xy_axes:
        data = np.rot90(data, k=1, axes=(0, 1))

    # Determine the global zmin and zmax for consistent color scaling
    zmin = np.min(data)
    zmax = np.max(data)

    ndim = data.ndim
    min_size = 600  # Minimum size for width and height

    if plot_type == 'slices':
        if ndim < 3:
            raise ValueError("Data must have at least 3 dimensions to plot slices.")

        dynamic_idx = dynamic_idx if dynamic_idx is not None else 0
        num_slices = data.shape[2]

        # Determine grid layout
        cols = min(num_slices, 4)  # Use the actual number of slices if less than 4
        rows = (num_slices + cols - 1) // cols

        fig = make_subplots(
            rows=rows, 
            cols=cols, 
            subplot_titles=[f'Slice {i+1}' for i in range(num_slices)],
            # horizontal_spacing=0,  # Reduce horizontal space between subplots
            # vertical_spacing=0.05   # Reduce vertical space between subplots
        )

        for i in range(num_slices):
            row = i // cols + 1
            col = i % cols + 1
            fig.add_trace(
                go.Heatmap(z=data[:, :, i, dynamic_idx], colorscale=color_continuous_scale, zmin=zmin, zmax=zmax, showscale=False),
                row=row, col=col
            )
        
        fig.update_layout(
            title=title,
            font=dict(family="Open Sans", color="black", size=16),  # Set title font and color
            width=max(data.shape[0]*cols, min_size),
            height=max(data.shape[1]*rows, min_size)
        )

        # Remove axis labels and ticks
        for i in range(1, num_slices + 1):
            fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, row=1, col=i)
            fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, row=1, col=i)

        colorbar_length = min(1, 1 * cols)
        last_trace_index = len(fig.data) - 1  
        fig.data[last_trace_index].update(
            showscale=True,
            colorbar=dict(
                orientation="h",  # Horizontal color bar
                y=-0.2,  # Position it below the plots
                thickness=15,  # Thickness of the color bar
                len=colorbar_length,  # Length of the color bar
                outlinecolor='black',  # Border color
                outlinewidth=1,  # Border width
                showticklabels=True,
                tickfont=dict(
                    size=12,  # Font size for tick labels
                    color='black',  # Font color for tick labels
                ),
            ),
            colorbar_title_font_family="Open Sans",
            colorbar_title_font_color = "black",
            colorbar_title_side = "bottom",
            colorbar_title_text = colorbar_title_text
        )  

    elif plot_type == 'dynamics':
        if ndim < 4:
            raise ValueError("Data must have at least 4 dimensions to plot dynamics.")

        slice_idx = slice_idx if slice_idx is not None else 0
        num_dynamics = data.shape[3]

        if num_dynamics > 16:
            interval = interval if interval > 0 else 8
            dynamics_indices = list(range(0, num_dynamics, interval))
        else:
            dynamics_indices = list(range(num_dynamics))

        if dynamics_indices[0] != 0:
            dynamics_indices.insert(0, 0)
        if dynamics_indices[-1] != num_dynamics - 1:
            dynamics_indices.append(num_dynamics - 1)

        cols = min(num_dynamics, 4)  # Use the actual number of slices if less than 4
        rows = (len(dynamics_indices) + cols - 1) // cols
        fig = make_subplots(
            rows=rows, 
            cols=cols, 
            subplot_titles=[f'Dyn. {i+1}' for i in dynamics_indices],
            horizontal_spacing=0,  # Reduce horizontal space between subplots
            vertical_spacing=0.05      # Reduce vertical space between subplots
        )

        for idx, i in enumerate(dynamics_indices):
            row = idx // cols + 1
            col = idx % cols + 1
            fig.add_trace(
                go.Heatmap(z=data[:, :, slice_idx, i], colorscale=color_continuous_scale, zmin=zmin, zmax=zmax, showscale=False),
                row=row, col=col
            )
        
        fig.update_layout(
            title=title,
            font=dict(family="Open Sans", color="black", size=16),  # Set title font and color
            width=max(200 * cols, min_size),
            height=max(200 * rows, min_size)
        )

        # Remove axis labels and ticks for all subplots
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, row=i, col=j)
                fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, row=i, col=j)

        colorbar_length = min(1, 1 * cols)
        last_trace_index = len(fig.data) - 1  
        fig.data[last_trace_index].update(
            showscale=True,
            colorbar=dict(
                orientation="h",  # Horizontal color bar
                y=-0.2,  # Position it below the plots
                thickness=15,  # Thickness of the color bar
                len=colorbar_length,  # Length of the color bar
                outlinecolor='black',  # Border color
                outlinewidth=1,  # Border width
                showticklabels=True,
                tickfont=dict(
                    size=12,  # Font size for tick labels
                    color='black',  # Font color for tick labels
                ),
            ),
            colorbar_title_font_family="Open Sans",
            colorbar_title_font_color = "black",
            colorbar_title_side = "bottom",
            colorbar_title_text = colorbar_title_text  
        )
    return fig

