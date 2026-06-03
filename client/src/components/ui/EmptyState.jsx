import { AlertCircle, SearchX } from "lucide-react";
import { cn } from "../../utils/cn";

const EmptyState = ({ icon = "search", title, description, className }) => {
  const icons = {
    search: <SearchX className="h-12 w-12 text-gray-400" />,
    alert: <AlertCircle className="h-12 w-12 text-gray-400" />,
  };

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-gray-50 p-8 text-center dark:border-gray-800 dark:bg-gray-900/50",
        className,
      )}
    >
      {icons[icon]}
      <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
        {title}
      </h3>
      {description && (
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          {description}
        </p>
      )}
    </div>
  );
};

export { EmptyState };
