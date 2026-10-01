import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import BoardPage from '../pages/BoardPage';
import { tasksApi } from '../api/tasksApi';
import { sprintsApi } from '../api/sprintsApi';
import { usersApi } from '../api/usersApi';

// Mock the API calls
vi.mock('../api/tasksApi', () => ({
  tasksApi: {
    getTasks: vi.fn(),
    updateTask: vi.fn(),
  }
}));

vi.mock('../api/sprintsApi', () => ({
  sprintsApi: {
    getAllSprints: vi.fn(),
  }
}));

vi.mock('../api/usersApi', () => ({
  usersApi: {
    getAllUsers: vi.fn(),
  }
}));

const mockSprints = [
  { id: 1, name: 'Sprint 1', status: 'active' }
];

const mockUsers = [
  { id: 1, name: 'User 1' }
];

describe('KanbanBoard (BoardPage Integration)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows a loading spinner before data arrives', async () => {
    let resolveSprints;
    const sprintsPromise = new Promise(resolve => { resolveSprints = resolve; });
    sprintsApi.getAllSprints.mockReturnValue(sprintsPromise);
    usersApi.getAllUsers.mockResolvedValue([]);
    
    const { container } = render(<BoardPage />);
    
    // Check for the spinner using the Tailwind class used in BoardPage.jsx
    expect(container.querySelector('.animate-spin')).toBeInTheDocument();
    
    // Resolve the promise so the test can exit cleanly
    resolveSprints([]);
  });

  it('renders three columns', async () => {
    sprintsApi.getAllSprints.mockResolvedValue(mockSprints);
    usersApi.getAllUsers.mockResolvedValue(mockUsers);
    tasksApi.getTasks.mockResolvedValue([]);

    render(<BoardPage />);

    // Wait for the loading state to finish by checking for the page title
    await waitFor(() => {
      expect(screen.queryByText('Sprint Board')).toBeInTheDocument();
    });

    // Check that the three column titles are present
    expect(screen.getByText('To Do')).toBeInTheDocument();
    expect(screen.getByText('In Progress')).toBeInTheDocument();
    expect(screen.getByText('Done')).toBeInTheDocument();
  });

  it('places a mocked task in the correct column by status', async () => {
    sprintsApi.getAllSprints.mockResolvedValue(mockSprints);
    usersApi.getAllUsers.mockResolvedValue(mockUsers);
    
    // Mock a task that belongs to the 'in_progress' status
    tasksApi.getTasks.mockResolvedValue([
      { id: 101, title: 'Learn Vitest', status: 'in_progress', sprint_id: 1, priority: 'high', assignee_id: 1 }
    ]);

    render(<BoardPage />);

    // Wait for the task to render
    await waitFor(() => {
      expect(screen.getByText('Learn Vitest')).toBeInTheDocument();
    });

    // Verify it is placed inside the 'In Progress' column
    const inProgressHeading = screen.getByText('In Progress');
    const inProgressColumn = inProgressHeading.closest('div').parentElement;
    
    expect(inProgressColumn).toHaveTextContent('Learn Vitest');
  });

  it('shows an error banner if the tasks fetch rejects', async () => {
    sprintsApi.getAllSprints.mockResolvedValue(mockSprints);
    usersApi.getAllUsers.mockResolvedValue(mockUsers);
    
    // Simulate a rejected API call when fetching tasks
    tasksApi.getTasks.mockRejectedValue(new Error('Network error'));

    render(<BoardPage />);

    // Wait for tasksApi.getTasks to be called
    await waitFor(() => {
      expect(tasksApi.getTasks).toHaveBeenCalled();
    });

    // react-hot-toast will render the toast message, wait for it to appear
    await waitFor(() => {
      expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument();
    });
  });
});
