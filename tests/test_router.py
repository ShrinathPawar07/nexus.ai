# tests/test_router.py

from nexus_ai.core.router import Router

def test_fintech_routing():
    router = Router()
    response = router.route_query("show revenue for TCS", "fintech")
    assert "Revenue analysis" in response

def test_edtech_routing():
    router = Router()
    response = router.route_query("suggest course for AI", "edtech")
    assert "Suggested learning paths" in response
