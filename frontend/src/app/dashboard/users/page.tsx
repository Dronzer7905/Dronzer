"use client"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus, Shield, User } from "lucide-react"

const users = [
  { id: "usr-1", name: "Alice Admin", email: "alice@dronzer.ai", role: "SUPER_ADMIN", status: "active" },
  { id: "usr-2", name: "Bob Builder", email: "bob@acme.com", role: "PROJECT_ADMIN", status: "active" },
  { id: "usr-3", name: "Charlie Coder", email: "charlie@acme.com", role: "DEVELOPER", status: "invited" },
]

export default function UsersPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Users & RBAC</h2>
          <p className="text-muted-foreground">
            Manage user access, roles, and platform invitations.
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" /> Invite User
        </Button>
      </div>

      <div className="grid gap-4">
        {users.map((u) => (
          <Card key={u.id}>
            <CardContent className="flex items-center justify-between p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary">
                  <User className="h-5 w-5 text-muted-foreground" />
                </div>
                <div>
                  <h3 className="font-semibold">{u.name}</h3>
                  <p className="text-sm text-muted-foreground">{u.email}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2 px-2 py-1 bg-muted rounded text-xs font-medium border">
                  <Shield className="h-3 w-3" />
                  {u.role}
                </div>
                
                {u.status === "active" ? (
                  <div className="text-green-500 text-sm font-medium">Active</div>
                ) : (
                  <div className="text-yellow-500 text-sm font-medium">Pending Invite</div>
                )}
                
                <Button variant="ghost" size="sm">Manage</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
