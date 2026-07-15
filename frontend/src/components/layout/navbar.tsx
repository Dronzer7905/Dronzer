"use client";

import { usePathname } from "next/navigation";
import { useAppStore } from "@/lib/stores/app-store";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useOrganizations } from "@/lib/hooks/use-organizations";
import { useProjects } from "@/lib/hooks/use-projects";
import { Search, LogOut, ChevronDown, User, Check } from "lucide-react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { cn } from "@/lib/utils";
import { Skeleton } from "@/components/ui/skeleton";

function getPageName(pathname: string) {
  if (pathname === "/dashboard") return "Overview";
  const parts = pathname.split("/").filter(Boolean);
  if (parts.length > 1) {
    const name = parts[1].replace("-", " ");
    return name.charAt(0).toUpperCase() + name.slice(1);
  }
  return "Overview";
}

export function Navbar() {
  const pathname = usePathname();
  const pageName = getPageName(pathname);
  
  const { activeOrganization, activeProject, setActiveOrg, setActiveProject } = useAppStore();
  const { userEmail, userRole, logout } = useAuthStore();
  
  const { data: orgs, isLoading: loadingOrgs } = useOrganizations();
  const { data: projects, isLoading: loadingProjects } = useProjects(activeOrganization?.id);

  const openCommandPalette = () => {
    window.dispatchEvent(new CustomEvent("open-command-palette"));
  };

  return (
    <header className="h-16 border-b border-border-primary bg-bg-secondary/80 backdrop-blur-md flex items-center justify-between px-6 z-10 shrink-0">
      
      {/* Left: Breadcrumbs / Context */}
      <div className="flex items-center gap-4 flex-1">
        <h1 className="text-lg font-semibold text-text-primary mr-4">{pageName}</h1>
        
        <div className="hidden md:flex items-center gap-2 text-sm">
          {/* Organization Switcher */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border-primary bg-bg-card hover:bg-bg-card-hover transition-colors focus-visible:ring-2 focus-visible:ring-accent-primary focus:outline-none">
                <span className="text-text-secondary">Org:</span>
                <span className="font-medium text-text-primary truncate max-w-[120px]">
                  {loadingOrgs ? <Skeleton className="w-16 h-4 inline-block" /> : (activeOrganization?.name || "Select Org")}
                </span>
                <ChevronDown className="w-4 h-4 text-text-tertiary" />
              </button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content className="w-56 glass-card p-1 z-50 rounded-lg shadow-xl animate-in fade-in-0 zoom-in-95 data-[side=bottom]:slide-in-from-top-2" sideOffset={8}>
                <DropdownMenu.Label className="px-2 py-1.5 text-xs font-semibold text-text-tertiary">Organizations</DropdownMenu.Label>
                {orgs?.map(org => (
                  <DropdownMenu.Item
                    key={org.id}
                    onClick={() => setActiveOrg(org)}
                    className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-text-primary cursor-pointer hover:bg-bg-elevated focus:bg-bg-elevated focus:outline-none"
                  >
                    <div className="w-4 flex justify-center">
                      {activeOrganization?.id === org.id && <Check className="w-4 h-4 text-accent-primary" />}
                    </div>
                    <span className="truncate">{org.name}</span>
                  </DropdownMenu.Item>
                ))}
                {!orgs?.length && !loadingOrgs && (
                  <div className="px-2 py-2 text-sm text-text-muted">No organizations found</div>
                )}
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>

          <span className="text-border-secondary">/</span>

          {/* Project Switcher */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <button 
                disabled={!activeOrganization}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border-primary bg-bg-card hover:bg-bg-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus-visible:ring-2 focus-visible:ring-accent-primary focus:outline-none"
              >
                <span className="text-text-secondary">Project:</span>
                <span className="font-medium text-text-primary truncate max-w-[120px]">
                  {!activeOrganization ? "None" : loadingProjects ? <Skeleton className="w-16 h-4 inline-block" /> : (activeProject?.name || "Select Project")}
                </span>
                <ChevronDown className="w-4 h-4 text-text-tertiary" />
              </button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content className="w-56 glass-card p-1 z-50 rounded-lg shadow-xl animate-in fade-in-0 zoom-in-95 data-[side=bottom]:slide-in-from-top-2" sideOffset={8}>
                <DropdownMenu.Label className="px-2 py-1.5 text-xs font-semibold text-text-tertiary">Projects</DropdownMenu.Label>
                {projects?.map(proj => (
                  <DropdownMenu.Item
                    key={proj.id}
                    onClick={() => setActiveProject(proj)}
                    className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-text-primary cursor-pointer hover:bg-bg-elevated focus:bg-bg-elevated focus:outline-none"
                  >
                    <div className="w-4 flex justify-center">
                      {activeProject?.id === proj.id && <Check className="w-4 h-4 text-accent-primary" />}
                    </div>
                    <span className="truncate">{proj.name}</span>
                    <span className={cn("ml-auto text-[10px] uppercase px-1.5 py-0.5 rounded", 
                      proj.environment === 'production' ? "bg-success-muted text-success" : 
                      proj.environment === 'staging' ? "bg-warning-muted text-warning" : "bg-info-muted text-info"
                    )}>
                      {proj.environment.substring(0, 4)}
                    </span>
                  </DropdownMenu.Item>
                ))}
                {!projects?.length && !loadingProjects && (
                  <div className="px-2 py-2 text-sm text-text-muted">No projects found</div>
                )}
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4">
        <button
          onClick={openCommandPalette}
          className="hidden sm:flex items-center gap-3 px-3 py-1.5 text-sm text-text-tertiary bg-bg-input border border-border-primary rounded-lg hover:border-border-secondary hover:text-text-secondary transition-colors focus-visible:ring-2 focus-visible:ring-accent-primary focus:outline-none"
        >
          <Search className="w-4 h-4" />
          <span>Search...</span>
          <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 rounded bg-bg-elevated font-mono text-[10px] font-medium text-text-muted">
            <span className="text-xs">⌘</span>K
          </kbd>
        </button>
        <button 
          onClick={openCommandPalette}
          className="sm:hidden p-2 text-text-tertiary hover:text-text-primary"
        >
          <Search className="w-5 h-5" />
        </button>

        {/* User Menu */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button className="flex items-center justify-center w-8 h-8 rounded-full bg-accent-muted text-accent-primary hover:bg-accent-primary hover:text-white transition-colors focus-visible:ring-2 focus-visible:ring-accent-primary focus:outline-none">
              <User className="w-4 h-4" />
            </button>
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content className="w-56 glass-card p-1 z-50 rounded-lg shadow-xl animate-in fade-in-0 zoom-in-95 data-[side=bottom]:slide-in-from-top-2 mr-6" sideOffset={8}>
              <div className="px-3 py-2 border-b border-border-primary mb-1">
                <p className="text-sm font-medium text-text-primary truncate">{userEmail || "User"}</p>
                <p className="text-xs text-text-tertiary capitalize mt-0.5">{userRole?.replace("_", " ").toLowerCase() || "Admin"}</p>
              </div>
              <DropdownMenu.Item
                onClick={logout}
                className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-error cursor-pointer hover:bg-error-muted focus:bg-error-muted focus:outline-none"
              >
                <LogOut className="w-4 h-4" />
                <span>Log out</span>
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}
