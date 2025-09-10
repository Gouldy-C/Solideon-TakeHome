import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type Layer } from "../lib/types";

export function useLayer(layerId?: string) {
  return useQuery({
    queryKey: ["layer", layerId],
    queryFn: async () => {
      const { data } = await api.get<Layer>(`/layers/${layerId}`);
      return data;
    },
    enabled: !!layerId,
  });
}