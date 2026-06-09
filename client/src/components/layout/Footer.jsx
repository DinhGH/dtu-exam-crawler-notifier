const Footer = () => {
  return (
    <footer className="border-t border-gray-200 bg-white py-4">
      <div className="container mx-auto px-4">
        <div className="  text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} DTU Exam Notifier. All rights
          reserved.
        </div>
      </div>
    </footer>
  );
};

export { Footer };
