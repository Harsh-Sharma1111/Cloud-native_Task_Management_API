import os
from app import create_app
from config import config_by_name

# Use FLASK_ENV or default to 'prod' in Docker
env_name = os.environ.get('FLASK_ENV', 'prod')
config_class = config_by_name.get(env_name, config_by_name['prod'])

# Create the application instance using the selected config
app = create_app(config_class)

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=(env_name == 'dev'))
