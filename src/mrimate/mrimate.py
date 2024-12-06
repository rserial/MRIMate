"""Main module."""

from parrec.recread import Recread
from parrec.parread import Parread
from pathlib import Path
import numpy as np
from rich import print
from mrimate.models import MRIExperiment_Philips
from mrimate.plot import plot_2d_data, plot_2d_slider
import plotly.graph_objects as go
from typing import Optional
import h5py

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
        self.data: np.ndarray = None
        self.spin_density: np.ndarray = None
        self.phase: np.ndarray = None
        self.velocity: np.ndarray = None
        self.data_loaded = False


    def load(self) -> None:
        """Load experiment parameters and data from the PAR, REC files."""
        self.parameters = MRIExperiment_Philips(**Parread(self.par_file).read())
        self.data = Recread(self.rec_file).read()

        self.removing_unwanted_zeros()
        self.resize_data()
        self.data_loaded = True

    def describe(self) -> None:
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")
        if hasattr(self.parameters, 'describe'):
            self.parameters.describe()

    def display_parameters(self)-> None:
        """Display model parameters"""
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")
        if hasattr(self.parameters, 'display_parameters'):
            self.parameters.display_parameters()
            
    def resize_data(self) -> None:
        """Resize the loaded data."""
        if self.parameters.is_flow_encoded():
            target_shape = (self.data.shape[0],self.data.shape[1], self.parameters.NumberOfSlices, self.parameters.NumberOfDynamics*2)
            self.data = np.reshape(self.data, target_shape)
            self.spin_density =  self.data[:, :, :, 0::2]#only for 1d velocity encoded
            phase_integer =  self.data[:, :, :, 1::2]#only for 1d velocity encoded
            self.phase = (phase_integer-4096/2)/(4096/2)*np.pi

        elif self.parameters.MaxNumberOfEchoes > 1:
            target_shape = (self.data.shape[0],self.data.shape[1], self.parameters.NumberOfSlices, self.parameters.MaxNumberOfEchoes)
            self.data = np.reshape(self.data, target_shape)
            self.spin_density = self.data            
        else:
            target_shape = (self.data.shape[0],self.data.shape[1], self.parameters.NumberOfSlices, self.parameters.NumberOfDynamics)
            self.data = np.reshape(self.data, target_shape)
            self.spin_density = self.data

    def removing_unwanted_zeros(self) -> None:
      
        non_zero_indices = np.nonzero(self.data)
        min_index = np.min(non_zero_indices, axis=1)
        max_index = np.max(non_zero_indices, axis=1)

        cropped_data = self.data[min_index[0]:max_index[0]+1, min_index[1]:max_index[1]+1, min_index[2]:max_index[2]+1]
        self.spin_density = cropped_data
        return

    def plot_proton_density(self, 
                            plot_type, 
                            slice_idx=None,
                            title='Proton Density',  
                            dynamic_idx=None,
                            color_continuous_scale='gray',
                            colorbar_title_text = "Intensity",  
                            interval=1,
                            rotate_xy_axes=False,
                            zmin=None,
                            zmax=None)  -> go.Figure:
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")
        fig = plot_2d_slider(self.spin_density, 
                                  plot_type=plot_type, 
                                  slice_idx=slice_idx, 
                                  dynamic_idx=dynamic_idx, 
                                  title=title, 
                                  color_continuous_scale=color_continuous_scale,
                                  colorbar_title_text=colorbar_title_text, 
                                  interval=interval,
                                  rotate_xy_axes=rotate_xy_axes,
                                  zmin = zmin,
                                  zmax = zmax
                                  )
        return fig
    
    def plot_velocity(self, 
                            plot_type, 
                            slice_idx=None, 
                            title='Velocity',  
                            dynamic_idx=None,
                            color_continuous_scale='RdBu',
                            colorbar_title_text = "Velocity [cm/s]",  
                            interval=1,
                            rotate_xy_axes=False,
                            zmin = None,
                            zmax = None)  -> go.Figure:
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")

        fig = plot_2d_slider(self.velocity, 
                                  plot_type=plot_type, 
                                  slice_idx=slice_idx, 
                                  dynamic_idx=dynamic_idx, 
                                  title=title, 
                                  color_continuous_scale=color_continuous_scale,
                                  colorbar_title_text=colorbar_title_text, 
                                  interval=interval,
                                  rotate_xy_axes=rotate_xy_axes,
                                  zmin = zmin,
                                  zmax = zmax
                                  )
        return fig
    
    def get_spin_density(self) -> Optional[np.ndarray]:
        """Safely access the spin_density attribute."""
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")

        if self.spin_density is None:
            raise ValueError("Spin density is not available. Ensure data is loaded and processed.")
        return self.spin_density

    def get_phase(self) -> Optional[np.ndarray]:
        """Safely access the phase attribute."""
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")

        if self.phase is None:
            raise ValueError("Phase data is not available. Ensure velocity encoding is present.")
        return self.phase
    
    def get_velocity(self) -> Optional[np.ndarray]:
        """Safely access the phase attribute."""
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")
        if self.phase is None:
            raise ValueError("Phase data is not available. Ensure velocity encoding is present.")

        if self.velocity is None:
            raise ValueError("Velocity data is not available. Call calculate_velocity() first.")  
        return self.velocity

    def calculate_velocity(self) -> Optional[np.ndarray]:
        if not self.data_loaded:
            raise ValueError("Data not loaded. Call 'load()' method first.")
        if self.parameters.is_flow_encoded():
            self.velocity = self.phase*self.parameters.MaxEncodedVelocity/np.pi #so far only valid for 1d velocity
        else:
            raise ValueError("Phase data is not available. Ensure velocity encoding is present.")

    def export_to_hdf5(self, filepath: Path, filename: str) -> None:
        """
        Export the MRI experiment data to an HDF5 file.

        Args:
            filepath (Path): Path directory where to save the hdf5 file.
            filename (str): The name of the HDF5 file to save.
        """
        if not self.data_loaded:
            print("Data not loaded. Call 'load()' method first.")
            return

        with h5py.File(filepath / filename, 'w') as hdf:
            # Save spin_density
            hdf.create_dataset('spin_density', data=self.get_spin_density())
            
            # Save phase
            if self.phase is not None:
                hdf.create_dataset('phase', data=self.get_phase())

            if self.velocity is not None:
            # Save velocity
                hdf.create_dataset('velocity', data=self.get_velocity())
            
            print(f"Data exported to {filename} successfully.")