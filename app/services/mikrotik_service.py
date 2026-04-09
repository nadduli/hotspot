"""MikroTik service — manages physical connection and hotspot users on MikroTik routers."""

import logging
import routeros_api

from app.models.router import Router


logger = logging.getLogger(__name__)


def _get_connection(router: Router):
    """
    Open a connection to a MikroTik router.
    Private helper used by all other functions in this service.
    """
    try:
        pool = routeros_api.RouterOsApiPool(
            host=router.wg_ip,
            username=router.api_username,
            password=router.api_password,
            port=router.api_port,
            plaintext_login=True
        )
        return pool.get_api()
    except Exception as e:
        logger.error(
            f"Failed to connect to router '{router.name}' "
            f"at {router.wg_ip}: {e}"
        )
        raise ConnectionError(
            f"Cannot connect to router '{router.name}' at {router.wg_ip}"
        )


def test_connection(router: Router) -> dict:
    """Test connection and return router identity and system info."""
    try:
        api      = _get_connection(router)
        identity = api.get_resource('/system/identity').get()[0]
        resource = api.get_resource('/system/resource').get()[0]

        logger.info(
            f"Connection successful: router='{router.name}' "
            f"version='{resource.get('version')}' "
            f"uptime='{resource.get('uptime')}'"
        )
        return {
            "connected": True,
            "identity":  identity.get("name"),
            "uptime":    resource.get("uptime"),
            "version":   resource.get("version"),
        }
    except ConnectionError as e:
        logger.error(f"Connection test failed for router '{router.name}': {e}")
        return {
            "connected": False,
            "identity":  None,
            "uptime":    None,
            "version":   None,
            "error":     str(e)
        }


def create_hotspot_user(
    router: Router,
    username: str,
    password: str,
    profile: str
) -> bool:
    """Create a hotspot user on MikroTik after payment is confirmed."""
    try:
        api = _get_connection(router)

        existing = api.get_resource('/ip/hotspot/user').get(name=username)
        if existing:
            logger.warning(
                f"Hotspot user already exists: "
                f"router='{router.name}' username='{username}'"
            )
            return True

        api.get_resource('/ip/hotspot/user').add(
            name=username,
            password=password,
            profile=profile,
            comment="Created by hotspot-app"
        )
        logger.info(
            f"Hotspot user created: "
            f"router='{router.name}' username='{username}' profile='{profile}'"
        )
        return True

    except Exception as e:
        logger.error(
            f"Failed to create hotspot user '{username}' "
            f"on router '{router.name}': {e}"
        )
        raise


def remove_hotspot_user(router: Router, username: str) -> bool:
    """Remove a hotspot user from MikroTik when session expires."""
    try:
        api   = _get_connection(router)
        users = api.get_resource('/ip/hotspot/user').get(name=username)

        if not users:
            logger.warning(
                f"Hotspot user not found for removal: "
                f"router='{router.name}' username='{username}'"
            )
            return False

        user_id = users[0]['.id']
        api.get_resource('/ip/hotspot/user').remove(user_id)
        logger.info(
            f"Hotspot user removed: "
            f"router='{router.name}' username='{username}'"
        )
        return True

    except Exception as e:
        logger.error(
            f"Failed to remove hotspot user '{username}' "
            f"from router '{router.name}': {e}"
        )
        raise


def get_active_sessions(router: Router) -> list:
    """Return all currently active hotspot sessions."""
    try:
        api      = _get_connection(router)
        sessions = api.get_resource('/ip/hotspot/active').get()
        logger.info(
            f"Retrieved {len(sessions)} active session(s) "
            f"from router '{router.name}'"
        )
        return sessions
    except Exception as e:
        logger.error(
            f"Failed to retrieve active sessions "
            f"from router '{router.name}': {e}"
        )
        raise