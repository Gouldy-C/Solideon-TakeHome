import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import type { LayerData, Waypoint } from "./types"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}


export function getWaypoints(layer_data: LayerData) : Waypoint[] {
  const waypoints = [] 
  console.log(layer_data)
  for (let i = 0; i < layer_data.weld_data.length; i++) {
    waypoints.push({
      seq: layer_data.weld_data[i].seq,
      x: layer_data.weld_data[i].x,
      y: layer_data.weld_data[i].y,
      z: layer_data.weld_data[i].z
    })
  }
  return waypoints
}