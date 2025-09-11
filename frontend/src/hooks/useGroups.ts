import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { type Group, type GroupData } from "../lib/types";

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
      const { data }: { data: Group[] } = await api.get("/groups");
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
      const { data }: { data: Group } = await api.get(`/groups/${groupId}`);
      return data;
    },
    enabled: !!groupId,
  });
}

export function useGroupData(groupId?: string) {
  return useQuery({
    queryKey: ["groupMetrics", groupId],
    queryFn: async () => {
      const { data } : { data: GroupData } = await api.get(`/groups/${groupId}/data`);
      return data;
    },
    enabled: !!groupId,
  });
}