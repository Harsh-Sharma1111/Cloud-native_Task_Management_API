import React, { useState, useEffect, useCallback } from 'react';
import { sprintsApi } from '../api/sprintsApi';
import { tasksApi } from '../api/tasksApi';
import { usersApi } from '../api/usersApi';
import KanbanBoard from '../components/KanbanBoard';
import TaskDetailModal from '../components/TaskDetailModal';
import SprintProgress from '../components/SprintProgress';
import { Toaster } from 'react-hot-toast';

export default function BoardPage() {
  const [sprints, setSprints] = useState([]);
  const [selectedSprintId, setSelectedSprintId] = useState('');
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  // Fetch initial sprints and users data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [sprintsData, usersData] = await Promise.all([
          sprintsApi.getAllSprints(),
          usersApi.getAllUsers()
        ]);
        
        setSprints(sprintsData);
        setUsers(usersData);
        
        // Select active sprint by default if exists
        const activeSprint = sprintsData.find(s => s.status === 'active');
        if (activeSprint) {
          setSelectedSprintId(String(activeSprint.id));
        } else if (sprintsData.length > 0) {
          setSelectedSprintId(String(sprintsData[0].id));
        }
      } catch (error) {
        console.error('Failed to load board data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const fetchTasks = useCallback(async () => {
    if (!selectedSprintId) return;
    try {
      const tasksData = await tasksApi.getTasks({ sprint_id: parseInt(selectedSprintId, 10) });
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      import('react-hot-toast').then(({ default: toast }) => {
        toast.error('Failed to load tasks');
      });
    }
  }, [selectedSprintId]);

  // Fetch tasks when selected sprint changes
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleTaskClick = (task) => {
    setSelectedTask(task);
    setIsModalOpen(true);
  };

  const handleCreateTask = () => {
    setSelectedTask(null);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedTask(null);
  };

  const handleTaskSaved = () => {
    setIsModalOpen(false);
    setSelectedTask(null);
    fetchTasks(); // Refresh board
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 md:p-8 max-w-7xl">
      <Toaster position="bottom-right" />
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight">
            Sprint Board
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1 font-medium">
            Manage and track your tasks
          </p>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-3 bg-white dark:bg-gray-800 p-1.5 pl-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
            <label htmlFor="sprint-select" className="text-sm font-semibold text-gray-700 dark:text-gray-300">
              Sprint:
            </label>
            <select
              id="sprint-select"
              value={selectedSprintId}
              onChange={(e) => setSelectedSprintId(e.target.value)}
              className="bg-gray-50 border-0 text-gray-900 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-2 font-medium dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white"
            >
              {sprints.map(sprint => (
                <option key={sprint.id} value={sprint.id}>
                  {sprint.name} ({sprint.status})
                </option>
              ))}
              {sprints.length === 0 && <option value="">No sprints available</option>}
            </select>
          </div>
          
          <button 
            onClick={handleCreateTask}
            className="flex items-center gap-2 px-4 py-2.5 text-sm font-bold text-white bg-blue-600 rounded-xl hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 transition-colors shadow-sm"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
            </svg>
            New Task
          </button>
        </div>
      </div>

      {selectedSprintId && (
        <SprintProgress sprintId={selectedSprintId} />
      )}

      <KanbanBoard 
        tasks={tasks} 
        setTasks={setTasks} 
        users={users} 
        onTaskClick={handleTaskClick} 
      />

      {isModalOpen && (
        <TaskDetailModal 
          task={selectedTask}
          onClose={handleModalClose}
          onSaved={handleTaskSaved}
        />
      )}
    </div>
  );
}
