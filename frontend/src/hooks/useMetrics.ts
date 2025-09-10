import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type LayerMetrics } from "../lib/types";

export function useLayerMetrics(layerId?: string) {
  return useQuery({
    queryKey: ["layerMetrics", layerId],
    queryFn: async () => {
      const { data } = await api.get<LayerMetrics>(
        `/layers/${layerId}/metrics`
      );
      return data;
    },
    enabled: !!layerId,
  });
}