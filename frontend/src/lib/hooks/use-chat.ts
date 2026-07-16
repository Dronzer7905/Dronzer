import { useQuery } from "@tanstack/react-query";
import { chatApi } from "@/lib/api/chat";

export function useGatewayModels() {
  return useQuery({
    queryKey: ["gateway-models"],
    queryFn: () => chatApi.listModels(),
  });
}
