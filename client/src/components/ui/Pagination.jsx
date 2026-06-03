import { cn } from "../../utils/cn";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "./Button";

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
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
      >
        <ChevronLeft className="h-4 w-4" />
        <span className="sr-only">Previous</span>
      </Button>

      {pages.map((page) => (
        <Button
          key={page}
          variant={currentPage === page ? "default" : "outline"}
          size="sm"
          onClick={() => onPageChange(page)}
          className={
            currentPage === page
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : ""
          }
        >
          {page}
        </Button>
      ))}

      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      >
        <ChevronRight className="h-4 w-4" />
        <span className="sr-only">Next</span>
      </Button>
    </nav>
  );
};

Pagination.displayName = "Pagination";

export { Pagination };
