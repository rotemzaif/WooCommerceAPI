API_HOSTS = {
    # "test": "http://localhost:10005/wp-json/wc/v3/",  # wordpress via local
    # "test": "http://localhost:8000/wp-json/wc/v3/",  # wordpress via docker container
    # "test": "http://host.docker.internal:8000/wp-json/wc/v3/",  # wordpress via docker container
    "test": "http://10.0.0.7:8000/wp-json/wc/v3/",  # wordpress via docker container
    "dev": "",
    "prod": ""
}

WOO_API_HOSTS = {
    # "test": "http://localhost:10005/",  # wordpress via local
    # "test": "http://localhost:8000/",  # wordpress via docker container
    "test": "http://10.0.0.7:8000/",  # wordpress via docker container
    "dev": "",
    "prod": ""
}

DB_HOSTS = {
    'machine1_local': {
        "test": {
            "host": "localhost",
            "database": "local",
            "table_prefix": "wp_",
            "port": 10006
        },
        "dev": {},
        "prod": {}
    },
    'machine1_docker': {
        "test": {
            "host": "localhost",
            "database": "mydb",
            "table_prefix": "wp_",
            "port": 3306
        },
        "dev": {},
        "prod": {}
    },
    'docker': {
        "test": {
            "host": "host.docker.internal",
            "database": "mydb",
            "table_prefix": "wp_",
            "port": 3306
        },
        "dev": {},
        "prod": {}
    }
}
