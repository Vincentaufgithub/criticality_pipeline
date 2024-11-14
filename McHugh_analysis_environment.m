addpath('/home/dekorvyb/Documents/criticality_pipeline/MatlabImportExport_v6.0.0');

% Define the file you want to process
nttFilePath = '/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/181-1223/181-1232/DAY07_2016-09-01_12-02-01/TT2.ntt';


% Define the FieldSelectionFlags to specify what data to extract
% Example: [1 1 1 1 1] to extract Timestamps, ScNumbers, CellNumbers, Features, and Samples
FieldSelectionFlags = [1 1 1 1 1];

% Set HeaderExtractionFlag to 1 to extract header information
HeaderExtractionFlag = 1;

% Use ExtractionMode 1 (Extract All Records)
ExtractionMode = 1;

% ExtractionModeVector is not needed for ExtractionMode 1, so it's empty
ExtractionModeVector = [];

% Call the function to extract the spike data
[Timestamps, ScNumbers, CellNumbers, Features, Samples, Header] = ...
    Nlx2MatSpike(nttFilePath, FieldSelectionFlags, HeaderExtractionFlag, ExtractionMode, ExtractionModeVector);

% Display the spike timestamps (example)
disp(Timestamps);

