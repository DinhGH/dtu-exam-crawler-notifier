import { Search } from "lucide-react";
import { Input } from "./Input";

const SearchBox = ({
  placeholder = "Search...",
  value,
  onChange,
  className,
  ...props
}) => {
  return (
    <div className={`relative ${className}`} {...props}>
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
      <Input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="pl-10"
      />
    </div>
  );
};

export { SearchBox };
