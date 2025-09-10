import GroupsPage from "@/components/pages/GroupsPage";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Home,
});

function Home() {
  return <GroupsPage />;
}
