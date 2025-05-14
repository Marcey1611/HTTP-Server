from handler.divs.div_handler import get_divs, post_divs
from handler.products.product_handler import get_products, post_products, delete_products, put_products
from handler.users.user_handler import get_users, post_users, delete_users, put_users
from handler.root_info.root_info_handler import get_root, get_info, get_config

set = {
    "/": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": get_root,
            "auth_required": False
        }
    },
    "/info": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": get_info,
            "auth_required": False
        }
    },"/info/config": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": get_config,
            "auth_required": False
        }
    },
    "/info/routes": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "auth_required": False
        }
    },
    "/info/headers": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "auth_required": False
        }
    },
    "/info/general": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "auth_required": False
        }
    },
    "/users": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": get_users,
            "auth_required": False
        },
        "POST": {
            "required_headers": {"host": ["set in server.py"], "content-type": ["application/json"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": post_users,
            "auth_required": True
        },
        "PUT": {
            "required_headers": {"host": ["set in server.py"], "content-type": ["application/json"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": put_users,
            "auth_required": True
        },
        "DELETE": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": delete_users,
            "auth_required": True
        }
    },
    "/products": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"],
            "handler": get_products,
            "auth_required": False
        },
        "POST": {
            "required_headers": {"host": ["set in server.py"], "content-type": ["application/xml"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"],
            "handler": post_products,
            "auth_required": True
        },
        "PUT": {
            "required_headers": {"host": ["set in server.py"], "content-type": ["application/xml"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"],
            "handler": put_products,
            "auth_required": True
        },
        "DELETE": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"],
            "handler": delete_products,
            "auth_required": True
        }
    },
    "/divs": {
        "GET": {
            "required_headers": {"host": ["set in server.py"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": get_divs,
            "auth_required": False
        },
        "POST": {
            "required_headers": {"host": ["set in server.py"], "content-type": ["text/html"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": post_divs,
            "auth_required": True
        }
    }
}