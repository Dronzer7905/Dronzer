"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { FolderKanban, Plus, Trash2, Check, Search, Loader2, X, AlertCircle } from "lucide-react";
import Link from "next/link";

import { useProjects, useCreateProject, useDeleteProject } from "@/lib/hooks/use-projects";
import { useAppStore } from "@/lib/stores/app-store";
import { EmptyState } from "@/components/ui/empty-state";
import { ConfirmationModal } from "@/components/ui/confirmation-modal";
import { SkeletonCard } from "@/components/ui/skeleton";
import type { ProjectResponse } from "@/lib/api/types";
import { cn } from "@/lib/utils";

const projectSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  environment: z.enum(["development", "staging", "production"]),
});
type ProjectForm = z.infer<typeof projectSchema>;

export default function ProjectsPage() {
  const { activeOrganization, activeProject, setActiveProject } = useAppStore();
  const { data: projects, isLoading } = useProjects(activeOrganization?.id);
  const createProject = useCreateProject();
  const deleteProject = useDeleteProject();

  const [search, setSearch] = useState("");
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState<ProjectResponse | null>(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ProjectForm>({
    resolver: zodResolver(projectSchema),
    defaultValues: { name: "", environment: "production" }
  });

  const filteredProjects = projects?.filter(p => p.name.toLowerCase().includes(search.toLowerCase())) || [];

  const handleCreate = async (data: ProjectForm) => {
    if (!activeOrganization) return;
    try {
      await createProject.mutateAsync({
        ...data,
        org_id: activeOrganization.id
      });
      setIsCreateOpen(false);
      reset();
    } catch (e) {
      // handled by mutation
    }
  };

  const handleDelete = async () => {
    if (!projectToDelete) return;
    try {
      await deleteProject.mutateAsync(projectToDelete.id);
      if (activeProject?.id === projectToDelete.id) {
        setActiveProject(null);
      }
    } catch (e) {
      // handled by mutation
    }
  };

  if (!activeOrganization) {
    return (
      <div className="max-w-3xl mx-auto mt-12">
        <div className="glass-card p-8 flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-full bg-warning-muted flex items-center justify-center mb-4">
            <AlertCircle className="w-8 h-8 text-warning" />
          </div>
          <h2 className="text-xl font-bold text-text-primary mb-2">No Organization Selected</h2>
          <p className="text-text-secondary mb-6 max-w-md">
            You need to select an active organization to view and manage projects.
          </p>
          <Link href="/dashboard/organizations" className="px-5 py-2.5 rounded-lg gradient-accent text-white font-medium">
            Go to Organizations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold text-text-primary tracking-tight">Projects</h2>
            <div className="px-2.5 py-0.5 rounded-full bg-bg-elevated border border-border-primary text-xs font-medium text-text-secondary">
              Org: {activeOrganization.name}
            </div>
          </div>
          <p className="text-sm text-text-secondary mt-1">Manage applications and environments.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input 
              type="text" 
              placeholder="Search projects..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="input-field pl-9 h-10 w-full sm:w-64"
            />
          </div>
          <button 
            onClick={() => setIsCreateOpen(true)}
            className="h-10 px-4 rounded-lg gradient-accent text-white text-sm font-medium flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            <span className="hidden sm:inline">Create Project</span>
          </button>
        </div>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : filteredProjects.length === 0 ? (
        <EmptyState 
          icon={FolderKanban}
          title={search ? "No projects found" : "No projects yet"}
          description={search ? `No results for "${search}"` : `Create your first project in ${activeOrganization.name}.`}
          action={
            !search && (
              <button 
                onClick={() => setIsCreateOpen(true)}
                className="px-4 py-2 rounded-lg gradient-accent text-white text-sm font-medium"
              >
                Create Project
              </button>
            )
          }
        />
      ) : (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {filteredProjects.map((project, i) => {
            const isActive = activeProject?.id === project.id;
            
            return (
              <motion.div 
                key={project.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card hover:glass-card-hover p-6 flex flex-col transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center border border-border-primary">
                      <FolderKanban className="w-5 h-5 text-text-secondary" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-text-primary text-base truncate max-w-[150px]">{project.name}</h3>
                      <div className="mt-1">
                        <span className={cn("text-[10px] uppercase px-1.5 py-0.5 rounded font-medium", 
                          project.environment === 'production' ? "bg-success-muted text-success" : 
                          project.environment === 'staging' ? "bg-warning-muted text-warning" : "bg-info-muted text-info"
                        )}>
                          {project.environment}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <button 
                    onClick={() => setProjectToDelete(project)}
                    className="p-2 text-text-tertiary hover:text-error hover:bg-error-muted rounded-lg opacity-0 group-hover:opacity-100 transition-all focus:opacity-100 focus:outline-none"
                    title="Delete Project"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                
                <div className="space-y-3 mb-6 flex-1">
                  <div className="text-xs text-text-tertiary">
                    Created on {new Date(project.created_at).toLocaleDateString()}
                  </div>
                </div>
                
                <button
                  onClick={() => setActiveProject(project)}
                  disabled={isActive}
                  className={`w-full py-2 rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-2
                    ${isActive 
                      ? "bg-accent-muted text-accent-primary cursor-default border border-accent-primary/20" 
                      : "bg-bg-elevated text-text-secondary hover:text-text-primary hover:border-border-secondary border border-border-primary"
                    }`}
                >
                  {isActive ? (
                    <>
                      <Check className="w-4 h-4" /> Active Context
                    </>
                  ) : "Set as Active"}
                </button>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Create Modal */}
      <Dialog.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex items-center justify-between mb-6">
              <Dialog.Title className="text-lg font-semibold text-text-primary">Create Project</Dialog.Title>
              <Dialog.Close asChild>
                <button className="p-1 rounded-lg hover:bg-bg-elevated text-text-tertiary hover:text-text-primary transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>
            
            <form onSubmit={handleSubmit(handleCreate)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Project Name</label>
                <input 
                  {...register("name")} 
                  autoFocus
                  className="input-field w-full h-10" 
                  placeholder="e.g. Chat App Frontend"
                  disabled={createProject.isPending}
                />
                {errors.name && <p className="mt-1.5 text-xs text-error">{errors.name.message}</p>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Environment</label>
                <select 
                  {...register("environment")} 
                  className="input-field w-full h-10 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
                  disabled={createProject.isPending}
                >
                  <option value="development">Development</option>
                  <option value="staging">Staging</option>
                  <option value="production">Production</option>
                </select>
                {errors.environment && <p className="mt-1.5 text-xs text-error">{errors.environment.message}</p>}
              </div>
              
              <div className="pt-4 flex justify-end gap-3">
                <Dialog.Close asChild>
                  <button type="button" className="px-4 py-2 rounded-lg text-sm font-medium bg-bg-elevated border border-border-primary text-text-secondary hover:text-text-primary">
                    Cancel
                  </button>
                </Dialog.Close>
                <button 
                  type="submit" 
                  disabled={createProject.isPending}
                  className="px-4 py-2 rounded-lg text-sm font-medium text-white gradient-accent hover:opacity-90 flex items-center gap-2 disabled:opacity-70"
                >
                  {createProject.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                  Create
                </button>
              </div>
            </form>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Delete Confirmation */}
      <ConfirmationModal
        open={!!projectToDelete}
        onOpenChange={(open) => !open && setProjectToDelete(null)}
        title="Delete Project"
        description={`Are you sure you want to delete "${projectToDelete?.name}"? This action cannot be undone.`}
        variant="danger"
        confirmLabel="Delete Project"
        onConfirm={handleDelete}
        loading={deleteProject.isPending}
      />
    </div>
  );
}
