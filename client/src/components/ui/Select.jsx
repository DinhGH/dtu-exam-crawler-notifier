import React from "react";
import { cn } from "../../utils/cn";
import { ChevronDown } from "lucide-react";

const Select = React.forwardRef(
  (
    { className, options, value, onChange, error, placeholder, ...props },
    ref,
  ) => {
    return (
      <div className="w-full relative">
        <div className="relative">
          <select
            value={value || ""}
            onChange={onChange}
            ref={ref}
            className={cn(
              "flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
              error && "border-red-500 focus:ring-red-500",
              className,
            )}
            {...props}
          >
            {placeholder && <option value="">{placeholder}</option>}
            {options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500 pointer-events-none" />
        </div>
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>
    );
  },
);

Select.displayName = "Select";

export { Select };
