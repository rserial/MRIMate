from pydantic import BaseModel, Field
from typing import Tuple, List, Union

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
    ImageAngulation: Tuple[float,float,float] #(ap,fh,rl in degrees)
    ImageOffcentre: Tuple[float,float,float] #(ap,fh,rl in mm) 
    SliceThickness: float #in mm
    SliceGap: float #in mm
    ImageDisplayOrientation: int
    SliceOrientation: int
    FmriStatusIndication: int
    ImageTypeEdEs: int
    PixelSpacing: Tuple[float, float] #in mm
    EchoTime: float
    DynScanBeginTime: float
    TriggerTime: float
    DiffusionBFactor: float
    NumberOfAverages: int
    ImageFlipAngle: float # in degrees
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
    PhaseEncodingVelocity: Tuple[float, float, float]#cm/s
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
