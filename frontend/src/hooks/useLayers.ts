import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type Layer, type LayerData } from "../lib/types";

export function useLayer(layerId?: string) {
  return useQuery({
    queryKey: ["layer_id", layerId],
    queryFn: async () => {
      const { data } = await api.get<Layer>(`/layers/${layerId}`);
      return data;
    },
    enabled: !!layerId,
  });
}

export function useLayerData(layerId?: string) {
  return useQuery({
    queryKey: ["layerData", layerId],
    queryFn: async () => {
      const { data } = await api.get<LayerData>(`/layers/${layerId}/data`);
      return data;
    },
    enabled: !!layerId,
  });
}
