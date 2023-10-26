from . import FlightPlan as Fp, GeoSolver
import math, numpy as np

def RenderWorld(LatRes : int = 20, LonRes : int = 20) -> dict[str : np.ndarray]:
  output : dict[str:np.ndarray] = {}
  u = np.linspace(0, 2 * np.pi, LonRes)
  v = np.linspace(0, np.pi, LatRes)
  output['X'] = GeoSolver.EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
  output['Y'] = GeoSolver.EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
  output['Z'] = GeoSolver.EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
  return output


def RenderGamaFpl(GamaFpl : list[Fp.GamaWaypoints.GamaFplWaypoint]) -> dict[str : np.ndarray]:
  output : dict[str:np.ndarray] = {}
  output['X'] = np.ndarray(shape=(1,1))
  output['Y'] = np.ndarray(shape=(1,1))
  output['Z'] = np.ndarray(shape=(1,1))
  if len(GamaFpl) == 1:
    output['X'][0] = GamaFpl[0].X
    output['Y'][0] = GamaFpl[0].Y
    output['Z'][0] = GamaFpl[0].Z
    return output
  for index in range(0, len(GamaFpl)):
    if index == 0:
      output['X'] = GamaFpl[index].X
      output['Y'] = GamaFpl[index].Y
      output['Z'] = GamaFpl[index].Z
      continue
    output['X'] = np.append(output['X'],GamaFpl[index].X)
    output['Y'] = np.append(output['Y'],GamaFpl[index].Y)
    output['Z'] = np.append(output['Z'],GamaFpl[index].Z)
  return output
  