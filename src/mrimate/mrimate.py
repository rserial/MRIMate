"""Main module."""

from parrec.recread import Recread
from parrec.parread import Parread
from pathlib import Path
from datetime import datetime
import plotly.express as px
import numpy as np
from models import MRIExperiment_Philips


class MRImateExperiment:
    """
    Represents an MRI experiment conducted with MRImate software.

    This class provides methods for loading experiment parameters, processing data,
    plotting figures, and saving results.

    Attributes:
        par_file (str): The filename for the PAR file.
        rec_file (str): The filename for the REC file.

    Methods:
        __init__(self, experiment_path: pathlib.Path) -> None:
            Initializes an MRImateExperiment instance for the specified experiment directory.

        load(self) -> None:
            Loads experiment parameters from the PAR file.

        process(self) -> Tuple[MRIExperiment_Philips, Recread]:
            Processes the experiment data and returns the processed results.

        plot(self, output_data: Recread) -> Tuple[Optional[Tuple], Optional[str]]:
            Generates and returns plots for the processed data.

        save_fig(self, figure: Tuple, experiment_name: str) -> None:
            Saves a figure to the processed_data directory.

        save_data(self, output_data: Recread, experiment_name: str) -> None:
            Saves processed data to the processed_data directory.

        name(self) -> str:
            Gets the name of the experiment.

        type(self) -> str:
            Gets the type of MRImate experiment.
    """

    def __init__(self, experiment_path: Path, filename: str) -> None:
        """
        Initialize an MRImateExperiment instance.

        Args:
            experiment_path (Path): The path to the experiment directory.
            filename (str): The filename prefix for PAR and REC files.
        """
        self.experiment_path = experiment_path
        self.par_file = experiment_path / (filename + '.par')
        self.rec_file = experiment_path / (filename + '.rec')
        self.parameters: MRIExperiment_Philips
        self.data: Recread

    def load(self) -> None:
        """Load experiment parameters and data from the PAR, REC files."""
        self.parameters = MRIExperiment_Philips(**Parread(self.par_file).read())
        self.data = Recread(self.rec_file).read()

        self.removing_unwanted_zeros()
        self.resize_data()

    def describe(self) -> None:
        description = "Experiment Details:\n"
        description += f"- Type: {self.parameters.SeriesDataType}\n"
        description += f"- Date: {datetime.strptime(self.parameters.ExaminationDateTime, '%Y.%m.%d / %H:%M:%S').strftime('%B %d, %Y')}\n\n"

        description += "Scan Information:\n"
        dimension = "3D" if '3D' in self.parameters.SeriesDataType else "2D"
        description += f"- Technique: {self.parameters.Technique}\n"
        description += f"- Dimension: {dimension}\n"
        description += f"- Resolution: {self.parameters.ScanResolution[0]}x{self.parameters.ScanResolution[1]} pixels\n"
        description += f"- Slices: {self.parameters.MaxNumberOfSlicesLocations}\n"
        description += f"- Dynamics: {self.parameters.MaxNumberOfDynamics if self.parameters.MaxNumberOfDynamics > 1 else 'None'}\n"
        description += f"- Flow Encoding: {'Yes' if self.parameters.PhaseEncodingVelocity else 'No'}\n"
        description += f"- Diffusion Encoding: {'Yes' if self.parameters.Diffusion else 'No'}\n"

        print(description)
        return

    
    def resize_data(self) -> None:
        """Resize the loaded data."""
        target_shape = (self.data.shape[0],self.data.shape[1], self.parameters.MaxNumberOfSlicesLocations, self.parameters.MaxNumberOfDynamics)
        self.data = np.reshape(self.data, target_shape)

    def removing_unwanted_zeros(self) -> None:
        non_zero_indices = np.nonzero(self.data)

        min_index = np.min(non_zero_indices, axis=1)
        max_index = np.max(non_zero_indices, axis=1)

        cropped_data = self.data[min_index[0]:max_index[0]+1, min_index[1]:max_index[1]+1, min_index[2]:max_index[2]+1]
        self.data = cropped_data
        return

    def plot_proton_density(self) -> px.imshow:
        """Generate and return plots for proton density data."""

        flipped_data = np.transpose(self.data, axes=(1, 0, 2,3))
        print(flipped_data.shape)

        fig = px.imshow(flipped_data[:,:,0,0], color_continuous_scale="gray")
        fig.update_layout(
            xaxis=dict(
                title='x-axis',
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,
                showticklabels=True,  # Ensure tick labels are shown
                tickcolor='black',  # Set tick color
                ticks='outside',  # Place ticks outside the plot area
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
            yaxis=dict(
                title='y-axis',
                showline=True,
                linecolor='black',
                linewidth=2, 
                mirror=True,
                showticklabels=True,  # Ensure tick labels are shown
                tickcolor='black',  # Set tick color
                ticks='outside',  # Place ticks outside the plot area
                ticklen=6,
                tickwidth=1.5,
                tickfont=dict(size=16),
            ),
            coloraxis_colorbar=dict(
                thickness=20,
                len=0.50,
                tickfont=dict(size=16),
                tickcolor='black',
                ticklen=6,
                tickwidth=1.5,
                tickmode='array',
                ticks='outside',
                outlinecolor='black',  # Add border color
                outlinewidth=1.1,  # Add border width
            ),
            width=500,
            height=500,
            font=dict(
                size=16,
            ),
        )
        return fig