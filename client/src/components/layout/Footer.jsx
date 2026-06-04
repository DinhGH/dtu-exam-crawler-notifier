const Footer = () => {
  return (
    <footer className="border-t border-gray-200 bg-white py-8">
      <div className="container mx-auto px-4">
        <div className="mt-8 border-t border-gray-200 pt-4 text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} DTU Exam Notifier. All rights
          reserved.
        </div>
      </div>
    </footer>
  );
};

export { Footer };
