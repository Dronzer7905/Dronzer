"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { authApi } from "@/lib/api/auth";
import { useAuthStore } from "@/lib/stores/auth-store";
import { toast } from "sonner";
import { Mail, Lock, Eye, EyeOff, Loader2, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

const setupSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(8, "Password must be at least 8 characters long"),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type SetupForm = z.infer<typeof setupSchema>;

export default function SetupPage() {
  const router = useRouter();
  const login = useAuthStore((s) => s.login);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hasHydrated, setHasHydrated] = useState(false);

  // Check hydration state
  useEffect(() => {
    useAuthStore.persist.onFinishHydration(() => setHasHydrated(true));
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setHasHydrated(useAuthStore.persist.hasHydrated());
  }, []);

  // Check setup status
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await authApi.getSetupStatus();
        if (status.is_setup) {
          // If already setup, go to login (or dashboard if logged in)
          if (hasHydrated && isAuthenticated) {
            router.replace("/dashboard");
          } else {
            router.replace("/login");
          }
        } else {
          setIsLoading(false);
        }
      } catch (err) {
        console.error("Failed to check setup status", err);
        toast.error("Could not verify system status. Backend might be down.");
      }
    };
    checkStatus();
  }, [hasHydrated, isAuthenticated, router]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SetupForm>({
    resolver: zodResolver(setupSchema),
  });

  const onSubmit = async (data: SetupForm) => {
    setIsSubmitting(true);
    try {
      // Use the newly created API method
      const res = await authApi.setup({ email: data.email, password: data.password });
      
      // Automatically log the user in since the backend returns tokens
      login(res.access_token, res.refresh_token);
      toast.success("Initial administrator account created!");
      router.push("/dashboard");
    } catch (err: unknown) {
      toast.error((err as Error).message || "Failed to setup admin account.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center p-4">
        <Loader2 className="w-8 h-8 text-accent-primary animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg-primary flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-accent-primary/20 blur-[120px] rounded-full pointer-events-none animate-pulse-glow" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent-secondary/20 blur-[120px] rounded-full pointer-events-none animate-pulse-glow" style={{ animationDelay: "2s" }} />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="w-full max-w-md"
      >
        <div className="glass-card-hover p-8 sm:p-10 z-10 relative">
          <div className="flex flex-col items-center mb-8 text-center">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="w-12 h-12 rounded-xl gradient-accent flex items-center justify-center mb-4 shadow-lg shadow-accent-primary/30"
            >
              <ShieldCheck className="text-white w-6 h-6" />
            </motion.div>
            <h1 className="text-2xl font-bold text-gradient mb-2">Welcome to Dronzer</h1>
            <p className="text-text-secondary text-sm">Create the initial administrator account</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-text-tertiary">
                  <Mail className="h-5 w-5" />
                </div>
                <input
                  {...register("email")}
                  type="email"
                  placeholder="admin@company.com"
                  className="input-field w-full pl-11 h-12"
                  disabled={isSubmitting}
                />
              </div>
              {errors.email && (
                <p className="mt-1.5 text-xs text-error">{errors.email.message}</p>
              )}
            </div>

            <div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-text-tertiary">
                  <Lock className="h-5 w-5" />
                </div>
                <input
                  {...register("password")}
                  type={showPassword ? "text" : "password"}
                  placeholder="Password (min. 8 characters)"
                  className="input-field w-full pl-11 pr-11 h-12"
                  disabled={isSubmitting}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-text-tertiary hover:text-text-primary transition-colors focus:outline-none"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1.5 text-xs text-error">{errors.password.message}</p>
              )}
            </div>

            <div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-text-tertiary">
                  <Lock className="h-5 w-5" />
                </div>
                <input
                  {...register("confirmPassword")}
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Confirm Password"
                  className="input-field w-full pl-11 pr-11 h-12"
                  disabled={isSubmitting}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-text-tertiary hover:text-text-primary transition-colors focus:outline-none"
                  tabIndex={-1}
                >
                  {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1.5 text-xs text-error">{errors.confirmPassword.message}</p>
              )}
            </div>

            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              type="submit"
              disabled={isSubmitting}
              className="w-full h-12 rounded-lg gradient-accent text-white font-medium shadow-lg shadow-accent-primary/25 hover:shadow-accent-primary/40 transition-all flex items-center justify-center disabled:opacity-70 disabled:cursor-not-allowed mt-2"
            >
              {isSubmitting ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                "Complete Setup"
              )}
            </motion.button>
          </form>
          
          <div className="mt-8 pt-6 border-t border-border-primary text-center">
            <p className="text-xs text-text-muted">
              This account will have full access to all organizations and projects.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
