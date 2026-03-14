import { useEffect, useState } from "react";
import API from "../api";
import TaskItem from "./TaskItem";

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    try {
      const res = await API.get("tasks/");
      setTasks(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  if (loading) return <div className="text-center py-10 text-slate-400">Loading tasks...</div>;

  return (
    <div className="space-y-3">
      {tasks.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl border-2 border-dashed border-slate-200">
          <p className="text-slate-400">No tasks found. Start by adding one above!</p>
        </div>
      ) : (
        tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            refresh={fetchTasks}
          />
        ))
      )}
    </div>
  );
}