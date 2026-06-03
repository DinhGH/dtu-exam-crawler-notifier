import { cn } from "../../utils/cn";
import { Loader2 } from "lucide-react";

const LoadingSpinner = ({ className, size = 24 }) => {
  return (
    <Loader2
      className={cn("animate-spin text-blue-600", className)}
      size={size}
    />
  );
};

export { LoadingSpinner };
