import React from "react";
import { cn } from "../../utils/cn";
import { Loader2 } from "lucide-react";

const buttonVariants = {
  variant: {
    default: "bg-blue-600 text-white hover:bg-blue-700",
    secondary:
      "bg-gray-100 text-gray-900 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700",
    outline:
      "border border-gray-300 bg-white hover:bg-gray-50 text-gray-900 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 dark:hover:bg-gray-800",
    ghost:
      "hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:text-gray-300",
    danger: "bg-red-600 text-white hover:bg-red-700",
  },
  size: {
    default: "px-4 py-2",
    sm: "px-3 py-1.5 text-sm",
    lg: "px-6 py-3",
    icon: "p-2",
  },
};

const Button = React.forwardRef(
  (
    {
      className,
      variant = "default",
      size = "default",
      isLoading,
      children,
      ...props
    },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed",
          buttonVariants.variant[variant],
          buttonVariants.size[size],
          className,
        )}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";

export { Button };
