import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type Waypoint } from "../lib/types";

export function useWaypoints(layerId?: string) {
  return useQuery({
    queryKey: ["waypoints", layerId],
    queryFn: async () => {
      const { data } = await api.get<Waypoint[]>(
        `/layers/${layerId}/waypoints`
      );
      return data;
    },
    enabled: !!layerId,
  });
}