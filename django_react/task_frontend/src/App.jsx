import { useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";

export default function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => setRefreshTrigger((prev) => prev + 1);

  return (
    <div className="min-h-screen bg-slate-50 flex justify-center py-12 px-4">
      <div className="w-full max-w-2xl">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
            Task Manager
          </h1>
          <p className="text-slate-500 mt-2">Stay organized and get things done.</p>
        </header>

        <TaskForm refresh={handleRefresh} />
        
        <div className="mt-8">
          <TaskList key={refreshTrigger} />
        </div>
      </div>
    </div>
  );
}