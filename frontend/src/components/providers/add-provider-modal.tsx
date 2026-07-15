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
import { useCreateProvider } from "@/lib/hooks/use-providers";

export function AddProviderModal() {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [priority, setPriority] = useState("1");
  const [weight, setWeight] = useState("1");
  const [models, setModels] = useState("");

  const createProvider = useCreateProvider();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    createProvider.mutate(
      {
        name,
        priority: parseInt(priority, 10) || 1,
        weight: parseInt(weight, 10) || 1,
        models: models ? models.split(",").map((m) => m.trim()).filter(Boolean) : [],
      },
      {
        onSuccess: () => {
          setOpen(false);
          setName("");
          setPriority("1");
          setWeight("1");
          setModels("");
        },
      }
    );
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <Plus className="w-4 h-4" />
          Add Provider
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Add New Provider</DialogTitle>
            <DialogDescription>
              Configure a new LLM provider for the gateway.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <label htmlFor="name" className="text-sm font-medium leading-none text-text-primary">
                Provider Name
              </label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. openai, anthropic"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label htmlFor="priority" className="text-sm font-medium leading-none text-text-primary">
                  Priority
                </label>
                <Input
                  id="priority"
                  type="number"
                  min="1"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="weight" className="text-sm font-medium leading-none text-text-primary">
                  Weight
                </label>
                <Input
                  id="weight"
                  type="number"
                  min="1"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                />
              </div>
            </div>
            <div className="space-y-2">
              <label htmlFor="models" className="text-sm font-medium leading-none text-text-primary">
                Models (comma separated)
              </label>
              <Input
                id="models"
                value={models}
                onChange={(e) => setModels(e.target.value)}
                placeholder="model-id-1, model-id-2"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={createProvider.isPending || !name}>
              {createProvider.isPending ? "Adding..." : "Add Provider"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
