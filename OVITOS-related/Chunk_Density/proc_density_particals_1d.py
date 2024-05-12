from ovito.io import import_file, export_file
from ovito.modifiers import *
import numpy

iname = "test"
# import multi-frames of extxyz
pip1 = import_file(f"../{iname}.xyz")
# labeled a 'Unity' for each atoms with the value '1'
pip1.modifiers.append(ComputePropertyModifier(
    expressions=['1'], output_property='Unity'))
# chunk box in 'z' direction
pip1.modifiers.append(SpatialBinningModifier(
    property = 'Unity',
    direction = SpatialBinningModifier.Direction.Z, 
    bin_count = 118,
    reduction_operation = SpatialBinningModifier.Operation.SumVol
))
# Time averaging
pip1.modifiers.append(TimeAveragingModifier(
    operate_on='table:binning'))
TimeAveragingModifier.interval = (pip1.source.num_frames//2,
    pip1.source.num_frames-1)

data = pip1.compute()
# print(data.tables['binning[average]'].xy())
# export data.
export_file(pip1, f'density-{iname}.dat', 'txt/table', key='binning')
