import { useState } from "react";
import API from "../api";

export default function TaskForm({ refresh }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const submitTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    setLoading(true);
    try {
      await API.post("tasks/", {
        title,
        description,
        completed: false
      });
      setTitle("");
      setDescription("");
      refresh();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={submitTask}
      className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200"
    >
      <h2 className="text-lg font-bold text-slate-800 mb-5">Create New Task</h2>
      
      <div className="space-y-4">
        <input
          className="w-full bg-slate-50 border border-slate-200 p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          className="w-full bg-slate-50 border border-slate-200 p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all h-24 resize-none"
          placeholder="Add some details..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button
          disabled={loading}
          className="w-full bg-blue-600 text-white font-semibold py-3 rounded-xl hover:bg-blue-700 active:transform active:scale-[0.98] transition-all disabled:opacity-50"
        >
          {loading ? "Adding..." : "Add Task"}
        </button>
      </div>
    </form>
  );
}