"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useCreateModel } from "@/lib/hooks/use-models";
import { useProviders } from "@/lib/hooks/use-providers";

export function AddModelModal() {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [providerId, setProviderId] = useState("");
  const [contextWindow, setContextWindow] = useState("8192");

  const createModel = useCreateModel();
  const { data: providers } = useProviders();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    createModel.mutate(
      {
        name,
        provider_id: providerId,
        context_window: parseInt(contextWindow, 10) || 8192,
      },
      {
        onSuccess: () => {
          setOpen(false);
          setName("");
          setProviderId("");
          setContextWindow("8192");
        },
      }
    );
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <Plus className="w-4 h-4" />
          Add Model
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Add New Model</DialogTitle>
            <DialogDescription>
              Register a new model with its provider and context window limit.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <label htmlFor="name" className="text-sm font-medium leading-none text-text-primary">
                Model Name
              </label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. llama-3.3-70b-versatile"
                required
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="providerId" className="text-sm font-medium leading-none text-text-primary">
                Provider
              </label>
              <div className="relative">
                <select
                  id="providerId"
                  value={providerId}
                  onChange={(e) => setProviderId(e.target.value)}
                  className="input-field h-10 w-full appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat pl-3 pr-10"
                  required
                >
                  <option value="" disabled>Select a provider</option>
                  {providers?.map((p) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="space-y-2">
              <label htmlFor="contextWindow" className="text-sm font-medium leading-none text-text-primary">
                Context Window
              </label>
              <Input
                id="contextWindow"
                type="number"
                min="1"
                value={contextWindow}
                onChange={(e) => setContextWindow(e.target.value)}
                required
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={createModel.isPending || !name || !providerId}>
              {createModel.isPending ? "Adding..." : "Add Model"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
