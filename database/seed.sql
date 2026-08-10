

USE fastapi_demo;

-- =========================================================
-- SAMPLE DATA
-- =========================================================

INSERT INTO users
    (name, email, password_hash)
VALUES
    ('John Doe', 'john@example.com', '$2b$12$examplehash1'),
    ('Jane Smith', 'jane@example.com', '$2b$12$examplehash2'),
    ('Bob Wilson', 'bob@example.com', '$2b$12$examplehash3');


INSERT INTO projects
    (name, description, owner_id)
VALUES
    (
        'FastAPI Learning',
        'Project for learning FastAPI and SQLAlchemy',
        1
    ),
    (
        'E-commerce API',
        'Example e-commerce backend',
        2
    );


INSERT INTO tasks
    (
        project_id,
        assigned_to,
        title,
        description,
        status,
        priority,
        due_date
    )
VALUES
    (
        1,
        1,
        'Create FastAPI project',
        'Initialize the FastAPI project structure',
        'completed',
        'high',
        '2026-08-05'
    ),
    (
        1,
        2,
        'Configure SQLAlchemy',
        'Configure SQLAlchemy with MySQL',
        'in_progress',
        'high',
        '2026-08-10'
    ),
    (
        1,
        3,
        'Create CRUD endpoints',
        'Implement CRUD operations for tasks',
        'pending',
        'medium',
        '2026-08-15'
    ),
    (
        2,
        2,
        'Create products endpoint',
        'Implement product CRUD',
        'pending',
        'high',
        '2026-08-20'
    );


INSERT INTO task_comments
    (task_id, user_id, comment)
VALUES
    (1, 1, 'Project initialized successfully.'),
    (2, 2, 'SQLAlchemy configuration is in progress.'),
    (2, 1, 'Remember to configure the connection pool.');


INSERT INTO tags
    (name)
VALUES
    ('backend'),
    ('fastapi'),
    ('mysql'),
    ('sqlalchemy'),
    ('api'),
    ('urgent');


INSERT INTO task_tags
    (task_id, tag_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5);
