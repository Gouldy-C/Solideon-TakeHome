import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef, useState } from "react";
import { api } from "../lib/api";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card } from "./ui/card";

export default function UploadZipModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const qc = useQueryClient();
  const [groupName, setGroupName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { mutate, isPending, error, reset } = useMutation({
    mutationFn: async ({
      file,
      groupName,
    }: {
      file: File;
      groupName: string;
    }) => {
      const form = new FormData();
      form.append("zip_file", file);
      form.append("group_name", groupName);
      return api.post("/ingest/upload-zip", form);
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["groups"] });
      setGroupName("");
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
      onClose();
    },
  });

  if (!open) return null;

  const canUpload = !!file && groupName.trim().length > 0 && !isPending;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/50">
      <Card className="p-4 gap-5 min-w-[380px]">
        <div className="text-lg font-semibold">Upload Weld Group (.zip)</div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (file && groupName.trim()) {
              mutate({ file, groupName: groupName.trim() });
            }
          }}
          className="space-y-3">
          <div className="space-y-1">
            <label className="block text-sm">Group name</label>
            <Input
              type="text"
              value={groupName}
              onChange={(e) => setGroupName(e.target.value)}
              placeholder="e.g., weld-batch-42"
              disabled={isPending}
              className=""
            />
          </div>

          <div className="space-y-1">
            <label className="block text-sm">ZIP file</label>
            <Input
              ref={fileInputRef}
              type="file"
              accept=".zip"
              disabled={isPending}
              onChange={(e) => {
                const f = e.target.files?.[0] ?? null;
                setFile(f);
              }}
              className="
                w-full overflow-hidden whitespace-nowrap text-ellipsis p-0 m-0

                /* Button (Browse) */
                file:mr-3 file:px-3 file:rounded-l-md file:font-semibold file:text-md
                file:bg-primary file:text-primary-foreground hover:file:bg-primary/90
                file:h-full file:items-center
              "
            />
          </div>

          {error && (
            <div className="text-sm text-red-400">
              {(error as Error).message}
            </div>
          )}

          <div className="mt-5 flex justify-end gap-4">
            <Button
              type="button"
              className=""
              onClick={() => {
                if (isPending) return;
                setGroupName("");
                setFile(null);
                if (fileInputRef.current) fileInputRef.current.value = "";
                reset();
                onClose();
              }}
              disabled={isPending}>
              Cancel
            </Button>
            <Button type="submit" className="" disabled={!canUpload}>
              {isPending ? "Uploading…" : "Upload"}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
