import { useEffect, useMemo, useState } from "react";
import { Card } from "..//ui/card";
import { Button } from "..//ui/button";
import { Badge } from "..//ui/badge";
import { Separator } from "..//ui/separator";

import { useGroup } from "../../hooks/useGroups";
import { useLayer, useLayerData } from "../../hooks/useLayers";

import { LayerComboBox } from "../layouts/LayerComboBox";
import { LayerScene3D } from "../layouts/LayerScene3D";
import { LayerMetricsChart } from "../layouts/LayerMetricsChart";

import type { Group, Layer } from "../../lib/types";
import { getWaypoints } from "@/lib/utils";

type Props = {
  groupId: string;
};

export default function GroupPage(props: Props) {
  const { groupId } = props;

  const {
    data: groupData,
    isLoading: groupLoading,
    error: groupError,
    refetch: refetchGroup,
  } = useGroup(groupId);

  const group = useMemo(() => {
    if (!groupData) return undefined as Group | undefined;
    const gAny = groupData;
    return ("group" in gAny ? gAny.group : gAny) as Group;
  }, [groupData]);

  const layers = useMemo(() => {
    if (!groupData) return [] as Layer[];
    const gAny = groupData;
    if ("layers" in gAny && Array.isArray(gAny.layers)) {
      return gAny.layers as Layer[];
    }
    if ("group" in gAny && Array.isArray(gAny.layers)) {
      return gAny.layers as Layer[];
    }
    return (groupData as Group)?.layers ?? [];
  }, [groupData]);

  const [selectedLayerId, setSelectedLayerId] = useState<
    string | undefined
  >(undefined);

  useEffect(() => {
    if (!layers?.length) {
      setSelectedLayerId(undefined);
      return;
    }
    if (!selectedLayerId || !layers.find((l: Layer) => l.id === selectedLayerId)) {
      setSelectedLayerId(layers[0].id);
    }
  }, [groupId, layers, selectedLayerId]);

  const {
    data: currentLayer,
    isLoading: layerLoading,
    error: layerError,
    refetch: refetchLayer,
  } = useLayer(selectedLayerId);

  const {
    data: layerData,
    isLoading: layerDataLoading,
    error: layerDataError,
    refetch: refetchLayerData,
  } = useLayerData(selectedLayerId);

  const refreshAll = () => {
    refetchGroup();
    refetchLayer();
    refetchLayerData();
  };
  

  const layerLabel = useMemo(() => {
    const n = currentLayer ?.layer_number;
    return typeof n === "number" ? `Layer ${n}` : "Layer";
  }, [currentLayer]);


  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="text-2xl font-semibold">{group?.name ?? "Group"}</div>
        <div className="ml-auto">
          <Button variant="outline" onClick={refreshAll}>
            Refresh
          </Button>
        </div>
      </div>

      <Card className="p-4">
        {groupLoading && <div className="text-slate-400">Loading group…</div>}
        {groupError && (
          <div className="text-red-400">{(groupError as Error).message}</div>
        )}
        {group && (
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-3">
              <div className="text-xl font-medium">{group.name}</div>
              {"ingest_complete" in group && (
                <Badge
                  variant="outline"
                  className={
                    group.ingest_complete
                      ? "bg-green-500/20 text-green-300"
                      : "bg-amber-500/20 text-amber-300"
                  }
                >
                  {group.ingest_complete ? "Ingested" : "Ingesting…"}
                </Badge>
              )}
              <Badge variant="outline">
                Layers: {layers.length || group.layer_count || 0}
              </Badge>
              {"id" in group && (
                <Badge variant="outline">ID: {group.id}</Badge>
              )}
            </div>
          </div>
        )}
      </Card>

      <LayerComboBox
        layers={layers}
        selectedLayerId={selectedLayerId}
        onChange={setSelectedLayerId}
        disabled={!layers?.length}
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card className="p-3">
          <div className="mb-2 flex items-center justify-between">
            <div className="font-medium">
              3D Layer View {currentLayer ? `• ${layerLabel}` : ""}
            </div>
            {(layerDataLoading || layerLoading) && (
              <div className="text-xs text-slate-400">Loading…</div>
            )}
          </div>
          <Separator className="mb-3" />
          {layerError && (
            <div className="text-red-400">{(layerError as Error).message}</div>
          )}
          {layerDataError && (
            <div className="text-red-400">
              {(layerDataError as Error).message}
            </div>
          )}
          <div className="h-[420px] w-full overflow-hidden rounded-md bg-slate-900">
            {layerData && <LayerScene3D waypoints={getWaypoints(layerData) ?? []} pointRadius={10} lineWidth={12} />}
          </div>
        </Card>

        <Card className="p-3">
          <div className="mb-2 flex items-center justify-between">
            <div className="font-medium">
              Layer Metrics {currentLayer ? `• ${layerLabel}` : ""}
            </div>
            {layerDataLoading && (
              <div className="text-xs text-slate-400">Loading…</div>
            )}
          </div>
          <Separator className="mb-3" />
          {layerDataError && (
            <div className="text-red-400">
              {(layerDataError as Error).message}
            </div>
          )}
          <div className="h-[420px] w-full">
            <LayerMetricsChart metrics={layerData?.weld_data} />
          </div>
        </Card>
      </div>
    </div>
  );
}