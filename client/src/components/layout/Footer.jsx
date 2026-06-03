import { Mail, Heart } from "lucide-react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="border-t border-gray-200 bg-white py-8 dark:border-gray-800 dark:bg-gray-900">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="mb-4 text-lg font-bold text-gray-900 dark:text-gray-100">
              DTU Exam Notifier
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Hệ thống tự động theo dõi và thông báo danh sách thi của Đại học
              Duy Tân qua Email.
            </p>
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold text-gray-900 dark:text-gray-100">
              Liên kết
            </h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>
                <Link
                  to="/"
                  className="hover:text-blue-600 dark:hover:text-blue-400"
                >
                  Trang chủ
                </Link>
              </li>
              <li>
                <Link
                  to="/register"
                  className="hover:text-blue-600 dark:hover:text-blue-400"
                >
                  Đăng ký theo dõi
                </Link>
              </li>
              <li>
                <Link
                  to="/search"
                  className="hover:text-blue-600 dark:hover:text-blue-400"
                >
                  Tra cứu danh sách thi
                </Link>
              </li>
              <li>
                <Link
                  to="/files"
                  className="hover:text-blue-600 dark:hover:text-blue-400"
                >
                  Danh sách tệp
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold text-gray-900 dark:text-gray-100">
              Liên hệ
            </h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li className="flex items-center space-x-2">
                <Mail className="h-4 w-4" />
                <span>contact@dtuexamnotifier.com</span>
              </li>
              <li className="flex items-center space-x-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.38 7.86 10.9.57.1.78-.25.78-.56 0-.28-.01-1.02-.01-2-3.2.7-3.88-1.46-3.88-1.46-.52-1.32-1.27-1.67-1.27-1.67-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.68 1.25 3.33.96.1-.74.4-1.25.73-1.54-2.55-.29-5.23-1.28-5.23-5.69 0-1.25.45-2.27 1.18-3.07-.12-.29-.51-1.46.11-3.04 0 0 .96-.31 3.14 1.17.91-.25 1.88-.37 2.85-.37.97 0 1.94.12 2.85.37 2.18-1.48 3.14-1.17 3.14-1.17.62 1.58.23 2.75.11 3.04.73.8 1.18 1.82 1.18 3.07 0 4.42-2.69 5.4-5.25 5.68.41.35.77 1.04.77 2.1 0 1.52-.01 2.75-.01 3.12 0 .31.21.66.79.55C20.71 21.37 24 17.07 24 12c0-6.35-5.15-11.5-12-11.5z" />
                </svg>
                <span>
                  <a
                    href="https://github.com/DinhGH/dtu-exam-crawler-notifier"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-600 dark:hover:text-blue-400"
                  >
                    GitHub
                  </a>
                </span>
              </li>
            </ul>
            <p className="mt-4 flex items-center justify-center space-x-1 text-sm text-gray-500 dark:text-gray-400">
              Made with <Heart className="h-4 w-4 text-red-500 fill-current" />{" "}
              by DTU Team
            </p>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-200 pt-4 text-center text-sm text-gray-500 dark:border-gray-800 dark:text-gray-400">
          &copy; {new Date().getFullYear()} DTU Exam Notifier. All rights
          reserved.
        </div>
      </div>
    </footer>
  );
};

export { Footer };
