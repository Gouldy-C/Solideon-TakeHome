import { Link } from "@tanstack/react-router";
import { ThemeToggle } from "../ui/ThemeToggle";
import { Button } from "../ui/button";
import UploadZipModal from "../UploadZipModal";
import { useState } from "react";


export function TopBar() {
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <div className="flex h-14 items-center justify-between gap-3 border-b px-4">
      <div className="flex gap-3 items-center">

        <Link to="/" className="font-semibold">
          All Groups
        </Link>
      </div>
      <div className="text-lg font-semibold">
        AM Spatial Sensing Analytics Dashboard
      </div>
      <div className="flex items-center gap-3">
        <Button variant="outline" size="sm" onClick={() => setModalOpen(true)}>
          Upload Data Zip
        </Button>
        <ThemeToggle />
      </div>
      < UploadZipModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </div>
  );
}
