import { useState } from "react";
import API from "../api";

export default function TaskItem({ task, refresh }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDesc, setEditDesc] = useState(task.description);

  const deleteTask = async () => {
    await API.delete(`tasks/${task.id}/`);
    refresh();
  };

  const toggleComplete = async () => {
    await API.put(`tasks/${task.id}/`, {
      ...task,
      completed: !task.completed
    });
    refresh();
  };

  const handleUpdate = async () => {
    await API.put(`tasks/${task.id}/`, {
      ...task,
      title: editTitle,
      description: editDesc
    });
    setIsEditing(false);
    refresh();
  };

  if (isEditing) {
    return (
      <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-5 space-y-3 shadow-inner">
        <input
          className="w-full p-2 rounded-lg border border-blue-300 outline-none focus:ring-2 focus:ring-blue-500"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
        />
        <textarea
          className="w-full p-2 rounded-lg border border-blue-300 outline-none focus:ring-2 focus:ring-blue-500 h-20 resize-none"
          value={editDesc}
          onChange={(e) => setEditDesc(e.target.value)}
        />
        <div className="flex gap-2 justify-end">
          <button 
            onClick={() => setIsEditing(false)}
            className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button 
            onClick={handleUpdate}
            className="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-all"
          >
            Save Changes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white border border-slate-200 rounded-2xl p-5 flex justify-between items-center hover:shadow-md transition-shadow">
      <div className="flex-1 pr-4">
        <div className="flex items-center gap-3 mb-1">
          <h3 className={`font-bold text-lg ${task.completed ? "line-through text-slate-400" : "text-slate-800"}`}>
            {task.title}
          </h3>
          <span className={`text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-full 
            ${task.completed ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"}
          `}>
            {task.completed ? "Done" : "To Do"}
          </span>
        </div>
        <p className="text-slate-500 text-sm line-clamp-2">
          {task.description}
        </p>
      </div>

      <div className="flex items-center gap-1">
        <button
          onClick={toggleComplete}
          className={`p-2 rounded-lg transition-colors ${
            task.completed ? "text-slate-400 hover:bg-slate-100" : "text-blue-600 hover:bg-blue-50"
          }`}
          title="Toggle Status"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
        </button>

        <button
          onClick={() => setIsEditing(true)}
          className="p-2 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors"
          title="Edit Task"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>

        <button
          onClick={deleteTask}
          className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          title="Delete Task"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
}