import GroupPage from '@/components/pages/GroupPage'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/group/$groupId')({
  component: RouteComponent,
})

function RouteComponent() {
  const { groupId } = Route.useParams()
  return (
    <div>
      <GroupPage groupId={groupId} />
    </div>
  )
}
