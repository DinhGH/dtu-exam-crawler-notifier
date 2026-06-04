import { BrowserRouter } from "react-router-dom";
import Router from "./routes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
import { Navbar } from "./components/layout/Navbar";
import { Footer } from "./components/layout/Footer";
import { ThemeProvider } from "./contexts/ThemeContext";

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <div className="min-h-screen bg-gray-50 transition-colors duration-200">
            <Navbar />
            <main className="flex-grow">
              <Router />
            </main>
            <Footer />
            <Toaster position="top-right" richColors />
          </div>
        </BrowserRouter>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
