import { createRootRoute, Outlet } from '@tanstack/react-router'
import { TopBar } from "../components/layouts/TopBar";


function RootLayout() {
  

  return (
    <div className="flex h-screen flex-col">
      <TopBar/>
      <div className="flex-1 overflow-hidden p-4">
        <Outlet/>
      </div>
    </div>
  );
}

export const Route = createRootRoute({ component: RootLayout })