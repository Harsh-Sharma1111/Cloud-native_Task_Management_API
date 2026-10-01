def test_create_task(client, auth_headers):
    """Test creating a task with valid authentication (201)."""
    response = client.post('/api/tasks/', json={
        "title": "New Task",
        "description": "Task description",
        "status": "todo",
        "priority": "high"
    }, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task description"
    assert "id" in data

def test_create_task_without_auth(client):
    """Test creating a task without authentication (401)."""
    response = client.post('/api/tasks/', json={
        "title": "Unauthorized Task"
    })
    
    assert response.status_code == 401

def test_create_task_missing_title(client, auth_headers):
    """Test creating a task missing the required title field (400)."""
    response = client.post('/api/tasks/', json={
        "description": "No title task"
    }, headers=auth_headers)
    
    assert response.status_code == 400

def test_create_task_title_too_long(client, auth_headers):
    """Test creating a task with a title exceeding max length (400)."""
    long_title = "A" * 250
    response = client.post('/api/tasks/', json={
        "title": long_title,
    }, headers=auth_headers)
    
    assert response.status_code == 400

def test_list_tasks(client, auth_headers):
    """Test retrieving a list of tasks (200)."""
    # Create a task to ensure the list is not empty
    client.post('/api/tasks/', json={
        "title": "Task for listing"
    }, headers=auth_headers)
    
    response = client.get('/api/tasks/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1
    assert "total" in data

def test_get_nonexistent_task(client):
    """Test retrieving a task that does not exist (404)."""
    response = client.get('/api/tasks/999999')
    assert response.status_code == 404

def test_update_task_status_only(client, auth_headers):
    """Test updating only the status of a task (200)."""
    # 1. Create a task
    create_response = client.post('/api/tasks/', json={
        "title": "Status Update Task",
        "description": "Original description",
        "status": "todo"
    }, headers=auth_headers)
    task_id = create_response.get_json()["id"]

    # 2. Update the task's status
    update_response = client.put(f'/api/tasks/{task_id}', json={
        "status": "in_progress"
    }, headers=auth_headers)
    
    assert update_response.status_code == 200
    
    # 3. Verify only the status changed
    updated_data = update_response.get_json()
    assert updated_data["status"] == "in_progress"
    assert updated_data["title"] == "Status Update Task"
    assert updated_data["description"] == "Original description"

def test_delete_task(client, auth_headers):
    """Test deleting a task (204) and confirming it's gone (404)."""
    # 1. Create a task
    create_response = client.post('/api/tasks/', json={
        "title": "Task to delete"
    }, headers=auth_headers)
    task_id = create_response.get_json()["id"]

    # 2. Delete the task
    delete_response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
    assert delete_response.status_code == 204

    # 3. Confirm 404 on subsequent GET
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404
