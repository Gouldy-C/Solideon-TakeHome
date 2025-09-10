import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type Group, type GroupMetrics, type Layer } from "../lib/types";

export function useGroups(
  options?: {
    staleTime?: number;
    refetchInterval?: number;
    refetchIntervalInBackground?: boolean;
  }
) {
  return useQuery({
    queryKey: ["groups"],
    queryFn: async () => {
      const { data } = await api.get<Group[]>("/groups");
      return data;
    },
    staleTime: 60_000,
    refetchInterval: 30_000,
    refetchIntervalInBackground: false,
    ...options,
  });
}

export function useGroup(groupId?: string) {
  return useQuery({
    queryKey: ["group", groupId],
    queryFn: async () => {
      const { data } = await api.get(`/groups/${groupId}`);
      return data as { group: Group; layers: Layer[] } | Group;
    },
    enabled: !!groupId,
  });
}

export function useGroupMetrics(groupId?: string) {
  return useQuery({
    queryKey: ["groupMetrics", groupId],
    queryFn: async () => {
      const { data } = await api.get(`/groups/${groupId}/metrics`);
      return data as GroupMetrics;
    },
    enabled: !!groupId,
  });
}