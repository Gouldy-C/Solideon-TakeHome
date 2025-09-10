import { useMemo, useState } from "react";
import { useGroups } from "../../hooks/useGroups";
import { Link } from "@tanstack/react-router";
import { Button } from "../ui/button";
import { Card } from "../ui/card";
import { Input } from "../ui/input";

export default function GroupsPage() {
  const { data: groups, isLoading, error, refetch } = useGroups();
  const [query, setQuery] = useState("");

  const filteredGroups = useMemo(() => {
    if (!groups) return [];
    const q = query.trim().toLowerCase();
    if (!q) return groups;
    return groups.filter((g) => g.name?.toLowerCase().includes(q));
  }, [groups, query]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search groups…"
          aria-label="Search groups"
        />
        <div className="ml-auto">
          <Button onClick={() => refetch()} disabled={isLoading}>
            Refresh
          </Button>
        </div>
      </div>

      {isLoading && <div className="text-slate-400">Loading…</div>}

      {error && (
        <div className="text-red-400">
          {(error as Error).message}{" "}
          <Button className="underline" onClick={() => refetch()}>
            Retry
          </Button>
        </div>
      )}

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
        {!isLoading && !error && groups && filteredGroups.length === 0 && (
          <div className="text-xl">No groups found</div>
        )}

        {filteredGroups.map((g) => (
          <Link key={g.id} to={`/group/$groupId`} params={{ groupId: g.id }}>
            <Card className="p-4">
              <div className="text-lg">{g.name}</div>
              <div className="flex items-center gap-5 text-sm justify-between">
                <div>Layers: {g.layer_count ?? "—"}</div>
                {g.ingest_complete === false ? (
                  <div className="rounded bg-chart-3/10 px-2 py-1 text-chart-3">
                    Ingesting
                  </div>
                ) : (
                  <div className="rounded bg-chart-2/10 px-2 py-1 text-chart-2">
                    Ingested
                  </div>
                )}
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}