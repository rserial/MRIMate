from pydantic import BaseModel, Field
from typing import Tuple, List, Union, Any
from datetime import datetime
from rich import print
import numpy as np

class ImageInformation_Philips(BaseModel):
    SliceNumber: int = Field(..., description="The number of imaged slices", unit= None)
    EchoNumber: int = Field(..., description="Number of acquired echoes", unit= None)
    DynamicScanNumber: int = Field(..., description="Number of acquired dynamic images", unit= None)
    CardiacPhaseNumber: int = Field(..., description="Number of cardiac phases", unit= None)
    ImageTypeMr: int
    ScanningSequence: int
    IndexInRecFile: int
    ImagePixelSize: int
    ScanPercentage: int
    ReconResolution: Tuple[int,int]
    RescaleIntercept: float
    RescaleSlope: float
    WindowCenter: int
    WindowWidth: int
    ImageAngulation: Tuple[float,float,float] = Field(..., description="Angulation of the image along the three directions (ap,fh,rl)", unit= "degrees")
    ImageOffcentre: Tuple[float,float,float] = Field(..., description="Off centre position of the image along the three directions (ap,fh,rl)", unit= "mm") 
    SliceThickness: float = Field(..., description="Slice thickmess", unit= "mm") 
    SliceGap: float = Field(..., description="Gap between slices", unit= "mm") 
    ImageDisplayOrientation: int
    SliceOrientation: int
    FmriStatusIndication: int
    ImageTypeEdEs: int
    PixelSpacing: Tuple[float, float] #in mm
    EchoTime: float = Field(..., description="Echo time", unit= "ms") 
    DynScanBeginTime: float
    TriggerTime: float
    DiffusionBFactor: float
    NumberOfAverages: int
    ImageFlipAngle: float = Field(..., description="Excitation RF flip angle", unit= "degrees") 
    CardiacFrequency: int #bpm
    MinimumRrInterval: int # in ms 
    MaximumRrInterval: int # in ms
    TurboFactor: int #<0=no turbo>  
    InversionDelay: float # in ms
    DiffusionBValueNumber: int #(imagekey!)
    GradientOrientationNumber: int #(imagekey!) 
    ContrastType: str
    DiffusionAnisotropyType: str
    Diffusion: Tuple[float,float,float] #(ap, fh, rl)
    LabelType: int # (ASL)(imagekey!)

class MRIExperiment_Philips(BaseModel):
    PatientName: Union[int,str] = Field(..., description="Name of the patient")
    ExaminationName: Union[int,str]
    ProtocolName: str
    ExaminationDateTime: str
    SeriesDataType: str
    AcquisitionNr: int
    ReconstructionNr: int
    ScanDuration: float #s
    MaxNumberOfCardiacPhases: int
    MaxNumberOfEchoes: int
    MaxNumberOfSlicesLocations: int
    MaxNumberOfDynamics: int
    MaxNumberOfMixes: int
    PatientPosition: str
    PreparationDirection: str
    Technique: str
    ScanResolution: List[int]
    ScanMode: str
    RepetitionTime: float #ms
    Fov: Tuple[float, float, float]#mm
    WaterFatShift: float
    AngulationMidslice: Tuple[float, float, float]
    OffCentreMidslice: Tuple[float, float, float]
    FlowCompensation: int
    Presaturation: int
    PhaseEncodingVelocity: Tuple[float, float, float] = Field(..., description="Maximum encoded velocity", unit= "cm/s") 
    Mtc: int
    Spir: int
    EpiFactor: int
    DynamicScan: int
    Diffusion: int
    DiffusionEchoTime: float
    MaxNumberOfDiffusionValues: int
    MaxNumberOfGradientOrients: int
    NumberOfLabelTypes: int
    ImageInformation: List[ImageInformation_Philips]

    def describe(self) -> None:
        description = "Experiment Details:\n"
        description += f"- Examination Name: {self.ExaminationName}\n"
        description += f"- Type: {self.ScanMode}\n"
        description += f"- Date: {datetime.strptime(self.ExaminationDateTime, '%Y.%m.%d / %H:%M:%S').strftime('%B %d, %Y')}\n\n"

        description += "Scan Information:\n"
        dimension = "3D" if '3D' in self.ScanMode else "2D"
        description += f"- Technique: {self.Technique}\n"
        description += f"- Dimension: {dimension}\n"
        description += f"- Resolution: {self.ScanResolution[0]}x{self.ScanResolution[1]} pixels\n"
        description += f"- Slices: {self.MaxNumberOfSlicesLocations}\n"
        description += f"- Dynamics: {self.MaxNumberOfDynamics if self.MaxNumberOfDynamics > 1 else 'None'}\n"
        description += f"- Flow Encoding: {'Yes' if self.PhaseEncodingVelocity != (0.0, 0.0, 0.0) else 'No'}\n"
        description += f"- Diffusion Encoding: {'Yes' if self.Diffusion else 'No'}\n"

        print(description)
        return
    
    def display_parameters(self) -> None:
        """Display model parameters with a customized ImageInformation field."""
        
        # Create a copy of self to modify
        model_for_display = self.model_copy()

        # Customize the ImageInformation field for display
        if len(model_for_display.ImageInformation) > 1:
            print("Note: The ImageInformation list contains more than one item. Displaying only last dynamic")
            model_for_display.ImageInformation = [
                model_for_display.ImageInformation[-1]
            ]
        
        # Print the modified model
        print(model_for_display)

    # def display_field_info(self, field_name: str) -> None:
    #     """Display the description and unit information for a given field."""
    #     field_info = self.model_fields.get(field_name)

    #     if field_info:
    #         description = field_info.description
    #         unit = field_info.extra.get('unit')
            
    #         print(f"[bold cyan]{field_name}[/bold cyan]:")
    #         if description:
    #             print(f"  [bold]Description:[/bold] {description}")
    #         if unit:
    #             print(f"  [bold]Unit:[/bold] {unit}")
    #     else:
    #         print(f"[bold red]Field '{field_name}' not found.[/bold red]")

    def is_flow_encoded(self) -> bool:
        """Check if PhaseEncodingVelocity is non-zero."""
        return self.PhaseEncodingVelocity != (0.0, 0.0, 0.0)
    
    @property
    def NumberOfSlices(self) -> int:
        # Return the specific value for Philips
        return self.MaxNumberOfSlicesLocations
    
    @property
    def NumberOfDynamics(self) -> int:
        return self.MaxNumberOfDynamics

    @property
    def MaxEncodedVelocity(self) -> float:
        return np.linalg.norm(self.PhaseEncodingVelocity)
