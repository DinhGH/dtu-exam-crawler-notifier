import React from "react";
import { cn } from "../../utils/cn";

const Table = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <div className="relative w-full overflow-auto">
      <table
        ref={ref}
        className={cn("w-full caption-bottom text-sm", className)}
        {...props}
      >
        <thead className="[&_tr]:border-b">
          <tr className="border-b border-gray-200 bg-gray-50/50 text-left dark:border-gray-800 dark:bg-gray-900/50">
            <th className="h-12 px-4 align-middle font-medium text-gray-500 dark:text-gray-400">
              <span className="sr-only">Expand</span>
            </th>
            {children?.props?.children?.props?.children?.map?.((th, i) => (
              <th
                key={i}
                className="h-12 px-4 align-middle font-medium text-gray-500 dark:text-gray-400"
              >
                {th}
              </th>
            ))}
          </tr>
        </thead>
        <tbody ref={ref} className="[&_tr:last-child]:border-0">
          {children}
        </tbody>
      </table>
    </div>
  );
});

Table.displayName = "Table";

const TableHeader = React.forwardRef(
  ({ className, children, ...props }, ref) => {
    return (
      <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props}>
        {children}
      </thead>
    );
  },
);

TableHeader.displayName = "TableHeader";

const TableBody = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <tbody
      ref={ref}
      className={cn("[&_tr:last-child]:border-0", className)}
      {...props}
    >
      {children}
    </tbody>
  );
});

TableBody.displayName = "TableBody";

const TableRow = React.forwardRef(
  ({ className, children, hover, ...props }, ref) => {
    return (
      <tr
        ref={ref}
        className={cn(
          "border-b border-gray-200 transition-colors hover:bg-gray-50/50 data-[state=selected]:bg-gray-50 dark:border-gray-800 dark:hover:bg-gray-800/50",
          hover && "cursor-pointer",
          className,
        )}
        {...props}
      >
        {children}
      </tr>
    );
  },
);

TableRow.displayName = "TableRow";

const TableHead = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <th
      ref={ref}
      className={cn(
        "h-12 px-4 text-left align-middle font-medium text-gray-500 dark:text-gray-400",
        className,
      )}
      {...props}
    >
      {children}
    </th>
  );
});

TableHead.displayName = "TableHead";

const TableCell = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <td
      ref={ref}
      className={cn(
        "p-4 align-middle text-gray-700 dark:text-gray-300",
        className,
      )}
      {...props}
    >
      {children}
    </td>
  );
});

TableCell.displayName = "TableCell";

const TableCaption = React.forwardRef(
  ({ className, children, ...props }, ref) => {
    return (
      <caption
        ref={ref}
        className={cn(
          "mt-4 text-sm text-gray-500 dark:text-gray-400",
          className,
        )}
        {...props}
      >
        {children}
      </caption>
    );
  },
);

TableCaption.displayName = "TableCaption";

export {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  TableCaption,
};
