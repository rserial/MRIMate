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

def plot_2d_slider(data, plot_type='slices', 
                   dynamic_idx=None, 
                   slice_idx=None,
                   title='Proton Density', 
                   color_continuous_scale='gray',
                   colorbar_title_text="Intensity", 
                   interval=1, 
                   rotate_xy_axes=False):
    """
    Generate an interactive slider plot for MRI data to slide through slices or dynamics.

    Args:
        data (ndarray): The MRI data to plot.
        plot_type (str): Type of plot to generate ('slices' or 'dynamics').
        slice_idx (int, optional): Index of the slice to plot when plot_type='dynamics'.
        dynamic_idx (int, optional): Index of the dynamic to plot when plot_type='slices'.
        title (str): Title of the plot.
        color_continuous_scale (str): Color scale for the plot.
        interval (int): Interval between slices or dynamics to plot in the slider.
        rotate_xy_axes (bool): Rotate the data along the XY axes.
    """
    # Rotate data if rotate_xy_axes is True
    if rotate_xy_axes:
        data = np.rot90(data, k=1, axes=(0, 1))

    # Determine the global zmin and zmax for consistent color scaling
    zmin = np.min(data)
    zmax = np.max(data)
    
    # Set default indices if not provided
    if plot_type == 'slices':
        num_slices = data.shape[2]
        dynamics = dynamic_idx if dynamic_idx is not None else 0
        indices = list(range(0, num_slices, interval))
        if indices[-1] != num_slices - 1:
            indices.append(num_slices - 1)
    elif plot_type == 'dynamics':
        num_dynamics = data.shape[3]
        slices = slice_idx if slice_idx is not None else 0
        indices = list(range(0, num_dynamics, interval))
        if indices[-1] != num_dynamics - 1:
            indices.append(num_dynamics - 1)
    else:
        raise ValueError("Invalid plot_type. Must be 'slices' or 'dynamics'.")

    # Create initial frame to display
    initial_frame = data[:, :, 0, dynamics] if plot_type == 'slices' else data[:, :, slices, 0]

    fig = go.Figure(
        data=[go.Heatmap(z=initial_frame, colorscale=color_continuous_scale, zmin=zmin, zmax=zmax)]
    )

    # Add frames for each slice or dynamic
    frames = [
        go.Frame(
            data=[go.Heatmap(
                z=data[:, :, i, dynamics] if plot_type == 'slices' else data[:, :, slices, i], 
                colorscale=color_continuous_scale, zmin=zmin, zmax=zmax)],
            name=str(i)
        )
        for i in indices
    ]
    
    fig.frames = frames

    # Set up slider steps
    slider_steps = [
        {"args": [[f.name], {"frame": {"duration": 100, "redraw": True}, "mode": "immediate"}],
         "label": str(i),
         "method": "animate"}
        for i, f in enumerate(fig.frames)
    ]

    # Set up sliders and buttons
    sliders = [{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 16, "color": "black", "family": "Open Sans"},
            "prefix": "Slice: " if plot_type == 'slices' else "Dynamic: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": slider_steps
    }]

    fig.update_layout(
        sliders=sliders,
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "mode": "immediate"}],
                    "label": "&#9654;",  # Play symbol
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    "label": "&#9724;",  # Pause symbol
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }],
        title=dict(
            text=title,
            font=dict(family="Open Sans", color="black", size=20)
        ),
        width=500,
        height=600
    )

    # Display colorbar with custom font and style
    fig.update_traces(showscale=True, colorbar=dict(
        title=colorbar_title_text,
        titleside="right",
        titlefont=dict(family="Open Sans", color="black", size=14),
        tickfont=dict(family="Open Sans", color="black", size=12),
        thickness=15,
        len=1.05,
        outlinecolor='black',
        outlinewidth=1
    ))

    # Show the figure
    fig.show()

