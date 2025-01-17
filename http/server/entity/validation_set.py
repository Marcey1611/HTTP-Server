from handler.divs.div_handler import get_divs, post_divs
from handler.products.product_handler import get_products, post_products
from handler.users.user_handler import get_users, post_users, delete_users

set = {
    "/": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_home",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_info",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info/routes": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_routes_info",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info/headers": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_headers_info",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info/general": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_general_info",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/users": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_get_users",
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": get_users
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["application/json"]},
            "handler": "handle_post_user",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": post_users
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["application/json"]},
            "handler": "handle_put_user",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"]
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_delete_user",
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": delete_users
        }
    },
    "/products": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_get_products",
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"],
            "handler": get_products
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["application/xml"]},
            "handler": "handle_post_product",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"],
            "handler": post_products
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["application/xml"]},
            "handler": "handle_put_product",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"]
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_delete_product",
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"]
        }
    },
    "/divs": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_get_divs",
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": get_divs
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["text/html"]},
            "handler": "handle_post_div",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": post_divs
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content_type": ["text/html"]},
            "handler": "handle_put_div",
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"]
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "handler": "handle_delete_div",
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "text/html"]
        }
    }
}