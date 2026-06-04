import { cn } from "../../utils/cn";
import { ChevronLeft, ChevronRight } from "lucide-react";

const PaginationButton = ({ page, currentPage, onClick }) => {
  const isActive = currentPage === page;
  return (
    <button
      onClick={() => onClick(page)}
      className={cn(
        "h-9 px-4 rounded-md text-sm font-medium transition-colors",
        isActive
          ? "bg-blue-600 text-white hover:bg-blue-700"
          : "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50",
      )}
    >
      {page}
    </button>
  );
};

const Pagination = ({
  className,
  totalPages,
  currentPage,
  onPageChange,
  ...props
}) => {
  const pages = [];
  for (let i = 1; i <= totalPages; i++) {
    pages.push(i);
  }

  return (
    <nav
      className={cn("flex items-center gap-2", className)}
      role="navigation"
      aria-label="Pagination"
      {...props}
    >
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className={cn(
          "h-9 px-4 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        )}
      >
        <ChevronLeft className="h-4 w-4" />
        <span className="sr-only">Previous</span>
      </button>

      {pages.map((page) => (
        <PaginationButton
          key={page}
          page={page}
          currentPage={currentPage}
          onClick={onPageChange}
        />
      ))}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={cn(
          "h-9 px-4 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        )}
      >
        <ChevronRight className="h-4 w-4" />
        <span className="sr-only">Next</span>
      </button>
    </nav>
  );
};

Pagination.displayName = "Pagination";

export { Pagination };
